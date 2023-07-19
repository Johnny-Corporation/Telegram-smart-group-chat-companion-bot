from __main__ import *


# --- Clean memory ---
@bot.message_handler(commands=["clean_memory"], func=time_filter and member_filter)
@error_handler
def clean_memory_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].messages_history = []
    bot.reply_to(message, templates[language_code]["memory_reset.txt"])
