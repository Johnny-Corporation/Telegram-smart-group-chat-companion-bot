# from telebot import TeleBot
# from os import environ

# tg_key = '5918531073:AAF1q4o2WIkBuee4CTSc95XIWexUox9-Xw4'
# bot = TeleBot(tg_key)
# bot_id = bot.get_me().id


# @bot.message_handler()
# def voice_processing(message):

#     bot.send_message(message.chat.id,'message.type')

#     bot.send_message(message.chat.id,message.content_type)

#     file_info = bot.get_file(message.voice.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open('new_file.ogg', 'wb') as new_file:
#         new_file.write(downloaded_file)


# @bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
#     'text', 'location', 'contact', 'sticker'])
# def voice_processing(message):

#     bot.send_message(message.chat.id,'message.type')

#     bot.send_message(message.chat.id,message.content_type)

#     # file_info = bot.get_file(message.voice.file_id)
#     # downloaded_file = bot.download_file(file_info.file_path)
#     # with open('new_file.ogg', 'wb') as new_file:
#     #     new_file.write(downloaded_file)


# bot.polling()



import os

filepath = 'output\\voice_in\\voice_message.AwACAgIAAxkBAAMgZLBbgtUX7Xsg6iTm4mUZokKn9_sAAk09AAKNqYhJWwrB8BCKQLovBA.ogg'

if os.path.isfile(filepath):
    # Open the file
    try:

        with open(filepath, 'r') as file:
            data = file.read()
        print('ev')
    except IOError:
        print(f"Error opening file at {filepath}")
else:
    print(f"No file found at {filepath}")