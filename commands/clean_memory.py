from __main__ import *


# --- Clean memory ---
@bot.message_handler(commands=["clean_memory"], func=time_filter)
@error_handler
def clean_memory(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].messages_history = []
    bot.reply_to(message, groups[message.chat.id].templates[language_code]["memory_reset.txt"])
