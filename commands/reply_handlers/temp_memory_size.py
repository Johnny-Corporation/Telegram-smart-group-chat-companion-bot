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
            inner_message.chat.id, templates[language_code]["set_memory_declined.txt"]
        )
        return
    if val <= 0:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["set_memory_declined.txt"]
        )
        return

    groups[inner_message.chat.id].change_memory_size = val
    bot.reply_to(inner_message, "✅")