from __main__ import *


# --- Help ---
@bot.message_handler(commands=["account"], func=time_filter)
def account(message, back_from: bool=False):
    language_code = groups[message.chat.id].lang_code

    # if message.from_user.id not in groups:
    #     bot.reply_to(
    #         message,
    #         groups[message.chat.id].templates[language_code]["user_doesnt_registrate.txt"].format(first_name=message.from_user.first_name),
    #         parse_mode="HTML",
    #         disable_web_page_preview=True,
    #     )
    #     return
    
    left_messages = groups[message.chat.id].permissions[groups[message.chat.id].subscription]["messages_limit"]-groups[message.chat.id].total_spent_messages
    if left_messages < 0:
        left_messages = 0

    name_of_groups = ''
    for name in groups[message.chat.id].id_groups:
        chat_info = bot.get_chat(name)
        name_of_groups = name_of_groups + chat_info.title
        if name != groups[message.chat.id].id_groups[-1]:
            name_of_groups = name_of_groups + ' , '

    if name_of_groups == '':
        name_of_groups = 'None'


    #Buttons
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_purchase.txt"],
        callback_data="purchase",
    )
    markup.add(button1)
    button2 = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_about_sub.txt"],
        callback_data="about_sub",
    )
    markup.add(button2)
    
    if back_from:
        bot.edit_message_text(
            groups[message.chat.id].templates[language_code]["account_info.txt"].format(
            first_name=message.from_user.first_name,
            subscription=groups[message.chat.id].subscription,
            left_messages=left_messages,
            left_groups=groups[message.chat.id].permissions[groups[message.chat.id].subscription]["allowed_groups"] - len(groups[message.chat.id].id_groups),
            name_of_groups=name_of_groups,
            ),
            message.chat.id, 
            message.message_id, 
            reply_markup=markup,
            parse_mode="HTML"
        )
        return

    bot.send_message(
        message.chat.id,
        groups[message.chat.id].templates[language_code]["account_info.txt"].format(
        first_name=message.chat.first_name,
        subscription=groups[message.chat.id].subscription,
        left_messages=left_messages,
        left_groups=groups[message.chat.id].permissions[groups[message.chat.id].subscription]["allowed_groups"] - len(groups[message.chat.id].id_groups),
        name_of_groups=name_of_groups,
        ),
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
