# GPT API
import openai

# Bot API
from telebot import TeleBot

# Local modules
from templates_loader import load_templates
from Johnny import Johnny
from internet_access import *

# Other
from dotenv import load_dotenv
from os import environ
import logging
import traceback
import json  # groups.json write groups in file !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

openai.api_key = openAI_api_key


def tokens_to_dollars(model, tokens):
    return "Not implemented"


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
                f"Error occurred!!!: \n -----------\n {traceback.format_exc()}\n ---------- "
            )
            send_to_developers("logs.log", file=True)
        else:
            logger.info(
                f"Command {message.text} executed in chat with id {message.chat.id}"
            )
            # log gpt responses

    return wrapper


def send_file(path, id):
    with open(path, "rb") as file:
        bot.send_document(id, file)


def send_to_developers(msg, file=False):
    for id in developer_chat_IDs:
        if id:
            if file:
                send_file(msg, id)
            else:
                bot.send_message(
                    id,
                    msg,
                )


# --- Help ---
@bot.message_handler(commands=["help"])
@error_handler
def error_command(message):
    bot.reply_to(
        message, templates["help.txt"]
    )  # finish here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"])
@error_handler
def tokens_info_command(message):
    # bot.reply_to(message, templates["help.txt"])
    bot.reply_to(message, "Not implemented")


# --- About ---
@bot.message_handler(commands=["about", "start"])
@error_handler
def about_command(message):
    bot.reply_to(message, templates["description.txt"])


# --- Report bug ---
@bot.message_handler(commands=["report_bug"])
@error_handler
def report_bug_command(message):
    bot.reply_to(message, templates["report_bug.txt"])


# --- Request feature ---
@bot.message_handler(commands=["request_feature"])
@error_handler
def request_feature_command(message):
    bot.reply_to(message, templates["request_feature"])


# --- Enable ---
@bot.message_handler(commands=["enable"])
@error_handler
def enable_command(message):
    # logic
    bot.reply_to(message, templates["enabled.txt"])


# --- Disable ---
@bot.message_handler(commands=["disable"])
@error_handler
def handle_start(message):
    # logic
    bot.reply_to(message, templates["disabled.txt"])


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
                message.chat.id, "Initializing..."
            )  # Will be replaced with sticker


logger.info("Bot started")
bot.polling()
