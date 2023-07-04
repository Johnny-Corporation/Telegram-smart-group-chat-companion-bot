# GPT API
import openai

# Bot API
from telebot import TeleBot

# Local modules
from Johnny import Johnny
from internet_access import *
from functions import *

# Other
from dotenv import load_dotenv
from os import environ, path, mkdir
import logging
import traceback

load_dotenv(".env")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

bot_token = environ.get("BOT_API_TOKEN")
openAI_api_key = environ.get("OPENAI_API_KEY")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")
if not all((bot_token, openAI_api_key)):
    logger.error(
        "Failed to load OPENAI_API_KEY or BOT_API_TOKEN from environment, exiting..."
    )
    exit()
if not developer_chat_IDs:
    logger.warning("Developers chat ids is not set!")
else:
    developer_chat_IDs = developer_chat_IDs.split(",")

templates = load_templates("templates\\")
stickers = load_stickers("stickers.json")
language_code = "ru"

if not path.exists("groups_info"):
    mkdir("groups_info")

openai.api_key = openAI_api_key


bot = TeleBot(bot_token)
bot_id = bot.get_me().id


def error_handler(func):
    def wrapper(message):
        try:
            func(message)
        except Exception as e:
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            bot.send_message(
                message.chat.id,
                "Sorry, unexpected error occurred, developer has been already notified!",
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


# --- Help ---
@bot.message_handler(commands=["help"])
@error_handler
def error_command(message):
    bot.reply_to(message, templates[language_code]["help.txt"], parse_mode="Markdown")


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"])
@error_handler
def tokens_info_command(message):
    bot.reply_to(
        message,
        templates[language_code]["tokens.txt"].format(dollars=0, spent_tokens=0),
    )


# --- About ---
@bot.message_handler(commands=["about", "start"])
@error_handler
def about_command(message):
    bot.reply_to(message, templates[language_code]["description.txt"])


# --- reply handler for feature requests ---
@error_handler
def feature_request_reply_handler(inner_message):
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} ({user.username}) 
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
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} ({user.username}) 
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
@bot.message_handler(commands=["report_bug"])
@error_handler
def report_bug_command(message):
    bot_reply = bot.reply_to(message, templates[language_code]["report_bug.txt"])

    bot.register_for_reply(bot_reply, bug_report_reply_handler)


# --- Request feature ---
@bot.message_handler(commands=["request_feature"])
@error_handler
def request_feature_command(message):
    bot_reply = bot.reply_to(message, templates[language_code]["request_feature.txt"])

    bot.register_for_reply(bot_reply, feature_request_reply_handler)


# --- Enable ---
@bot.message_handler(commands=["enable"])
@error_handler
def enable_command(message):
    # logic
    if language_code == "en":
        return bot.reply_to(message, templates[language_code]["enabled.txt"])
    bot.send_sticker(message.chat.id, stickers["enable"])


# --- Disable ---
@bot.message_handler(commands=["disable"])
@error_handler
def handle_start(message):
    # logic
    bot.reply_to(message, templates[language_code]["disabled.txt"])


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"])
@error_handler
def set_temp_command(message):
    # logic (check val from 0 to 1!)
    bot.reply_to(message, "Not implemented")


# --- Handling new groups ---
@bot.message_handler(content_types=["new_chat_members"])
@error_handler
def handle_new_chat_members(message):
    for new_chat_member in message.new_chat_members:
        if new_chat_member.id == bot_id:
            bot.send_message(message.chat.id, templates["new_group_welcome.txt"])
            bot.send_message(
                message.chat.id,
                "Initializing..." if language_code == "en" else "Инициализация...",
            )  # Will be replaced with sticker
            with open(
                f"groups_info\\{bot.get_chat(message.chat.id).title}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(convert_to_json(str(bot.get_chat(message.chat.id))))


groups = {}  # {id:Johnny object}


# @bot.message_handler()
# def handle_sticker(message):
#     bot.reply_to
#     print(sticker_file_id)
#     # Use the sticker_file_id as needed


# check this with reply handling!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
logger.info("Bot started")
# add ability to change languages by language code suffix
# send sticker enabled
bot.polling()
