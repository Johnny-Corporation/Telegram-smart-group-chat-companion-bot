from __main__ import *


# --- Set memory size ---
@bot.message_handler(commands=["temporary_memory_size"], func=time_filter and member_filter)
@error_handler
def set_temp_memory_size_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["change_temp_memory_size.txt"].format(
            memory=groups[message.chat.id].temporary_memory_size
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_memory_size_reply_handler)
