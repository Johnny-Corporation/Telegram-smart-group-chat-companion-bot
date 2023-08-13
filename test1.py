import telebot
import time
from telebot import types

bot = telebot.TeleBot('6386393540:AAEYh8-sCQdRL7nGabG7YV7_mnaFxss8p2U')

stop_count = 0

@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, f"Приветствую, <i>{message.from_user.first_name}</i>!\n \nЗдесь Вы можете выиграть <u>свидание-сюрприз!</u> Нужно лишь ответить <u>на пару вопросов!</u>" , parse_mode="HTML")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Да!')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Начнём?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):

    # --- Начало ---
    if message.text == 'Да!':
        bot.send_message(message.chat.id, "Начнём!")
        time.sleep(0.3)

    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Ну вы же понимаете, что вам всё равно придётся пройти через этот тест)")
        time.sleep(0.3)

    # --- Познакомимся? ---

    elif message.text == 'Нет?' or message.text == 'Неуверена, что нет' or message.text == 'Возможно нет' or message.text == 'НЕТ!!!':
        bot.send_message("Намёк я точно определённо не понял\n \nКак говорила одна прекрасная девушка: ")

    elif message.text == 'Я в телеграме не знакомлюсь':
        bot.send_message("Тогда нам и не придётся!")

    elif message.text == 'НЕТ!':
        bot.send_message("Ну на самом деле я итак всё знаю")
        time.sleep(0.3)
        bot.send_message("Почти")

    elif message.text == 'Вы кажется ошиблись':
        bot.send_message("Тогда нам и не придётся!")



    else:
        bot.send_message(message.chat.id, f"Отвечайте на вопрос, иначе же подарок достанется кому-то другому)\nУ вас осталось {3-stop_count} попыток.")
        stop_count = stop_count + 1


def first_question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn2 = types.KeyboardButton('Нет')
    itembtn1 = types.KeyboardButton('Нет?')
    itembtn4 = types.KeyboardButton('Неуверена, что нет')
    itembtn5 = types.KeyboardButton('Я в телеграме не знакомлюсь')
    itembtn6 = types.KeyboardButton('Ты не в моем вкусе')
    itembtn7 = types.KeyboardButton('Я сейчас занята')
    itembtn8 = types.KeyboardButton('Вы кажется ошиблись')
    itembtn3 = types.KeyboardButton('Возможно нет')
    itembtn15 = types.KeyboardButton('Отшить по-своему')  
    itembtn9 = types.KeyboardButton('Зачем так далеко листаешь?')
    itembtn10 = types.KeyboardButton('НЕТ!')
    itembtn11= types.KeyboardButton('НЕТ!!!')
    itembtn12= types.KeyboardButton('Ну попробуй')
    itembtn13= types.KeyboardButton('Ты итак знаешь, что меня зовут Ксения и мне 16')
    itembtn14= types.KeyboardButton('Ну давай')

    markup.add(itembtn1)
    markup.add(itembtn2)
    markup.add(itembtn4)
    markup.add(itembtn5)
    markup.add(itembtn6)
    markup.add(itembtn7)
    markup.add(itembtn8)
    markup.add(itembtn3)
    markup.add(itembtn15)
    markup.add(itembtn9)
    markup.add(itembtn10)
    markup.add(itembtn11)
    markup.add(itembtn12)
    markup.add(itembtn13)
    markup.add(itembtn14)

    bot.send_message(message.chat.id, "Познакомимся?", reply_markup=markup)






bot.polling(none_stop=True)
