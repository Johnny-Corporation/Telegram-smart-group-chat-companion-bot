from __main__ import *


# --- set_up functions ---
@infinite_retry
@bot.message_handler(commands=["settings"], func=time_filter)
def settings(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()

    button0 = types.InlineKeyboardButton(
        text=templates[language_code]["button_change_model.txt"],
        callback_data="change_model",
    )

    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_up.txt"],
        callback_data="bot_answers",
    )
    # sphere of conservation
    sphere_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_sphere.txt"],
        callback_data="sphere",
    )
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_change_lang.txt"],
        callback_data="change_lang",
    )
    button3 = types.InlineKeyboardButton(
        text=templates[language_code]["button_customization.txt"],
        callback_data="special_features",
    )
    button4 = types.InlineKeyboardButton(
        text=templates[language_code]["button_choose_inline_mode.txt"],
        callback_data="choose_inline_mode",
    )

    # Adding buttons to keyboard
    markup.add(button0)
    markup.add(button1)
    markup.add(sphere_button)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)

    if message.chat.id < 0:
        owner_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_change_owner.txt"],
            callback_data="change_owner",
        )
        markup.add(owner_button)

    # if groups[message.chat.id].owner_id and message.chat.id>0:
    #     permission_button = types.InlineKeyboardButton(
    #         text="Change the characteristics of group",
    #         callback_data="permissions_of_group",
    #     )
    #     markup.add(permission_button)

    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )
    markup.add(back_button)

    # Initialize buttons

    bot.edit_message_text(
        templates[language_code]["change_bot_settings.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )
    return
