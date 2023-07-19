from __main__ import *


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"], func=time_filter and member_filter)
@error_handler
def set_temp_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["change_temp.txt"].format(
            temperature=groups[message.chat.id].temperature
        ),
        parse_mode="HTML",
    )
    bot.register_for_reply(bot_reply, set_temp_reply_handler)
