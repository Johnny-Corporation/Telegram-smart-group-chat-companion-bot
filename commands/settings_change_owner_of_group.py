from __main__ import *


# --- Change the owner of group ---
@bot.message_handler(commands=["change_owner_of_group"], func=time_filter)
@error_handler
def change_owner_of_group(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["change_owner_of_group.txt"],
        parse_mode="HTML",
    )

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, change_owner_reply_handler)