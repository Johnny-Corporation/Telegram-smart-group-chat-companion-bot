import telebot
from telebot import types

bot_token = "5918531073:AAF1q4o2WIkBuee4CTSc95XIWexUox9-Xw4"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Нажми меня", callback_data='b')
    button1 = types.InlineKeyboardButton(text="Нажми меня1", callback_data='a')
    button2 = types.InlineKeyboardButton(text="Нажми меня2", callback_data='c')
    markup.add(button)
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'a' or call.data == 'b')
def action(call):
    bot.send_message(call.message.chat.id, "Вы нажали на кнопку!")

@bot.callback_query_handler(func=lambda call: call.data == 'c')
def action(call):
    bot.send_message(call.message.chat.id, "Вы нажали на кнопку!1")

bot.polling()


