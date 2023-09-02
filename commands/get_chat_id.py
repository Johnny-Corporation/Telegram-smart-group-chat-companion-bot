from __main__ import *


# --- About ---
@bot.message_handler(commands=["id"], func=time_filter)
@error_handler
def about(message):
    bot.reply_to(message, message.chat.id)
