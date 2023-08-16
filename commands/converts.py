from __main__ import *


# --- To text ---
@bot.message_handler(commands=["totext"], func=time_filter)
@error_handler
def totext_command(message):
    language_code = groups[message.chat.id].lang_code

    if message.reply_to_message.content_type != "voice":
        bot.send_message(message.chat.id, templates[language_code]["uncorrect_type.txt"])
        return

    if message.reply_to_message:
        
        text = to_text(bot, message, reply_to=message.reply_to_message)

        bot.reply_to(
            message,
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )

        return
    
    bot.send_message(message.chat.id, "Error")
