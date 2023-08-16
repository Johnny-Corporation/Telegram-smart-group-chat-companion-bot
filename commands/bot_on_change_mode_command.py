from __main__ import *


def change_mode(message):

    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text=templates[language_code]["button_enable_auto.txt"],
        callback_data="auto_mode",
    )
    markup.add(button)
    button = types.InlineKeyboardButton(
        text=templates[language_code]["button_enable_dialog.txt"],
        callback_data="dialog_mode",
    )
    markup.add(button)
    button = types.InlineKeyboardButton(
        text=templates[language_code]["button_enable_manual.txt"],
        callback_data="manual_mode",
    )
    markup.add(button)
    bot.send_message(
        message.chat.id,
        templates[language_code]["enabled.txt"],        #It'ds just Choose chat mode
        reply_markup=markup,
        parse_mode="HTML",
    )