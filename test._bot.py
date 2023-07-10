import telebot
from telebot import types

bot_token = "5918531073:AAF1q4o2WIkBuee4CTSc95XIWexUox9-Xw4"
bot = telebot.TeleBot(bot_token)


# @bot.message_handler()
# def echo_all(message):
#     chat_type = message.chat.type  # Получаем тип чата

#     if chat_type == "private":
#         bot.reply_to(message, "Вы написали мне в личные сообщения.")
#     elif chat_type in ["group", "supergroup"]:
#         bot.reply_to(message, "Вы написали в групповом чате.")
#     else:
#         bot.reply_to(message, "Я не уверен, где вы мне написали.")


@bot.message_handler(
        func=lambda message: message.chat.type == 'private'
)
def handle_private_message(message):
    # Здесь ваш код для обработки личных сообщений
    bot.reply_to(message, "Это личное сообщение!")


@bot.message_handler(
    func=lambda message: message.chat.type in ["group", "supergroup"],
)
def echo_priv(message):
    bot.reply_to(message, "Ты в группе")


bot.polling()