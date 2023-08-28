from __main__ import *


# --- Set sphere of conversation ---
@error_handler
def enter_promocode(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["enter_promocode.txt"],
        parse_mode="HTML",
    )

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, enter_promocode_reply_handler)
