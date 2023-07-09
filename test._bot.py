import telebot

TOKEN = "5918531073:AAF1q4o2WIkBuee4CTSc95XIWexUox9-Xw4"
bot = telebot.TeleBot(TOKEN)


# get_custom_emoji_stickers(custom_emoji_ids: List[str]) → List[Sticker]


@bot.message_handler(commands=["start"])
def send_welcome(message):
    # get_custom_emoji_stickers
    custom_emoji = "https://t.me/addemoji/CreepyEmoji"
    bot.send_message(message.chat.id, "AAAA")


@bot.message_handler(content_types="emoji")
def main_messages_handler(message):
    bot.send_message(message.chat.id, str(message.file.id))


bot.polling(none_stop=True)
