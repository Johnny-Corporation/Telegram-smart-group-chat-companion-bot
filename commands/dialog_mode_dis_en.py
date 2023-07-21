from __main__ import *


# --- Dialog mode enable ---
@bot.message_handler(commands=["enable_dialog"], func=time_filter and member_filter)
@error_handler
def dialog_enable_command(message):
    if groups[message.chat.id].enabled == False:
        bot.reply_to(
            message, groups[message.chat.id].templates[language_code]["bot_is_disabled.txt"], parse_mode="HTML"
        )

    else:
        language_code = groups[message.chat.id].lang_code
        groups[message.chat.id].trigger_probability = 1

        bot.reply_to(message, groups[message.chat.id].templates[language_code]["dialog_enabled.txt"])


# --- Dialog mode disable ---
@bot.message_handler(commands=["disable_dialog"], func=time_filter)
@error_handler
def dialog_disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].trigger_probability = 0.2

    bot.reply_to(message, groups[message.chat.id].templates[language_code]["dialog_disabled.txt"])
