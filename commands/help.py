from __main__ import *


# --- Help ---
@bot.message_handler(commands=["help"], func=time_filter)
@error_handler
def help(message):
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["help.txt"],
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
