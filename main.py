# Bot API
from telebot import TeleBot, types

# Local modules
from Johnny import Johnny
from internet_access import *
from functions import *
from logger import logger

# Other
from dotenv import load_dotenv
from os import environ, path, mkdir
import traceback
from datetime import datetime
import threading
from typing import Dict

load_dotenv(".env")

# Needed for filtering messages when bot was offline
start_time = datetime.now()
skip_old_messages = True  # True until message older than bot start time received
ignored_messages = 0  # count number of ignored messages when bot was offline for logs


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
groups: Dict[int, Johnny] = {}  # {group chat_id:Johnny object}

if not path.exists("groups_info"):
    mkdir("groups_info")

if not path.exists("clients_info"):
    mkdir("clients_info")


bot = TeleBot(bot_token)
bot_id = bot.get_me().id
bot_username = bot.get_me().username

# Init quick access keyboard
keyboard = types.ReplyKeyboardMarkup()
keyboard.add(
    *[types.KeyboardButton(text="/enable"), types.KeyboardButton(text="/disable")]
)


def error_handler(func):
    """Handles all occurred errors, logs them, sends error and logs.log to developers

    Args:
        func (function)
    """

    def wrapper(message):
        try:
            func(message)
        except Exception:
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
            send_to_developers("debug_logs.log", bot, developer_chat_IDs, file=True)
            send_to_developers("info_logs.log", bot, developer_chat_IDs, file=True)
        else:
            if not message.text:
                return
            if message.text[0] == "/":  # command
                logger.info(
                    f'Command "{message.text}" executed in chat with id {message.chat.id}by user with id {message.from_user.id}'
                )
            else:
                logger.info(
                    f'Message "{message.text}" sent in chat with id {message.chat.id} by user with id {message.from_user.id}'
                )

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
    "Filters message if its id in blacklist"
    if message.chat.id not in blacklist:
        return True
    return not (message.message_id in blacklist.get(message.chat.id))


def reply_blacklist_filter(message):
    """Bloscks message if it is a reply to message which is in reply_blacklist"""
    if message.chat.id not in blacklist:
        return True
    return (message.reply_to_message is None) or (
        message.reply_to_message.message_id not in reply_blacklist[message.chat.id]
    )


# --- Start ---
@bot.message_handler(commands=["start"], func=time_filter)
@error_handler
def about_command(message):

    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)


# --- About ---
@bot.message_handler(commands=["about"], func=time_filter)
@error_handler
def about_command(message):

    language_code = groups[message.chat.id].lang_code
    bot.reply_to(
        message,
        templates[language_code]["description.txt"]
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


# --- report functions ---
@bot.message_handler(commands=["report"], func=time_filter)
@error_handler
def report_command(message):
    report_markup = types.InlineKeyboardMarkup()
    report_button = types.InlineKeyboardButton(
        text="Report bug", callback_data="report_bug"
    )
    req_button = types.InlineKeyboardButton(
        text="Suggest new feature to bot", callback_data="request_feature"
    )

    report_markup.add(report_button)
    report_markup.add(req_button)

    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["report.txt"],
        reply_markup=report_markup,
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "report_bug" or call.data == "request_feature"
)
def handler_report_buttons(call):
    if call.data == "report_bug":
        report_bug_command(call.message)
    elif call.data == "request_feature":
        request_feature_command(call.message)


# --- set_up functions ---
@bot.message_handler(commands=["set_up"], func=time_filter)
@error_handler
def set_up_command(message):
    set_up_markup = types.InlineKeyboardMarkup()
    system_button = types.InlineKeyboardButton(
        text="Change the role of bot", callback_data="set_role"
    )
    temp_button = types.InlineKeyboardButton(
        text="Change bot's answer length", callback_data="set_temp"
    )
    ans_button = types.InlineKeyboardButton(
        text="Change frequency of bot's answers", callback_data="set_ans"
    )
    memory_button = types.InlineKeyboardButton(
        text="Change the size of your messages-memory", callback_data="set_memory"
    )

    set_up_markup.add(system_button)
    set_up_markup.add(temp_button)
    set_up_markup.add(ans_button)
    set_up_markup.add(memory_button)

    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["set_up_functions.txt"],
        reply_markup=set_up_markup,
        parse_mode="HTML",
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "set_temp"
    or call.data == "set_ans"
    or call.data == "set_memory"
)
def handler_report_buttons(call):
    if call.data == "set_role":
        set_system_content_command(call.message)
    elif call.data == "set_temp":
        set_temp_command(call.message)
    elif call.data == "set_ans":
        set_probability_command(call.message)
    elif call.data == "set_memory":
        set_temp_memory_size_command(call.message)


# --- customizations functions ---
@bot.message_handler(commands=["customization"], func=time_filter)
@error_handler
def customization_command(message):
    customization_markup = types.InlineKeyboardMarkup()
    dyn_gen_button = types.InlineKeyboardButton(
        text="Enable/disable dynamic generation", callback_data="dyn_gen"
    )
    change_lang_button = types.InlineKeyboardButton(
        text="Change the language", callback_data="change_lang"
    )

    customization_markup.add(dyn_gen_button)
    customization_markup.add(change_lang_button)

    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["customization.txt"],
        reply_markup=customization_markup,
        parse_mode="HTML",
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "change_lang" or call.data == "dyn_gen"
)
def handler_report_buttons(call):
    if call.data == "change_lang":
        set_temp_command(call.message)
    elif call.data == "dyn_gen":
        set_probability_command(call.message)


# --- view mode ---
@bot.message_handler(commands=["view_mode"], func=time_filter)
@error_handler
def view_mode_command(message):
    if groups[message.chat.id].enabled == True:
        on_off = "enabled"
        if groups[message.chat.id].trigger_probability == 1:
            mode = "dialog"
        elif groups[message.chat.id].trigger_probability == 0:
            mode = "manual"
        else:
            mode = "auto"

        language_code = groups[message.chat.id].lang_code
        bot.send_message(
            message.chat.id,
            templates[language_code]["view_mode.txt"].format(on_off=on_off, mode=mode),
        )

    else:
        language_code = groups[message.chat.id].lang_code
        bot.send_message(
            message.chat.id, templates[language_code]["view_mode_disabled.txt"]
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
            dollars=tokens_to_dollars(
                groups[message.chat.id].model,
                total_tokens[0],
                total_tokens[1],
            ),
            spent_tokens=sum(groups[message.chat.id].total_spent_tokens),
        ),
    )


# --- Group info ---
@bot.message_handler(commands=["group_info"], func=time_filter)
@error_handler
def group_info_command(message):
    language_code = groups[message.chat.id].lang_code
    total_tokens = groups[message.chat.id].total_spent_tokens
    if groups[message.chat.id].dynamic_gen == False:
        dynamic_gen_en = "disabled"
    else:
        dynamic_gen_en = "enabled"
    if groups[message.chat.id].lang_code == "en":
        language_code1 = "english"
    elif groups[message.chat.id].lang_code == "ru":
        language_code1 = "русский"
    elif groups[message.chat.id].lang_code == "es":
        language_code1 = "español"
    elif groups[message.chat.id].lang_code == "de":
        language_code1 = "deutsch"

    bot.send_message(
        message.chat.id,
        templates[language_code]["group_info.txt"].format(
            group_name=message.chat.title,
            temperature=groups[message.chat.id].temperature,
            answers_frequency=groups[message.chat.id].trigger_probability,
            temporary_memory_size=groups[message.chat.id].temporary_memory_size,
            dollars=tokens_to_dollars(
                groups[message.chat.id].model,
                total_tokens[0],
                total_tokens[1],
            ),
            spent_tokens=sum(groups[message.chat.id].total_spent_tokens),
            dynamic_gen_en=dynamic_gen_en,
            language=language_code1,
        ),
        parse_mode="HTML",
    )


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


# --- reply handler for question to bot
@error_handler
def question_to_bot_reply_handler(inner_message):
    bot.reply_to(inner_message, groups[inner_message.chat.id].one_answer(inner_message))


# --- reply handler for set temp
@error_handler
def set_temp_reply_handler(inner_message):
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        return
    if (val > 2) or (val < 0):
        bot.reply_to(inner_message, "❌")
        return

    groups[inner_message.chat.id].temperature = val
    bot.reply_to(inner_message, "✅")


# --- reply handler for set temp memory size
@error_handler
def set_memory_size_reply_handler(inner_message):
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        return
    if val <= 0:
        bot.reply_to(inner_message, "❌")
        return

    groups[inner_message.chat.id].change_memory_size(val)
    bot.reply_to(inner_message, "✅")


# --- reply handler for set probability
@error_handler
def set_probability_reply_handler(inner_message):
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        return
    if (val < 0) or (val > 1):
        bot.reply_to(inner_message, "❌")
        return

    groups[inner_message.chat.id].trigger_probability = val
    bot.reply_to(inner_message, "✅")


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"], func=time_filter)
@error_handler
def set_temp_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["change_temp.txt"])
    bot.register_for_reply(bot_reply, set_temp_reply_handler)


# --- Set probability ---
@bot.message_handler(commands=["set_answer_probability"], func=time_filter)
@error_handler
def set_probability_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message, templates[language_code]["change_probability.txt"]
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_probability_reply_handler)


# --- Set memory size ---
@bot.message_handler(commands=["temporary_memory_size"], func=time_filter)
@error_handler
def set_temp_memory_size_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message, templates[language_code]["change_temp_memory_size.txt"]
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_memory_size_reply_handler)


# --- Set system content ---
@bot.message_handler(commands=["set_role"], func=time_filter)
@error_handler
def set_system_content_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        "vbnbhohaffobhasabghwrhpghjwrbjwpjwpvgjpvfrjwpjwpvgrfpvgjpivgwrifjopwrwrig",
    )


# --- Report bug ---
@bot.message_handler(commands=["report_bug"], func=time_filter)
@error_handler
def report_bug_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["report_bug.txt"])
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, bug_report_reply_handler)


# --- Request feature ---
@bot.message_handler(commands=["request_feature"], func=time_filter)
@error_handler
def request_feature_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["request_feature.txt"])
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, feature_request_reply_handler)


# ---------- GamePlay funcs ----------


# --- Question to bot  ------
@bot.message_handler(commands=["question_to_bot"], func=time_filter)
@error_handler
def question_to_bot_command(message):
    language_code = groups[message.chat.id].lang_code

    if " " in message.text:
        response = groups[message.chat.id].one_answer(message)
        bot.reply_to(message, response)
    else:
        bot_reply = bot.reply_to(
            message, templates[language_code]["question_to_bot.txt"]
        )
        reply_blacklist[message.chat.id].append(bot_reply.message_id)
        bot.register_for_reply(message, question_to_bot_reply_handler)


# --- Enable ---
@bot.message_handler(commands=["enable"], func=time_filter)
@error_handler
def enable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = True
    if language_code == "ru":
        bot.send_sticker(message.chat.id, stickers["enable"])
    bot.reply_to(message, templates[language_code]["enabled.txt"], parse_mode="HTML")


# --- Disable ---
@bot.message_handler(commands=["disable"], func=time_filter)
@error_handler
def disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = False

    bot.send_message(message.chat.id, templates[language_code]["disabled.txt"])


# --- Dialog mode enable ---
@bot.message_handler(commands=["enable_dialog"], func=time_filter)
@error_handler
def dialog_enable_command(message):
    if groups[message.chat.id].enabled == False:
        bot.reply_to(
            message, "You bot is disbaled.\n/enable to activate him", parse_mode="HTML"
        )

    else:
        language_code = groups[message.chat.id].lang_code
        groups[message.chat.id].trigger_probability = 1

        bot.reply_to(message, templates[language_code]["dialog_enabled.txt"])


# --- Dialog mode disable ---
@bot.message_handler(commands=["disable_dialog"], func=time_filter)
@error_handler
def dialog_disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].trigger_probability = 0.2

    bot.reply_to(message, templates[language_code]["dialog_disabled.txt"])


# --- Manual mode enable ---
@bot.message_handler(commands=["enable_manual"], func=time_filter)
@error_handler
def manual_enable_command(message):
    if groups[message.chat.id].enabled == False:
        bot.reply_to(
            message, "You bot is disbaled.\n/enable to activate him", parse_mode="HTML"
        )

    else:
        language_code = groups[message.chat.id].lang_code
        groups[message.chat.id].trigger_probability = 0
        bot.reply_to(
            message, templates[language_code]["manual_enabled.txt"], parse_mode="HTML"
        )


# --- Manual mode disable ---
@bot.message_handler(commands=["disable_manual"], func=time_filter)
@error_handler
def manual_disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].trigger_probability = 0.2

    bot.reply_to(message, templates[language_code]["manual_disabled.txt"])


# --- Clean memory ---
@bot.message_handler(commands=["clean_memory"], func=time_filter)
@error_handler
def clean_memory_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].messages_history = []
    bot.reply_to(message, templates[language_code]["memory_reset.txt"])


# --- Change language ---
@bot.message_handler(commands=["change_language"], func=time_filter)
@error_handler
def change_language_command(message):
    change_language(message.chat.id)


# --- Commands list ---
@bot.message_handler(commands=["commands"], func=time_filter)
@error_handler
def change_language_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id, templates[language_code]["commands.txt"], parse_mode="HTML"
    )


def change_language(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="ru"))
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="en"))
    keyboard.add(types.InlineKeyboardButton(text="Deutsch", callback_data="de"))
    keyboard.add(types.InlineKeyboardButton(text="Español", callback_data="es"))
    bot.send_message(chat_id, "Choose language", reply_markup=keyboard)


# --- callback handler ---
@bot.callback_query_handler(
    func=lambda call: call.data == "ru"
    or call.data == "en"
    or call.data == "de"
    or call.data == "es"
)
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
    elif call.data == "es":
        groups[call.message.chat.id].lang_code = "es"
        bot.send_message(call.message.chat.id, "Ahora en el Bazar nativo")
        language_code = "es"
    elif call.data == "de":
        groups[call.message.chat.id].lang_code = "de"
        bot.send_message(call.message.chat.id, "Jetzt auf dem Heimatmarkt")
        language_code = "de"

    if not previous_lang:
        send_welcome_text_and_load_data(call.message.chat.id, language_code)


def send_welcome_text_and_load_data(chat_id: int, language_code: str = "en") -> None:
    """Sends initialization messages to group and loads data in group's object

    Args:
        chat_id (int)
    """
    bot.send_message(chat_id, templates[language_code]["new_group_welcome.txt"])
    bot.send_message(chat_id, templates[language_code]["initialization.txt"])
    if language_code == "ru":
        send_sticker(chat_id, stickers["initializing"], bot)

    groups[chat_id].load_data()

    bot.send_message(
        chat_id,
        templates[language_code]["done_initializing.txt"],
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
            "You haven't set the language. English sets by default.\nUse /change_language for changing language",
        )
        send_welcome_text_and_load_data(chat_id)

    else:
        
        if type == 'private':
            with open(
                f"clients_info\\{bot.get_chat(chat_id).title}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(convert_to_json(str(bot.get_chat(chat_id))))
        else:
            with open(
                f"groups_info\\{bot.get_chat(chat_id).title}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(convert_to_json(str(bot.get_chat(chat_id))))

        groups[chat_id] = Johnny(bot, chat_id, str(bot_username))

        blacklist[chat_id] = []
        reply_blacklist[chat_id] = []

        logger.info(f"Bot initialized in new group (id: {chat_id})")
        change_language(chat_id)


@bot.message_handler(
    func=lambda message: reply_blacklist_filter(message)
    and blacklist_filter(message)
    and time_filter(message)
)
@error_handler
def main_messages_handler(message):
    """Handles all messages"""
    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)
    else:
        threading.Thread(
            target=groups[message.chat.id].new_message, args=(message,)
        ).start()
        logger.info(
            f"Created new thread for handling message, now threads running: {threading.active_count()}"
        )


logger.info("Bot started")
bot.polling()
