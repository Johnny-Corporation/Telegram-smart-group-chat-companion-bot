from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["settings"], func=time_filter)
def settings(message, back_from: bool=False):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_up.txt"],
        callback_data="bot_answers",
    )
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_change_lang.txt"],
        callback_data="change_lang",
    )
    button3 = types.InlineKeyboardButton(
        text=templates[language_code]["button_customization.txt"],
        callback_data="special_features",
    )

    # Adding buttons to keyboard
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    if message.chat.id < 0:
        owner_button = types.InlineKeyboardButton(
            text="Change owner of group",
            callback_data="change_owner",
        )
        markup.add(owner_button)

    if back_from:
        bot.edit_message_text(
            templates[language_code]["change_bot_settings.txt"], 
            message.chat.id, 
            message.message_id, 
            reply_markup=markup,
            parse_mode="HTML"
        )
        return

    # Seconding keyboard
    bot.send_message(
            message.chat.id,
            templates[language_code]["change_bot_settings.txt"],
            reply_markup=markup,
            parse_mode="HTML",
        )