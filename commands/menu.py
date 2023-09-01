from __main__ import *


# ---------- Main message ----------


def menu(message, back_from=False):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_question_to_bot.txt"],
        callback_data="question_to_bot",
    )
    markup.add(button1)
    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_generate_image.txt"],
        callback_data="generate_image",
    )
    markup.add(button1)
    if message.chat.id < 0:
        button1 = types.InlineKeyboardButton(
            text=templates[language_code]["button_menu_group.txt"],
            callback_data="group",
        )
        markup.add(button1)
    else:
        button1 = types.InlineKeyboardButton(
            text=templates[language_code]["button_menu_account.txt"],
            callback_data="account",
        )
        markup.add(button1)
    if message.chat.id > 0:
        button1 = types.InlineKeyboardButton(
            text=templates[language_code]["button_purchase.txt"],
            callback_data="purchase",
        )
        markup.add(button1)
    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_menu_settings.txt"],
        callback_data="settings",
    )
    markup.add(button1)
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
        text=templates[language_code]["button_menu_about.txt"],
        callback_data="about",
    )
    markup.add(button2)
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_close.txt"],
        callback_data="close_message",
    )
    markup.add(button2)

    if back_from:
        bot.edit_message_text(
            templates[language_code]["menu.txt"],
            message.chat.id,
            message.message_id,
            reply_markup=markup,
            parse_mode="HTML",
        )
        return

    bot.send_message(
        message.chat.id,
        templates[language_code]["menu.txt"],
        reply_markup=markup,
        parse_mode="HTML",
    )
    bot.delete_message(message.chat.id, message.message_id)
