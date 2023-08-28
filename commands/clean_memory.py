from __main__ import *


# --- Clean memory ---
@error_handler
def clean_memory(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].messages_history = []
    bot.reply_to(message, templates[language_code]["memory_reset.txt"])
