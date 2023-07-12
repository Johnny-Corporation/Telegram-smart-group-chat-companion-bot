from __main__ import *


# --- Manual mode enable ---
@bot.message_handler(commands=["enable_manual"], func=time_filter)
@error_handler
def manual_enable_command(message):
    if groups[message.chat.id].enabled == False:
        bot.reply_to(
            message, templates[language_code]["bot_is_disabled.txt"], parse_mode="HTML"
        )

    else:
        language_code = groups[message.chat.id].lang_code
        groups[message.chat.id].trigger_probability = 0
        bot.reply_to(
            message, templates[language_code]["manual_enabled.txt"], parse_mode="HTML"
        )


# --- Manual mode disable ---
@bot.message_handler(commands=["disable_manual"], func=time_filter)
@error_handler
def manual_disable_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].trigger_probability = 0.2

    bot.reply_to(message, templates[language_code]["manual_disabled.txt"])
