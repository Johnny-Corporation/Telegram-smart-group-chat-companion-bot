
from telebot import TeleBot

tg_key = '6142647841:AAHAEEgJLuJo2YseI4UPL4G9_bunrboMjO0'
bot = TeleBot(tg_key)
bot_id = bot.get_me().id


@bot.message_handler(commands=["start"])
def about_command(message):
    print(message.text)
    bot.reply_to(message, 'nococoocb')


bot.polling()