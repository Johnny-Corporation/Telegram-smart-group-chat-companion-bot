from __main__ import *


# --- reply handler for set frequency penalty
@error_handler
def set_frequency_penalty_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_variety_declined.txt"]
        )
        return
    if val < 0 or val > 2:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["set_variety_declined.txt"]
        )
        return

    groups[inner_message.chat.id].frequency_penalty = val
    bot.reply_to(inner_message, "✅")
