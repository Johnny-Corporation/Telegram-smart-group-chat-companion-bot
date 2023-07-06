# Bot API
from telebot import TeleBot, types

# Local modules
from Johnny import Johnny
from internet_access import *
from functions import *

# Other
from dotenv import load_dotenv
from os import environ, path, mkdir
import logging
import traceback
from datetime import datetime


load_dotenv(".env")

# Needed for filtering messages when bot was offline
start_time = datetime.now()
skip_old_messages = True
ignored_messages = 0  # count number of ignored messages when bot was offline for logs

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


bot_token = environ.get("BOT_API_TOKEN")

developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")
if not bot_token:
    logger.error("Failed to load BOT_API_TOKEN from environment, exiting...")
    exit()
if not developer_chat_IDs:
    logger.warning("Developers chat ids is not set!")
else:
    developer_chat_IDs = developer_chat_IDs.split(",")


templates = load_templates("templates\\")
stickers = load_stickers("stickers.json")
blacklist = {}  # chat_id:[messages_ids] needed for filtering messages
reply_blacklist = {}  # chat_id:[messages_ids] needed for filtering replies to messages
groups = {}  # {id:Johnny object}

if not path.exists("groups_info"):
    mkdir("groups_info")


bot = TeleBot(bot_token)
bot_id = bot.get_me().id
bot_username = bot.get_me().username

# Init quick access keyboard
keyboard = types.ReplyKeyboardMarkup()
buttons = [
    types.KeyboardButton(text=lang)
    for lang in ["English", "Spanish", "French", "German"]
]  # create buttons
keyboard.add(
    *[types.KeyboardButton(text="/enable"), types.KeyboardButton(text="/disable")]
)


def error_handler(func):
    def wrapper(message):
        try:
            func(message)
        except Exception as e:
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            bot.send_message(
                message.chat.id,
                "Sorry, unexpected error occurred, developers have been already notified!",
            )
            send_to_developers(
                f"Error occurred!!!: \n -----------\n {traceback.format_exc()}\n ---------- ",
                bot,
                developer_chat_IDs,
            )
            send_to_developers("logs.log", bot, developer_chat_IDs, file=True)
        else:
            logger.info(
                f"Command {message.text} executed in chat with id {message.chat.id}"
            )
            # log gpt responses

    return wrapper


def time_filter(message):
    """Filters message which were sent before bot start"""
    global skip_old_messages, ignored_messages
    if not skip_old_messages:
        return True
    message_time = datetime.fromtimestamp(message.date)
    if start_time < message_time:
        skip_old_messages = False
        logger.warning(
            f"{ignored_messages} messages have been ignored since last start."
        )
        return True
    else:
        ignored_messages += 1
        return False


def blacklist_filter(message):
    if message.chat.id not in blacklist:
        return True
    return not (message.message_id in blacklist.get(message.chat.id))


def reply_blacklist_filter(message):
    if message.chat.id not in reply_blacklist:
        return True
    return (message.reply_to_message is None) or (
        message.reply_to_message.message_id not in reply_blacklist[message.chat.id]
    )


# --- Help ---
@bot.message_handler(commands=["help"], func=time_filter)
@error_handler
def help_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["help.txt"],
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"], func=time_filter)
@error_handler
def tokens_info_command(message):
    language_code = groups[message.chat.id].lang_code
    total_tokens = groups[message.chat.id].total_spent_tokens
    bot.reply_to(
        message,
        templates[language_code]["tokens.txt"].format(
            dollars=tokens_to_dollars("", total_tokens), spent_tokens=total_tokens
        ),
    )


# --- About ---
@bot.message_handler(commands=["about", "start"], func=time_filter)
@error_handler
def about_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.reply_to(message, templates[language_code]["description.txt"])


# --- Dynamic generation ---
@bot.message_handler(commands=["dynamic_generation"], func=time_filter)
@error_handler
def dynamic_generation_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].dynamic_gen = not groups[message.chat.id].dynamic_gen
    bot.reply_to(
        message,
        templates[language_code]["dynamic_generation.txt"].format(
            groups[message.chat.id].dynamic_gen
        ),
    )


# --- reply handler for feature requests ---
@error_handler
def feature_request_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} (@{user.username}) 
            from group with name {inner_message.chat.title} requested a feature! 
            Here is what he said: 
            {inner_message.text}""",
        bot,
        developer_chat_IDs,
    )
    bot.reply_to(
        inner_message,
        templates[language_code]["feature_request_thanks.txt"],
    )


# --- reply handler for bug reports ---
@error_handler
def bug_report_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} (@{user.username}) 
            from group with name {inner_message.chat.title} reported a bug! 
            Here is what he said: 
            {inner_message.text}""",
        bot,
        developer_chat_IDs,
    )
    bot.reply_to(
        inner_message,
        templates[language_code]["bug_report_thanks.txt"],
    )


# --- Report bug ---
@bot.message_handler(commands=["report_bug"], func=time_filter)
@error_handler
def report_bug_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["report_bug.txt"])
    if message.chat.id not in reply_blacklist:
        reply_blacklist[message.chat.id] = [bot_reply.message_id]
    else:
        reply_blacklist.append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, bug_report_reply_handler)


# --- Request feature ---
@bot.message_handler(commands=["request_feature"], func=time_filter)
@error_handler
def request_feature_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["request_feature.txt"])
    if message.chat.id not in reply_blacklist:
        reply_blacklist[message.chat.id] = [bot_reply.message_id]
    else:
        reply_blacklist.append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, feature_request_reply_handler)


# --- Enable ---
@bot.message_handler(commands=["enable"], func=time_filter)
@error_handler
def enable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = True
    if language_code == "en":
        return bot.reply_to(message, templates[language_code]["enabled.txt"])
    bot.send_sticker(message.chat.id, stickers["enable"])


# --- Disable ---
@bot.message_handler(commands=["disable"], func=time_filter)
@error_handler
def disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = False
    bot.reply_to(message, templates[language_code]["disabled.txt"])


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"], func=time_filter)
@error_handler
def set_temp_command(message):
    language_code = groups[message.chat.id].lang_code
    # logic (check val from 0 to 2!)
    bot.reply_to(message, "Not implemented")


# --- Change language ---
@bot.message_handler(commands=["change_language"], func=time_filter)
@error_handler
def change_language_command(message):
    change_language(message.chat.id)


def change_language(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="ru"))
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="en"))
    bot.send_message(chat_id, "Choose language", reply_markup=keyboard)


# --- callback handler ---
@bot.callback_query_handler(func=lambda call: True)
def handle_language_change(call):
    previous_lang = groups[call.message.chat.id].lang_code
    if call.data == "en":
        groups[call.message.chat.id].lang_code = "en"
        bot.send_message(call.message.chat.id, "Language changed to english ")
        language_code = "en"
    elif call.data == "ru":
        groups[call.message.chat.id].lang_code = "ru"
        bot.send_message(call.message.chat.id, "Теперь на родном базарим")
        language_code = "ru"

    if not previous_lang:
        bot.send_message(
            call.message.chat.id, templates[language_code]["new_group_welcome.txt"]
        )
        bot.send_message(
            call.message.chat.id,
            ("Initializing..." if language_code == "en" else "Инициализация..."),
            reply_markup=keyboard,
        )

        groups[call.message.chat.id].load_data()

        bot.send_message(
            call.message.chat.id,
            ("Done!" if language_code == "en" else "Готово!"),
        )


# --- Handling new groups ---
@bot.message_handler(content_types=["new_chat_members"], func=time_filter)
@error_handler
def handle_new_chat_members(message):
    for new_chat_member in message.new_chat_members:
        if new_chat_member.id == bot_id:
            init_new_group(message.chat.id)


def init_new_group(chat_id):
    if chat_id in groups:
        groups[chat_id].lang_code = "en"
        bot.send_message(
            chat_id,
            """You haven't set the language, using english. 
            Use /change_language for changing language""",
        )
        language_code = "en"
        bot.send_message(
            chat_id,
            templates[language_code]["new_group_welcome.txt"],
            reply_markup=keyboard,
        )
        bot.send_message(
            chat_id,
            ("Initializing..." if language_code == "en" else "ru"),
        )
        groups[chat_id].load_data()

        bot.send_message(
            chat_id,
            ("Done!" if language_code == "en" else "Готово!"),
        )

    else:
        with open(
            f"groups_info\\{bot.get_chat(chat_id).title}.json",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(convert_to_json(str(bot.get_chat(chat_id))))

        groups[chat_id] = Johnny(bot, chat_id, logger, bot_username)

        blacklist[chat_id] = []
        reply_blacklist[chat_id] = []

        change_language(chat_id)


@bot.message_handler(
    func=lambda message: reply_blacklist_filter(message)
    and blacklist_filter(message)
    and time_filter(message)
)
def main_messages_handler(message):
    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)
    else:
        if response := groups[message.chat.id].new_message(message):
            bot.send_message(message.chat.id, response)


logger.info("Bot started")
bot.polling()
