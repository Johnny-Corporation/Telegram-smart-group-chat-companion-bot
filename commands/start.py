from __main__ import *


# --- Start ---
@bot.message_handler(commands=["start"], func=time_filter and member_filter)
@error_handler
def about_command(message):
    init_new_group(message.chat.id, message.from_user.id)
