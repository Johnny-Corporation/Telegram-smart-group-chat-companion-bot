from __main__ import *


# --- reply handler for set probability
@error_handler
def set_probability_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_probability_declined.txt"],
        )
        return
    if (val < 0) or (val > 1):
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_probability_declined.txt"],
        )
        return

    groups[inner_message.chat.id].trigger_probability = val
    bot.reply_to(inner_message, "✅")