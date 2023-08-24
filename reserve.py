from os import environ, listdir, path
import json

# Bot API
from telebot import TeleBot, types


from dotenv import load_dotenv


load_dotenv(".env")

crash_message = "Apologies, bot down for maintenance"

bot_token = environ.get("BOT_API_TOKEN")

bot = TeleBot(bot_token)


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_button = types.KeyboardButton("Bot is temporarily unavailable")
markup.add(run_button)


file_list = listdir("output/clients_info")
for filename in file_list:
    file_path = path.join("output/clients_info", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        bot.send_message(json.load(file)["id"], crash_message, reply_markup=markup)

file_list = listdir("output/groups_info")
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
        bot.reply_to(
            message,
            "Bot is temporarily unavailable",
            reply_markup=markup,
        )
        return


bot.polling()
