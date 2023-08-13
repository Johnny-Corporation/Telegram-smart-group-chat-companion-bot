from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["settings"], func=time_filter and member_filter)
def settings_command(message, back_from: bool=False):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_up.txt"],
        callback_data="set_up",
    )
    button2 = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_customization.txt"],
        callback_data="customization",
    )

    # Adding buttons to keyboard
    markup.add(button1)
    markup.add(button2)

    if back_from:
        bot.edit_message_text(
            groups[message.chat.id].templates[language_code]["change_bot_settings.txt"], 
            message.chat.id, 
            message.message_id, 
            reply_markup=markup,
            parse_mode="HTML"
        )
        return

    # Seconding keyboard
    bot.send_message(
            message.chat.id,
            groups[message.chat.id].templates[language_code]["change_bot_settings.txt"],
            reply_markup=markup,
            parse_mode="HTML",
        )