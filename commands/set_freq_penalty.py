from __main__ import *


# --- Set frequency penalty (variety of answers) ---
@bot.message_handler(commands=["set_variety"], func=time_filter and member_filter)
@error_handler
def set_frequency_penalty_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["set_variety.txt"].format(
            frequency_penalty=groups[message.chat.id].frequency_penalty
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_frequency_penalty_reply_handler)
