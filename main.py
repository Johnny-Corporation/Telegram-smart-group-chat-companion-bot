# ---------------  Imports ---------------
from os import environ, path, mkdir, execl
from sys import argv, executable

if not path.exists("output"):
    mkdir("output")

# Bot API
from telebot import TeleBot, types

# Local modules
from Johnny import Johnny
from utils.internet_access import *
from utils.functions import *
from utils.logger import logger

# Other
from dotenv import load_dotenv
import traceback
from datetime import datetime
import threading
from typing import Dict


# --------------- Initialization ---------------


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

if not path.exists("output\\groups_info"):
    mkdir("output\\groups_info")

if not path.exists("output\\clients_info"):
    mkdir("output\\clients_info")


bot = TeleBot(bot_token)
bot_id = bot.get_me().id
bot_username = bot.get_me().username

# Init quick access keyboard
keyboard = types.ReplyKeyboardMarkup()
keyboard.add(
    *[types.KeyboardButton(text="/enable"), types.KeyboardButton(text="/disable")]
)


# --------------- Error handling ---------------


def error_handler(func):
    """Handles all occurred errors, logs them, sends error and logs.log to developers

    Args:
        func (function)
    """

    def wrapper(message: types.Message):
        try:
            func(message)
        except KeyError:
            chat_id = (
                message.chat.id
                if isinstance(message, types.Message)
                else message.message.chat.id
            )

            bot.send_message(
                chat_id,
                "Sorry, bot was restarted. Your data saved!",
            )
            init_new_group(chat_id)
        except Exception:
            chat_id = (
                message.chat.id
                if isinstance(message, types.Message)
                else message.message.chat.id
            )
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            bot.send_message(
                chat_id,
                "Sorry, unexpected error occurred, developers have been already notified!",
            )
            send_to_developers(
                f"Error occurred!!!: \n -----------\n {traceback.format_exc()}\n ---------- ",
                bot,
                developer_chat_IDs,
            )
            send_to_developers(
                "output\\debug_logs.log", bot, developer_chat_IDs, file=True
            )
            send_to_developers(
                "output\\info_logs.log", bot, developer_chat_IDs, file=True
            )
        else:

            if isinstance(message, types.CallbackQuery):
                logger.info("Callback query processed without errors")
            elif (message.chat.id in groups) or message.text[0] == "/":  # command
                logger.info(
                    f'Command "{message.text}" executed in chat with id {message.chat.id}by user with id {message.from_user.id}'
                )
            else:
                logger.info(
                    f'Message "{message.text}" sent in chat with id {message.chat.id} by user with id {message.from_user.id}'
                )

    return wrapper


# --------------- Filters ---------------


def time_filter(message: types.Message):
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


def blacklist_filter(message: types.Message):
    "Filters message if its id in blacklist"
    if message.chat.id not in blacklist:
        return True
    return not (message.message_id in blacklist.get(message.chat.id))


def reply_blacklist_filter(message: types.Message):
    """Blocks message if it is a reply to message which is in reply_blacklist"""
    if message.chat.id not in blacklist:
        return True
    return (message.reply_to_message is None) or (
        message.reply_to_message.message_id not in reply_blacklist[message.chat.id]
    )


# --------------- Some functions ---------------


def change_language(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="ru"))
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="en"))
    # keyboard.add(types.InlineKeyboardButton(text="Deutsch", callback_data="de"))
    # keyboard.add(types.InlineKeyboardButton(text="Español", callback_data="es"))
    bot.send_message(chat_id, "Choose language", reply_markup=keyboard)


def send_welcome_text_and_load_data(chat_id: int, language_code: str = "en") -> None:
    """Sends initialization messages to group and loads data in group's object

    Args:
        chat_id (int)
    """


    if chat_id>0:
        bot.send_message(chat_id, templates[language_code]["new_user_welcome.txt"])
    else:
        bot.send_message(chat_id, templates[language_code]["new_group_welcome.txt"])

    bot.send_message(chat_id, templates[language_code]["initialization.txt"])
    if language_code == "ru":
        send_sticker(chat_id, stickers["initializing"], bot)

    groups[chat_id].load_data()

    bot.send_message(
        chat_id,
        templates[language_code]["done_initializing.txt"],
    )


# ---------------  Handling and initialing new groups ---------------


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
        chat = bot.get_chat(chat_id)
        if chat_id > 0:  # private
            last_name = chat.last_name
            if chat.last_name == None:
                last_name = 'None'
            with open(
                f"output\\clients_info\\{clean_string(chat.first_name)}-{last_name}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(convert_to_json(str(chat)))
        else:
            with open(
                f"output\\groups_info\\{clean_string(chat.title)}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(convert_to_json(str(chat)))

        groups[chat_id] = Johnny(bot, chat_id, str(bot_username))

        blacklist[chat_id] = []
        reply_blacklist[chat_id] = []

        logger.info(f"Bot initialized in new group (id: {chat_id})")

        change_language(chat_id)
        


# --------------- Commands ---------------

# Reply handlers (important to import them before commands, because commands are using them)
from commands.reply_handlers.feature_request import *
from commands.reply_handlers.bug_report import *
from commands.reply_handlers.question_to_bot import *
from commands.reply_handlers.set_temp import *
from commands.reply_handlers.frequency_penalty import *
from commands.reply_handlers.presense_penalty import *
from commands.reply_handlers.set_sphere import *
from commands.reply_handlers.temp_memory_size import *
from commands.reply_handlers.set_probability import *

# Commands
from commands.about import *
from commands.help import *
from commands.start import *
from commands.set_up_command import *
from commands.view_mode import *
from commands.tokens_info import *
from commands.dynamic_generation import *
from commands.set_temp import *
from commands.set_prob import *
from commands.set_memory_size import *
from commands.set_freq_penalty import *
from commands.set_sphere import *
from commands.set_answer_len import *
from commands.report_bug import *
from commands.request_feature import *
from commands.question_to_bot import *
from commands.enable_disable import *
from commands.dialog_mode_dis_en import *
from commands.manual_mode_en_dis import *
from commands.clean_memory import *
from commands.commands_list import *
from commands.group_info import *
from commands.change_lang import *
from commands.dev_tools import *

# Buttons handler
from commands.buttons_handler import *

# --------------- Main messages handler ---------------


@bot.message_handler(
    func=lambda message: reply_blacklist_filter(message)
    and blacklist_filter(message)
    and time_filter(message),
)
@error_handler
def main_messages_handler(message: types.Message):
    """Handles all messages"""
    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)
    else:
        threading.Thread(
            target=groups[message.chat.id].new_message, args=(message,)
        ).start()
        logger.info(
            f"Created new thread for handling message, now threads running: {threading.active_count()}, 4 of which are system"
        )


# --------------- Running ---------------

logger.info("Bot started")
bot.polling()
