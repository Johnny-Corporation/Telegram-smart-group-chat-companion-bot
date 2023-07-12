from __main__ import *


# --- About ---
@bot.message_handler(commands=["about"], func=time_filter)
@error_handler
def about_command(message):
    language_code = groups[message.chat.id].lang_code
    print("-----------------------")
    bot.reply_to(message, templates[language_code]["description.txt"])
