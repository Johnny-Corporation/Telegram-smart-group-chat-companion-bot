from telebot import TeleBot
from os import environ

tg_key = environ.get("OPENAI_API_KEY")
bot = TeleBot(tg_key)
bot_id = bot.get_me().id


@bot.message_handler(commands=["start"])
def about_command(message):
    print(message.text)
    bot.reply_to(message, "nococoocb")


bot.polling()
