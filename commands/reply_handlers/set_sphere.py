from __main__ import *


# --- reply handler for set sphere
@error_handler
def set_sphere_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = str(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["sphere_declined.txt"]
        )
        return

    groups[inner_message.chat.id].sphere = val
    bot.reply_to(inner_message, "✅")
