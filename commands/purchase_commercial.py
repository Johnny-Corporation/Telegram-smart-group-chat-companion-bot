from __main__ import *

@infinite_retry
def commercial(message):

    language_code = groups[message.chat.id].lang_code

    commercial_markup = types.InlineKeyboardMarkup()

    for suggestion in commercial_links:

        button = types.InlineKeyboardButton(
            text=templates[language_code]["button_messages.txt"].format(num_of_messages=commercial_links[suggestion]),
            callback_data=f"commercialㅤ{suggestion}ㅤ{commercial_links[suggestion]}",
        )
        commercial_markup.add(button)

    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="purchase",
    )
    commercial_markup.add(back_button)

    bot.edit_message_text(
        templates[language_code]["purchase_commercial.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=commercial_markup,
        parse_mode="HTML",
    )

@infinite_retry
def subscribe_to_channel(message, num, channel_username):
    language_code = groups[message.chat.id].lang_code

    commercial_markup = types.InlineKeyboardMarkup()

    button = types.InlineKeyboardButton(
        text=templates[language_code]["button_confirm.txt"],
        callback_data=f"confirm-commercialㅤ{channel_username}ㅤ{num}",
    )
    commercial_markup.add(button)
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="free_messages",
    )
    commercial_markup.add(back_button)

    bot.edit_message_text(
        templates[language_code]["purchase_commercial_subscribe_to_channel.txt"].format(num=num, link=f"https://t.me/{channel_username}"),
        message.chat.id,
        message.message_id,
        reply_markup=commercial_markup,
        parse_mode="HTML",
    )