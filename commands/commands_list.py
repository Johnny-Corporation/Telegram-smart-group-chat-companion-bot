from __main__ import *


# --- Commands list ---
@bot.message_handler(commands=["commands"], func=time_filter and member_filter)
@error_handler
def change_language_command(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id, templates[language_code]["commands.txt"], parse_mode="HTML"
    )
