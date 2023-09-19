from __main__ import *


# --- set_up functions ---


def other(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_report_bug.txt"],
        callback_data="report_bug",
    )
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_request_feature.txt"],
        callback_data="request_feature",
    )
    markup.add(button1, button2)
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_support_us.txt"],
        url="https://t.me/JohnnyCorp",
    )
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_contact_developer.txt"],
        url="https://t.me/JohnnyCorp",
    )
    markup.add(button2)
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_about.txt"],
        callback_data="about",
    )
    markup.add(button2)

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
