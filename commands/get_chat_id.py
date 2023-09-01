from __main__ import *


# --- About ---
@bot.message_handler(commands=["id"], func=time_filter)
@error_handler
def about(message, back_from=False):
    bot.reply_to(message, message.chat.id)
