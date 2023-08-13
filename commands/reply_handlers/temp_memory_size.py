from __main__ import *


# --- reply handler for set temp memory size
@error_handler
def set_memory_size_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_memory_declined.txt"]
        )
        return
    if val <= 0:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_memory_declined.txt"]
        )
        return
    
    if groups[inner_message.chat.id].temporary_memory_size_limit >= val:

        groups[inner_message.chat.id].change_memory_size = val
        bot.reply_to(inner_message, "✅")

    else:

        bot.reply_to(inner_message, groups[inner_message.chat.id].templates[language_code]["no_rights.txt"], parse_mode = "HTML")
