from __main__ import *


# --- Enable ---
@bot.message_handler(commands=["enable"], func=time_filter)
@error_handler
def enable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = True
    if language_code == "ru":
        bot.send_sticker(message.chat.id, stickers["enable"])
    bot.reply_to(message, templates[language_code]["enabled.txt"], parse_mode="HTML")


# --- Disable ---
@bot.message_handler(commands=["disable"], func=time_filter)
@error_handler
def disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = False

    bot.send_message(message.chat.id, templates[language_code]["disabled.txt"])
