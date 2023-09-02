from __main__ import *


# --- About ---
@bot.message_handler(commands=["model"], func=time_filter)
@error_handler
def about(message):
    bot.reply_to(message, f"Current model: {groups[message.chat.id].model}")
