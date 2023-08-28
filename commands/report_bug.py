from __main__ import *


# --- Report bug ---
@bot.message_handler(commands=["report_bug"], func=time_filter)
@error_handler
def report_bug(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )
    markup.add(button1)

    bot_reply = bot.edit_message_text(templates[language_code]["report_bug.txt"], message.chat.id, message.message_id, reply_markup=markup)
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, bug_report_reply_handler)
