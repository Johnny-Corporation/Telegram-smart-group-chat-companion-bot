from __main__ import *


# --- Clean memory ---
@bot.message_handler(commands=["change_language"], func=time_filter and member_filter)
@error_handler
def change_lang_command(message):
    change_language(message.chat.id)
