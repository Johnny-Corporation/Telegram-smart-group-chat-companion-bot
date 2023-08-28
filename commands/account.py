from __main__ import *


# --- Help ---
def account(message):
    language_code = groups[message.chat.id].lang_code

    left_messages = (
        groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription][
            "messages_limit"
        ]
        - groups[message.chat.id].total_spent_messages
    )
    if left_messages < 0:
        left_messages = 0

    name_of_groups = ""
    for name in groups[message.chat.id].id_groups:
        chat_info = bot.get_chat(name)
        name_of_groups = name_of_groups + chat_info.title
        if name != groups[message.chat.id].id_groups[-1]:
            name_of_groups = name_of_groups + " , "

    if name_of_groups == "":
        name_of_groups = "None"

    markup = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_about_sub.txt"],
        callback_data="about_sub",
    )
    markup.add(button2)
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )
    markup.add(back_button)

    bot.edit_message_text(
        templates[language_code]["account_info.txt"].format(
            first_name=message.from_user.first_name,
            subscription=groups[message.chat.id].subscription,
            left_messages=left_messages,
            name_of_groups=name_of_groups,
        ),
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )