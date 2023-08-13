from __main__ import *


# --- Set sphere of conservation ---
@bot.message_handler(commands=["enter_new_tokens"], func=time_filter and member_filter)
@error_handler
def enter_purchase_of_tokens(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["enter_new_tokens.txt"],
        parse_mode="HTML",
    )

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, enter_new_tokens_reply_handler)