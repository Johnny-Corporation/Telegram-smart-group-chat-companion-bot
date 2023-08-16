from __main__ import *


# --- About ---
@bot.message_handler(commands=["about"])
# @error_handler
def about(message):
    language_code = groups[message.chat.id].lang_code
    bot.reply_to(message, templates[language_code]["description.txt"].format(
        probability=groups[message.chat.id].trigger_probability
    ), parse_mode='HTML')
