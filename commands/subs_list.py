from __main__ import *


# --- messages info ---
@error_handler
def sub_info(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_account",
    )
    markup.add(button1)

    if message.chat.id not in groups:
        bot.reply_to(
            message,
            templates[language_code]["user_doesnt_registrate.txt"].format(first_name=message.chat.first_name),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return
    
    left_messages = groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"]-groups[message.chat.id].total_spent_messages
    if left_messages < 0:
        left_messages = 0

    dyn_gen_per = translate_text(language_code, 'allowed')
    if groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["dynamic_gen_permission"] == False:
        dyn_gen_per = translate_text(language_code, 'not allowed')
    voice_out_per = translate_text(language_code, 'allowed')
    if groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["voice_output_permission"] == False:
        voice_out_per = translate_text(language_code, 'not allowed')
    set_up_per = translate_text(language_code, 'allowed')
    if groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["sphere_permission"] == False:
        set_up_per = translate_text(language_code, 'not allowed')

    name_of_groups = ''
    for name in groups[message.chat.id].id_groups:
        chat_info = bot.get_chat(name)
        name_of_groups = name_of_groups + chat_info.title
        if name != groups[message.chat.id].id_groups[-1]:
            name_of_groups = name_of_groups + ' , '

    if name_of_groups == '':
        name_of_groups = 'None'

    bot.edit_message_text(
        templates[language_code]["info_about_user_sub.txt"].format(
        first_name=message.chat.first_name,
        subscription=groups[message.chat.id].subscription,
        messages=groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"],
        left_messages=left_messages,
        groups=groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["allowed_groups"],
        left_groups=groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["allowed_groups"] - len(groups[message.chat.id].id_groups),
        name_of_groups=name_of_groups,
        dyn_gen_per=dyn_gen_per,
        voice_out_per=voice_out_per,
        set_up_per=set_up_per
        ),
        message.chat.id, 
        message.message_id, 
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    

@bot.message_handler(commands=["subs_list"], func=time_filter)
def subs_list(message):

    language_code = groups[message.chat.id].lang_code 

    bot.send_message(message.chat.id, templates[language_code]["sub_free_description.txt"], parse_mode = "HTML")
    bot.send_message(message.chat.id, templates[language_code]["sub_pro_description.txt"], parse_mode = "HTML")