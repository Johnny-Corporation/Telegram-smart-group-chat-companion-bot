from __main__ import *
from utils.functions import generate_voice_message, generate_voice_message_premium
from os import environ


# --- Convert from text to voice ---
def text_to_voice(bot, message, language_code, reply=True, text_from=" "):
    if reply:
        if message.reply_to_message.content_type != "text":
            bot.send_message(
                message.chat.id, templates[language_code]["uncorrect_type.txt"]
            )
            return
        text = message.reply_to_message.text

    else:
        text = text_from

    if str(message.from_user.id) in environ.get("DEVELOPER_CHAT_IDS"):
        path = generate_voice_message_premium(message, text, language_code)
    else:
        path = generate_voice_message(message, text, language_code)

    with open(path, "rb") as audio:
        bot.send_voice(chat_id=message.chat.id, voice=audio)
    return
