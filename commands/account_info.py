from __main__ import *


# --- Help ---
@bot.message_handler(commands=["account_info"], func=time_filter and member_filter)
@error_handler
def account_info_command(message):
    language_code = groups[message.chat.id].lang_code

    if message.from_user.id not in groups:
        bot.reply_to(
            message,
            groups[message.chat.id].templates[language_code]["user_doesnt_registrate.txt"].format(first_name=message.from_user.first_name),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return
    
    left_tokens = groups[message.from_user.id].tokens_limit-groups[message.from_user.id].total_spent_tokens[0]-groups[message.from_user.id].total_spent_tokens[1]
    if left_tokens < 0:
        left_tokens = 0

    dyn_gen_per = translate_text(language_code, 'allowed')
    if groups[message.from_user.id].dynamic_gen_permission == False:
        dyn_gen_per = translate_text(language_code, 'not allowed')
    voice_in_per = translate_text(language_code, 'allowed')
    if groups[message.from_user.id].voice_input_permission == False:
        voice_in_per = translate_text(language_code, 'not allowed')
    voice_out_per = translate_text(language_code, 'allowed')
    if groups[message.from_user.id].voice_output_permission == False:
        voice_out_per = translate_text(language_code, 'not allowed')
    set_up_per = translate_text(language_code, 'allowed')
    if groups[message.from_user.id].sphere_permission == False:
        set_up_per = translate_text(language_code, 'not allowed')

    name_of_groups = ''
    for name in groups[message.from_user.id].id_groups:
        chat_info = bot.get_chat(name)
        name_of_groups = name_of_groups + chat_info.title
        if name != groups[message.from_user.id].id_groups[-1]:
            name_of_groups = name_of_groups + ' , '

    if name_of_groups == '':
        name_of_groups = 'None'

    bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["account_info.txt"].format(
        first_name=message.from_user.first_name,
        subscription=groups[message.from_user.id].subscription,
        tokens=groups[message.from_user.id].tokens_limit,
        left_tokens=left_tokens,
        groups=groups[message.from_user.id].allowed_groups,
        left_groups=groups[message.from_user.id].allowed_groups - len(groups[message.from_user.id].id_groups),
        name_of_groups=name_of_groups,
        temp_memory_limit=groups[message.from_user.id].temporary_memory_size_limit,
        temp_memory=groups[message.from_user.id].temporary_memory_size,
        dyn_gen_per=dyn_gen_per,
        voice_in_per=voice_in_per,
        voice_out_per=voice_out_per,
        set_up_per=set_up_per
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
