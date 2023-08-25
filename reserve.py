from os import environ, listdir, path, _exit, makedirs, path, walk
import json
from shutil import copytree, move
from utils.db_controller import Controller
from datetime import datetime
import zipfile

# Bot API
from telebot import TeleBot, types


from dotenv import load_dotenv


load_dotenv(".env")

crash_message = "Apologies, bot down for maintenance"

bot_token = environ.get("BOT_API_TOKEN")

bot = TeleBot(bot_token)

developer_chat_ids = environ["DEVELOPER_CHAT_IDS"]

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
dev_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_button = types.KeyboardButton("Bot is temporarily unavailable")
dev_tools_button = types.KeyboardButton("/dev_tools")
markup.add(run_button)
dev_markup.add(run_button)
dev_markup.add(dev_tools_button)


def create_archive(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for folder_root, _, files in walk(folder_path):
            for file in files:
                file_path = path.join(folder_root, file)
                archive_path = path.relpath(file_path, folder_path)
                archive.write(file_path, archive_path)


def send_file(path: str, id: int, bot) -> None:
    """Sends a file to chat

    Args:
        path (str): path to file
        id (int): chat id
        bot (_type_): TeleBot object
    """
    with open(path, "rb") as file:
        bot.send_document(id, file)


if not path.exists("output"):
    makedirs("output\\groups_info", exist_ok=True)
    makedirs("output\\clients_info", exist_ok=True)
    makedirs("output\\files", exist_ok=True)
    makedirs("output\\files\\DALLE", exist_ok=True)
    makedirs("temp\\", exist_ok=True)
    makedirs("outputs_archive\\", exist_ok=True)
file_list = listdir("output\\clients_info")
for filename in file_list:
    file_path = path.join("output/clients_info", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        if str(chat_id := json.load(file)["id"]) in developer_chat_ids:
            if path.exists("temp\\error.txt"):
                send_file("temp\\error.txt", chat_id, bot)
            bot.send_message(chat_id, crash_message, reply_markup=dev_markup)
        else:
            bot.send_message(chat_id, crash_message, reply_markup=markup)

file_list = listdir("output\\groups_info")
for filename in file_list:
    file_path = path.join("output/groups_info", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        chat_id = int(content[6 : content.index(",")])
        bot.send_message(
            chat_id,
            crash_message,
            reply_markup=markup,
        )


@bot.message_handler(commands=["dev_tools"])
def start(message):
    if str(message.chat.id) not in developer_chat_ids:
        bot.reply_to(message, "ACCESS DENIED")
        bot.reply_to(message, "🖕🏿")
        return
    chat_id = message.chat.id
    dev_tools_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    button1 = types.InlineKeyboardButton(
        text="Move current output to archive",
        callback_data="move_out",
    )
    dev_tools_markup.add(button1)
    button1 = types.InlineKeyboardButton(
        text="Kill bot ",
        callback_data="kill_bot",
    )
    dev_tools_markup.add(button1)
    # --------------------------------------
    button = types.InlineKeyboardButton(
        text="Get logs",
        callback_data="get_logs",
    )
    dev_tools_markup.add(button)
    # --------------------------------------
    button1 = types.InlineKeyboardButton(
        text="Get user",
        callback_data="get_user",
    )
    button2 = types.InlineKeyboardButton(
        text="Get group",
        callback_data="get_group",
    )
    dev_tools_markup.add(button1, button2)
    # --------------------------------------
    button = types.InlineKeyboardButton(
        text="Database file",
        callback_data="get_db_file",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get current output",
        callback_data="get_cur_out",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get all archived outputs",
        callback_data="get_all_outs",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Add current output to archive",
        callback_data="copy_cur_out_to_archive",
    )
    dev_tools_markup.add(button)
    # Sending keyboard
    bot.send_message(
        chat_id,
        "----- DEVELOPER TOOLS -----",
        reply_markup=dev_tools_markup,
        parse_mode="HTML",
    )


@bot.callback_query_handler(func=lambda call: True)
def keyboard_buttons_handler(call):
    global bot
    call_data = call.data
    match call_data:
        case "get_cur_out":
            create_archive("output", "temp\\output.zip")
            send_file("temp\\output.zip", call.message.chat.id, bot)
        case "get_all_outs":
            create_archive("outputs_archive", "temp\\outputs_archive.zip")
            send_file("temp\\outputs_archive.zip", call.message.chat.id, bot)
        case "move_out":
            bot.reply_to(
                call.message,
                ">>> Current output was moved to archive, in root new directory will be created.",
            )
            move(
                "output",
                f"outputs_archive\\output_{str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')}",
            )
            makedirs("output\\groups_info", exist_ok=True)
            makedirs("output\\clients_info", exist_ok=True)
            makedirs("output\\files", exist_ok=True)
            makedirs("output\\files\\DALLE", exist_ok=True)
            makedirs("temp\\", exist_ok=True)
            makedirs("outputs_archive\\", exist_ok=True)
        case "kill_bot":
            bot.reply_to(call.message, "😵")
            _exit(0)
        case "get_logs":
            send_file("output/info_logs.log", call.message.chat.id, bot)
            send_file("output/debug_logs.log", call.message.chat.id, bot)
        case "copy_cur_out_to_archive":
            copytree(
                "output",
                f"outputs_archive\\output_{str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')}",
            )
            bot.reply_to(call.message, "✅")

        case "get_user":
            get_user_info(call.message)
        case "get_group":
            get_group_info(call.message)
        case "get_db_file":
            send_file("output/DB.sqlite", call.message.chat.id, bot)


@bot.message_handler(content_types=["text"], func=lambda message: True)
def main_messages_handler(message: types.Message):
    """Handles all messages"""

    if "@SmartGroupParticipant_bot" in message.text:
        bot.reply_to(
            message,
            "Bot is temporarily unavailable",
            reply_markup=markup,
        )
        return
    if message.chat.type == "private":
        if str(message.chat.id) in developer_chat_ids:
            bot.reply_to(
                message,
                "Bot is temporarily unavailable",
                reply_markup=dev_markup,
            )
        else:
            bot.reply_to(
                message,
                "Bot is temporarily unavailable",
                reply_markup=markup,
            )
        return


bot.polling()


controller = Controller()
# ----------------------- Functions for devtools -----------------------


def get_user_info(message):
    users_list = listdir("output\\clients_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(
        message,
        "Choose and reply " + f"\n {users}",
    )
    bot.register_for_reply(bot_reply, get_user_info_reply_handler)


def get_user_info_reply_handler(inner_message):
    path = (
        "output\\clients_info\\"
        + listdir("output\\clients_info")[int(inner_message.text)]
    )
    send_file(
        path,
        inner_message.chat.id,
        bot,
    )
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # between : and ,
        group_id = int(content.split(",")[0].replace('{"id":', ""))
    with open("temp\\messages_history_client.txt", "w", encoding="utf-8") as f:
        f.write("[START]\n")
        for i in controller.get_last_n_messages_from_chat(
            n=999999999, chat_id=group_id
        )[::-1]:
            print(i)
            f.write(f"{i[0]}  = = = {i[1]}" + "\n")
        f.write("[END]")

    send_file(
        "temp\\messages_history_client.txt",
        inner_message.chat.id,
        bot,
    )


def get_group_info(message):
    users_list = listdir("output\\groups_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(
        message,
        "Choose and reply" + f"\n {users}",
    )
    bot.register_for_reply(bot_reply, get_group_info_reply_handler)


def get_group_info_reply_handler(inner_message):
    path = (
        "output\\groups_info\\"
        + listdir("output\\groups_info")[int(inner_message.text)]
    )
    send_file(
        path,
        inner_message.chat.id,
        bot,
    )
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # between : and ,
        group_id = int(content.split(",")[0].replace('{"id":', ""))
    with open("temp\\messages_history_group.txt", "w", encoding="utf-8") as f:
        f.write("[START]\n")
        for i in controller.get_last_n_messages_from_chat(
            n=999999999, chat_id=group_id
        )[::-1]:
            print(i)
            f.write(f"{i[0]}  = = = {i[1]}" + "\n")
        f.write("[END]")

    send_file(
        "temp\\messages_history_group.txt",
        inner_message.chat.id,
        bot,
    )
