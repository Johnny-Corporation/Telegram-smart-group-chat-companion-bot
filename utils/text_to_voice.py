from __main__ import *
from utils.functions import generate_voice_message


# --- Convert from text to voice ---
def text_to_voice(bot, message, language_code, reply=True, text_from=' '):

    if reply:
        if message.reply_to_message.content_type != "text":
            bot.send_message(message.chat.id, templates[language_code]["uncorrect_type.txt"])
            return
        text = message.reply_to_message.text

    else:

        text = text_from

    with open(generate_voice_message(message, text, language_code), 'rb') as audio:
        bot.send_voice(chat_id=message.chat.id, voice=audio)
        audio_path = audio
    remove(audio_path.name)
    return
