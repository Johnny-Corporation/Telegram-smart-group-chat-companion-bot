from __main__ import *


# --- ask gen img prompt ---
@bot.message_handler(commands=["img"], func=time_filter)
@error_handler
def ask_gen_image_prompt(message):
    language_code = groups[message.chat.id].lang_code

    bot_reply = bot.send_message(
        message.chat.id, templates[language_code]["img_prompt.txt"]
    )

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, img_prompt_reply_handler)
