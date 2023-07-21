from __main__ import *


# --- reply handler for set temp
@error_handler
def set_temp_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_temp_declined.txt"]
        )
        return
    if (val > 2) or (val < 0):
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_temp_declined.txt"]
        )
        return

    groups[inner_message.chat.id].temperature = val
    bot.reply_to(inner_message, "✅")
