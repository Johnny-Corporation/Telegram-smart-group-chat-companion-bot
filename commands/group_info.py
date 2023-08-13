from __main__ import *


# --- Group info ---
@bot.message_handler(commands=["group_info"], func=time_filter and member_filter)
@error_handler
def group_info_command(message):

    language_code = groups[message.chat.id].lang_code


    if message.chat.id>0:
        bot.send_message(message.chat.id, groups[message.chat.id].templates[language_code]["group_info_in_private.txt"])
        return 


    total_tokens = groups[message.chat.id].total_spent_tokens
    if groups[message.chat.id].dynamic_gen == False:
        dynamic_gen_en = "disabled"
    else:
        dynamic_gen_en = "enabled"

    if groups[message.chat.id].voice_input_permission == True:
        voice_in = "allowed"
    else:
        voice_in = "disallowed"

    if groups[message.chat.id].lang_code == "en":
        language_code1 = "english"
    elif groups[message.chat.id].lang_code == "ru":
        language_code1 = "русский"
    elif groups[message.chat.id].lang_code == "es":
        language_code1 = "español"
    elif groups[message.chat.id].lang_code == "de":
        language_code1 = "deutsch"

    if groups[message.chat.id].answer_length == "as you need":
        answer_length = translate_text(language_code, "as bot need")
    else:
        answer_length = translate_text(language_code, "as you need")

    bot.send_message(
        message.chat.id,
        groups[message.chat.id].templates[language_code]["group_info.txt"].format(
            group_name=message.chat.title,
            username=str(bot.get_chat(groups[message.chat.id].owner_id).username),
            subscription=groups[message.chat.id].subscription,
            temperature=groups[message.chat.id].temperature,
            answers_frequency=groups[message.chat.id].trigger_probability,
            temporary_memory_size=groups[message.chat.id].temporary_memory_size,
            presense_penalty=groups[message.chat.id].presence_penalty,
            frequency_penalty=groups[message.chat.id].frequency_penalty,
            length=answer_length,
            sphere=groups[message.chat.id].sphere,
            tokens=groups[message.chat.id].tokens_limit,
            dollars=tokens_to_dollars(
                groups[groups[message.chat.id].owner_id].model,
                total_tokens[0],
                total_tokens[1],
            ),
            spent_tokens=sum(groups[message.chat.id].total_spent_tokens),
            tokens_left = groups[message.chat.id].tokens_limit-groups[message.chat.id].total_spent_tokens[0]-groups[message.chat.id].total_spent_tokens[1],
            dynamic_gen_en=dynamic_gen_en,
            language=language_code1,
            voice_in=voice_in,
            ),
        parse_mode="HTML",
    )
