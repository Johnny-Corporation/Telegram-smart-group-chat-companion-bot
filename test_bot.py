from telebot import TeleBot
from os import environ

tg_key = '6142647841:AAHAEEgJLuJo2YseI4UPL4G9_bunrboMjO0'
bot = TeleBot(tg_key)
bot_id = bot.get_me().id

# while messages[-1].find('/end') == -1:
#     None

@bot.message_handler(commands=["start"])
def about_command(message):
    bot.send_message(message.chat.id, "start")
    


messages = []
i = 0

@bot.message_handler(commands=["start_conservation"])
def about_command(message):

    full_message = message.text
    message_to_gpt = ''

    messages.append('/start')
    try:
        for i in range(full_message.index(' ')+1, len(full_message)):
            message_to_gpt = message_to_gpt + message[i]

        messages.append(message_to_gpt)
    except:
        None

    bot.send_message(message.chat.id, "start conservation")

@bot.message_handler(commands=["end_conservation"])
def about_command(message):
    bot.send_message(message.chat.id, "end conservation")
    messages.clear()
    

@bot.message_handler(content_types='text')
def about_command(message):
    print(messages)
    if '/start' in messages:
        bot.send_message(message.chat.id, "middle")
    else:
        bot.send_message(message.chat.id, 'out')


bot.polling()
