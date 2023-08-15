from __main__ import *


# --- Convert from text to voice ---
def text_to_voice(message):
    language_code = groups[message.chat.id].lang_code

    if message.reply_to_message.content_type != "text":
        bot.send_message(message.chat.id, groups[message.chat.id].templates[language_code]["uncorrect_type.txt"])
        return

    if message.reply_to_message:

        with open(generate_voice_message(message, message.reply_to_message.text), 'rb') as audio:
            bot.send_voice(chat_id=message.chat.id, voice=audio)
            audio_path = audio
        remove(audio_path.name)
        return
    
    bot.send_message(message.chat.id, "Error")
