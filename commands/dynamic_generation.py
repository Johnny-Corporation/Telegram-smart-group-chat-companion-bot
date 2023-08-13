from __main__ import *


# --- Dynamic generation ---
@bot.message_handler(commands=["dynamic_generation"], func=time_filter and member_filter)
@error_handler
def dynamic_generation_command(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].dynamic_gen = not groups[message.chat.id].dynamic_gen
    bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["dynamic_generation.txt"].format(
            groups[message.chat.id].dynamic_gen
        ),
    )
