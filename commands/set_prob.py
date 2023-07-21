from __main__ import *


# --- Set probability ---
@bot.message_handler(commands=["set_answer_probability"], func=time_filter and member_filter)
@error_handler
def set_probability_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["change_probability.txt"].format(
            probability=groups[message.chat.id].trigger_probability
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_probability_reply_handler)
