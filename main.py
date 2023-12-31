# ---------------  Imports ---------------
from os import environ, makedirs, path, remove, path
from shutil import copytree

from functools import wraps

makedirs("output//", exist_ok=True)

# Bot API
from telebot import TeleBot, types
from telebot.apihelper import ApiTelegramException

# Local modules
groups = {}  # {group chat_id:Johnny object}
survey_results = {}  # option: [ [id,username] ]
already_pressed_survey = []  # list of ids which take part in survey
from Johnny import Johnny
from utils.internet_access import *
from utils.functions import *
from utils.logger import logger
from utils.gpt_interface import *

# Other
from dotenv import load_dotenv
import traceback
from datetime import datetime
from time import sleep
import threading
from typing import Dict
import string
from random import choice

from utils.time_tracking import *

sub_pro_promocode = generate_code()
discount_on_sub_50 = generate_code()
discount_on_sub_20 = generate_code()
discount_for_public = "JOHNNY"
promocode_100 = generate_code()
promocodes = {'sub': sub_pro_promocode, 'discount_50_subscription': discount_for_public, 'messages_100': promocode_100}

# --------------- Initialization ---------------

load_dotenv(".env")

# Needed for filtering messages when bot was offline
start_time = datetime.now()
skip_old_messages = True  # True until message older than bot start time received
ignored_messages = 0  # count number of ignored messages when bot was offline for logs


bot_token = environ.get("BOT_API_TOKEN")

yoomoney_token = environ.get("PAYMENT_RUS_TOKEN")

commercial_links = {"greenlightInv": 10}  # Link: num_of_messages for it

developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")
if not bot_token:
    logger.error("Failed to load BOT_API_TOKEN from environment, exiting...")
    exit()
if not developer_chat_IDs:
    logger.warning("Developers chat ids is not set!")
else:
    developer_chat_IDs = developer_chat_IDs.split(",")


templates = load_templates("templates\\")
blacklist = {}  # chat_id:[messages_ids] needed for filtering messages
reply_blacklist = {}  # chat_id:[messages_ids] needed for filtering replies to messages
messages_to_be_deleted_global = []

if path.exists("output"):
    makedirs("outputs_archive", exist_ok=True)
    copytree(
        "output",
        f"outputs_archive\\output_{str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')}",
    )

makedirs("output\\groups_info", exist_ok=True)
makedirs("output\\clients_info", exist_ok=True)
makedirs("output\\files", exist_ok=True)
makedirs("output\\files\\DALLE", exist_ok=True)
makedirs("output\\files\\KANDINKSY", exist_ok=True)
makedirs("temp\\", exist_ok=True)
makedirs("outputs_archive\\", exist_ok=True)

bot = TeleBot(bot_token)
bot_id = bot.get_me().id
bot_username = bot.get_me().username


# Sending message bot is online again after restart!

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_button = types.KeyboardButton("Start")
markup.input_field_placeholder = "🚀"
markup.add(run_button)

first_message = ""  # input(
#     "Enter message to send users who were using bot, if Johnny notified them that he fall, its better to send something to notify them that it is working now, press Enter to do not send anything: "
# )

remembered_chats_ids = []


file_list = listdir("output/clients_info")
for filename in file_list:
    file_path = path.join("output/clients_info", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        try:  # If this user blocked bot
            id_ = json.load(file)["id"]
            if first_message:
                bot.send_message(id_, first_message, reply_markup=markup)
            remembered_chats_ids.append(str(id_))
        except:
            pass
file_list = listdir("output/groups_info")
for filename in file_list:
    file_path = path.join("output/groups_info", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        chat_id = int(content[6 : content.index(",")])
        try:  # If this user blocked bot
            if first_message:
                bot.send_message(
                    chat_id,
                    first_message,
                    reply_markup=markup,
                )
            remembered_chats_ids.append(str(chat_id))
        except:
            pass


def delete_pending_messages():
    for m in messages_to_be_deleted_global:
        bot.delete_message(m.chat.id, m.message_id)
        messages_to_be_deleted_global.remove(m)


# --------------- Error handling ---------------
errors_details = {}  # message_id:text
errors_previews = {}  # message_id:text


def error_handler(args):
    """Handles all occurred errors, logs them, sends error and logs.log to developers

    Args:
        func (function)
    """

    def wrapper(message: types.Message):
        try:
            args(message)
            if (hasattr(message, "text")) and message.text == "ERROR":
                0 / 0
        except KeyError:
            pass
        except Exception:
            chat_id = (
                message.chat.id
                if isinstance(message, types.Message)
                else message.message.chat.id
            )
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            close_btn_markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text=templates[groups[message.chat.id].lang_code]["button_close.txt"],
                callback_data="close_message",
            )
            close_btn_markup.add(button1)
            bot.send_message(
                chat_id,
                templates[groups[message.chat.id].lang_code]["error_occured.txt"],
                parse_mode="html",
                reply_markup=close_btn_markup,
            )
            expand_error_btn_markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text="Show details",
                callback_data="get_error_details",
            )
            expand_error_btn_markup.add(button1)
            msgs = send_to_developers(
                templates["en"]["dev_error_report.txt"].format(
                    fn=groups[chat_id].fn,
                    un=groups[chat_id].username,
                    ln=groups[chat_id].ln,
                ),
                bot,
                developer_chat_IDs,
                reply_markup=expand_error_btn_markup,
            )
            for m in msgs:
                errors_details[m.message_id] = traceback.format_exc()
                errors_previews[m.message_id] = templates["en"][
                    "dev_error_report.txt"
                ].format(
                    fn=groups[chat_id].fn,
                    un=groups[chat_id].username,
                    ln=groups[chat_id].ln,
                )
        else:
            if isinstance(message, list):
                return
            if isinstance(message, types.CallbackQuery):
                logger.info("Callback query processed without errors")

            elif message.content_type == "voice":
                logger.info(
                    f"Voice message executed in chat with id {message.chat.id} by user with id {message.from_user.id}"
                )
            elif message.content_type == "video_note":
                logger.info(
                    f"Video note executed in chat with id {message.chat.id} by user with id {message.from_user.id}"
                )
            else:
                logger.info(
                    f'Message "{message.text}" sent in chat with id {message.chat.id} by user with id {message.from_user.id}'
                )

    if callable(args):
        return wrapper
    else:
        chat_id = args.thread.chat_id
        logger.error(f"Unexpected error: {traceback.format_exc()}")
        close_btn_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text=templates[groups[chat_id].lang_code]["button_close.txt"],
            callback_data="close_message",
        )
        close_btn_markup.add(button1)
        bot.send_message(
            chat_id,
            templates[groups[chat_id].lang_code]["error_occured.txt"],
            reply_markup=close_btn_markup,
            parse_mode="html",
        )
        expand_error_btn_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            text="Show details",
            callback_data="get_error_details",
        )
        expand_error_btn_markup.add(button1)
        msgs = send_to_developers(
            templates["en"]["dev_error_report.txt"].format(
                fn=groups[chat_id].fn,
                un=groups[chat_id].username,
                ln=groups[chat_id].ln,
            ),
            bot,
            developer_chat_IDs,
            reply_markup=expand_error_btn_markup,
        )
        for m in msgs:
            errors_details[m.message_id] = traceback.format_exc()
            errors_previews[m.message_id] = templates["en"][
                "dev_error_report.txt"
            ].format(
                fn=groups[chat_id].fn,
                un=groups[chat_id].username,
                ln=groups[chat_id].ln,
            )


threading.excepthook = error_handler

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


def change_language(chat_id, message_id=None):
    avaible_languages = get_avaible_langs()

    keyboard = types.InlineKeyboardMarkup()
    # Got avaible languages
    with open("utils\\flags.json", "r", encoding="utf-8") as flags:
        flags_languages = json.load(flags)
    for lang_code in avaible_languages:
        lang = check_language(lang_code)
        keyboard.add(
            types.InlineKeyboardButton(
                text=flags_languages[lang[0]]
                + " "
                + translate_text(lang[0], lang[1].capitalize()),
                callback_data=f"{lang[1]}-apply_lang",
            )
        )  # lang[0] = language_code, lang[1] = full name of lang

    if message_id != None:
        keyboard.add(
            types.InlineKeyboardButton(
                text="<<<",
                callback_data="settings",
            )
        )
        bot.edit_message_text(
            "Choose language", chat_id, message_id, reply_markup=keyboard
        )
        return

    bot.send_message(chat_id, "Choose language", reply_markup=keyboard)


def send_welcome_text_and_load_data(
    message, chat_id: int, owner_id: int, language_code: str = "en"
) -> None:
    if owner_id not in groups:
        bot.send_message(
            chat_id,
            templates[language_code]["register_in_bot.txt"].format(
                bot_username=bot_username
            ),
        )
        return

    chat_member = bot.get_chat_member(chat_id, bot_id)
    if chat_member.status != "administrator" and chat_id < 0:
        bot.send_message(chat_id, templates[language_code]["group_admin_rights.txt"])
        return

    groups[chat_id].activated = True

    ("REGISTRATION IS GOING")

    # Load messages
    groups[chat_id].load_data()

    groups[chat_id].commercial_links = commercial_links

    if chat_id > 0:
        groups[chat_id].enabled = True
        groups[chat_id].trigger_probability = 1

    # User
    if chat_id > 0:
        # Try to get info from database
        sub_exist = groups[chat_id].load_subscription(chat_id)

        # If there isn't data, registries new user
        if not sub_exist:
            new_user = True

            chat_info = bot.get_chat(chat_id)
            firstname = chat_info.first_name
            lastname = chat_info.last_name
            username = chat_info.username

            groups[chat_id].add_new_user(
                chat_id, firstname, lastname, username, "Free", 10
            )
            groups[chat_id].load_subscription(chat_id)

        else:
            # Turn on the time-tracker of subscription (if user bought ut before)
            groups[chat_id].track_sub(
                chat_id, new=False
            )  # If user have free plan - in track_sub it considering
            new_user = False

    # For group/chat
    else:
        # Load info to group from loader of group (owner_id)
        groups[chat_id].characteristics_of_sub = {}

        groups[chat_id].subscription = groups[owner_id].subscription

        characteristics_of_sub = take_info_about_sub(groups[owner_id].subscription)
        groups[chat_id].characteristics_of_sub[
            groups[owner_id].subscription
        ] = characteristics_of_sub

        groups[chat_id].owner_id = owner_id

        # Add to owner's data info about him group
        groups[owner_id].id_groups.append(chat_id)

        permissions = {
            "change_model": True,
            "bot_answers": True,
            "sphere": True,
            "change_lang": True,
            "special_features": True,
            "choose_inline_mode": True,
            "change_owner": True,
        }
        groups[owner_id].permissions_of_groups[chat_id] = permissions

    # if groups[chat_id].subscription == "Pro":
    groups[chat_id].dynamic_gen = True

    # Load buttons
    markup = load_buttons(
        types, groups, chat_id, language_code, owner_id=groups[chat_id].owner_id
    )

    # Welcome text for group and user
    if chat_id > 0:
        groups[chat_id].trigger_probability = 1
        if str(chat_id) not in developer_chat_IDs:
            bot.send_message(
                chat_id,
                groups[chat_id].templates[language_code]["new_user_welcome.txt"],
                reply_markup=markup,
                parse_mode="HTML",
            )

    else:
        bot.send_message(
            chat_id,
            groups[chat_id].templates[language_code]["new_group_welcome.txt"],
            reply_markup=markup,
            parse_mode="HTML",
        )

    if chat_id > 0:
        if str(chat_id) in developer_chat_IDs:
            bot.send_message(
                chat_id,
                f"As a developer, you granted Pro sub\n {'='*20} \n Как разработчику, вам выдана подписка Pro",
                reply_markup=markup,
            )
            chat_info = bot.get_chat(chat_id)
            firstname = chat_info.first_name
            lastname = chat_info.last_name
            username = chat_info.username
            groups[message.chat.id].add_new_user(
                message.chat.id,
                firstname,
                lastname,
                username,
                "Pro",
                999,
            )
            groups[message.chat.id].load_subscription(message.chat.id)
            if groups[chat_id].subscription == "Pro":
                groups[chat_id].dynamic_gen = True
            return


# ---------------  Handling and initialing new groups ---------------


@bot.message_handler(content_types=["new_chat_members"], func=time_filter)
def handle_new_chat_members(message):
    for new_chat_member in message.new_chat_members:
        if new_chat_member.id == bot_id:
            bot.send_message(
                message.chat.id,
                f"Write a message to start",
            )

    try:
        remove(f"output\\groups_info\\{clean_string(message.chat.title)}.json")
        groups.pop(message.chat.id)
        groups[message.from_user.id].id_groups.remove(message.chat.id)
    except:
        None


@bot.message_handler(content_types=["migrate_to_chat_id"], func=time_filter)
def handle_migrate_group_to_supergroup(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["group_upgraded_to_super_group.txt"],
        parse_mode="Markdown",
    )


def init_new_group(chat_id, inviting=False, referrer_id=None):
    if chat_id in groups:
        return  # Lang code not set
    else:
        chat = bot.get_chat(chat_id)
        if chat_id > 0:  # private
            last_name = chat.last_name
            if chat.last_name == None:
                last_name = "None"
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
        groups[chat_id].templates = load_templates("templates\\")

        if inviting:
            # Bonuses to invited men
            groups[chat_id].referrer_id = referrer_id
            groups[chat_id].invited = True
            groups[chat_id].discount_subscription["Referral discount"] = 0.8

        blacklist[chat_id] = []
        reply_blacklist[chat_id] = []

        logger.info(f"Bot initialized in new group (id: {chat_id})")

        change_language(chat_id)


# --------------- Commands ---------------

# Reply handlers (important to import them before commands, because commands are using them)
from commands.reply_handlers.add_commercial_link import *
from commands.reply_handlers.dev_tool_add_promocode import *
from commands.reply_handlers.settings_change_language import *
from commands.reply_handlers.bug_report import *
from commands.reply_handlers.feature_request import *
from commands.reply_handlers.purchase_enter_new_messages import *
from commands.reply_handlers.purchase_enter_promocode import *
from commands.reply_handlers.purchase_support_us import *
from commands.reply_handlers.question_to_bot import *
from commands.reply_handlers.settings_bot_answers import *
from commands.reply_handlers.settings_change_owner import *
from commands.reply_handlers.gen_img_prompt import *

# Commands
from commands.inline_additional_settings import *
from commands.inline_handler import *
from commands.view_model import *
from commands.models_switcher import *
from commands.get_chat_id import *
from commands.about import *
from commands.account_referral import *
from commands.account import *
from commands.bot_on_view_mode import *
from commands.bot_on_change_mode_command import *
from commands.clean_memory import *
from commands.converts import *
from commands.dev_tools import *
from commands.enable_disable import *
from commands.group import *
from commands.load import *
from commands.other import *
from commands.purchase_commercial import *
from commands.purchase_enter_promocode import *
from commands.purchase_extend_sub import *
from commands.purchase_pay_subscription import *
from commands.purchase_pay_messages import *
from commands.purchase_support_us import *
from commands.purchase_update_sub import *
from commands.purchase import *
from commands.question_to_bot import *
from commands.report_bug import *
from commands.request_feature import *
from commands.settings import *
from commands.settings_change_language import *
from commands.settings_bot_answers import *
from commands.settings_change_owner_of_group import *
from commands.settings_special_features import *
from commands.settings_change_permissions import *
from commands.about import *
from commands.start import *
from commands.subs_list import *
from commands.tranzzo import *
from commands.menu import *
from commands.ask_gen_image_prompt import *
from commands.choose_inline_mode import *

# Buttons handler
from commands.buttons_handler import *
from commands.commands_handler import *

# Payment handler (need be there)
from utils.yoomoney import *
from utils.text_to_voice import *

# --------------- Main messages handler ---------------


@bot.message_handler(
    content_types=[
        "text",
        "audio",
        "document",
        "photo",
        "sticker",
        "video",
        "video_note",
        "voice",
        "location",
    ],
    func=lambda message: reply_blacklist_filter(message)
    and blacklist_filter(message)
    and time_filter(message),
)
@error_handler
def main_messages_handler(message: types.Message):
    """Handles all messages"""

    # chat_member = bot.get_chat_member(message.chat.id, bot.get_me().id)
    # if chat_member.status == "kicked":
    #     return

    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)

    else:
        # Check for existing of buttons
        try:
            groups[message.chat.id].button_commands[-1]
        except:
            return

        # Checks the command of ReplyButtons
        if message.text in groups[message.chat.id].button_commands:
            button_on = reply_keyboard_buttons_handler(
                message, groups[message.chat.id].button_commands
            )
            return

        # Checks the registration of user
        if groups[message.chat.id].activated == False:
            return

        new_thread = threading.Thread(
            target=groups[message.chat.id].new_message, args=(message, groups)
        )
        new_thread.chat_id = message.chat.id
        new_thread.start()
        logger.info(
            f"Created new thread for handling message, now threads running: {threading.active_count()}, some of which are system"
        )


# --------------- Running ---------------

logger.info(" ---->>>> BOT STARTED <<<<---- ")
bot.infinity_polling(timeout=500)
