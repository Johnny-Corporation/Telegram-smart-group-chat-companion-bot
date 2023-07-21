from __main__ import *


# --- About ---
@bot.message_handler(commands=["about"], func=time_filter and member_filter)
@error_handler
def about_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.reply_to(message, groups[message.chat.id].templates[language_code]["description.txt"].format(
        probability=groups[message.chat.id].trigger_probability
    ), parse_mode='HTML')
