from __main__ import *


# --- Request feature ---

@bot.message_handler(commands=["request_feature"], func=time_filter)
@error_handler
def request_feature(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="<<<",
        callback_data="other_from_reply",
    )
    markup.add(button1)

    bot_reply = bot.edit_message_text(templates[language_code]["request_feature.txt"],message.chat.id, message.message_id,reply_markup=markup)
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, feature_request_reply_handler)
