from __main__ import *


# --- Clean memory ---
@bot.message_handler(commands=["change_language"], func=time_filter)
@error_handler
def change_lang(message):
    change_language(message.chat.id)
