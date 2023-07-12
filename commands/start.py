from __main__ import *


# --- Start ---
@bot.message_handler(commands=["start"], func=time_filter)
@error_handler
def about_command(message):
    init_new_group(message.chat.id)
