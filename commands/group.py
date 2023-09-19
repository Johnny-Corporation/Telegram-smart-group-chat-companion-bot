from __main__ import *


# --- Group info ---


@bot.message_handler(commands=["group"], func=time_filter)
def group(message):
    language_code = groups[message.chat.id].lang_code

    # --- Detect characteristics_of_sub

    if message.chat.id > 0:
        bot.send_message(
            message.chat.id, templates[language_code]["group_info_in_private.txt"]
        )
        return

    if groups[message.chat.id].lang_code == "en":
        language_code1 = "english"
    elif groups[message.chat.id].lang_code == "ru":
        language_code1 = "русский"
    elif groups[message.chat.id].lang_code == "es":
        language_code1 = "español"
    elif groups[message.chat.id].lang_code == "de":
        language_code1 = "deutsch"

    # --- Buttons ---
    markup = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton(
    #     text=templates[language_code]["button_see_settings_of_bot_answers.txt"],
    #     callback_data="see_settings_of_bot_answers",
    # )
    # markup.add(button1)
    # button2 = types.InlineKeyboardButton(
    #     text=templates[language_code]["button_see_settings_of_special_functions.txt"],
    #     callback_data="see_settings_of_special_functions",
    # )
    # markup.add(button2)
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )
    markup.add(back_button)

    # --- If we went back from ahead settings ---
    bot.edit_message_text(
        templates[language_code]["group_info.txt"].format(
            group_name=message.chat.title,
            username=str(bot.get_chat(groups[message.chat.id].owner_id).username),
            subscription=groups[message.chat.id].subscription,
            spent_messages=groups[message.chat.id].total_spent_messages,
            messages_left=groups[
                groups[message.chat.id].owner_id
            ].characteristics_of_sub[groups[message.chat.id].subscription][
                "messages_limit"
            ]
            - groups[message.chat.id].total_spent_messages,
            language=language_code1,
        ),
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )


def see_settings_of_special_functions(message):
    language_code = groups[message.chat.id].lang_code

    # --- Detect the characteristics_of_sub ---

    # Dynamic gemeration
    if (
        groups[message.chat.id].characteristics_of_sub[
            groups[message.chat.id].subscription
        ]["dynamic_gen_permission"]
        == False
    ):
        dynamic_gen_en = "disabled"
    else:
        dynamic_gen_en = "enabled"

    # Voice out
    if (
        groups[message.chat.id].characteristics_of_sub[
            groups[message.chat.id].subscription
        ]["voice_output_permission"]
        == True
    ):
        voice_out = "allowed"
    else:
        voice_out = "disallowed"

    # --- Buttons ---

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="group",
    )
    markup.add(back_button)

    # --- Edit 'Group' message ---
    bot.edit_message_text(
        templates[language_code]["special_functions_in_group.txt"].format(
            dynamic_gen_en=dynamic_gen_en, voice_out=voice_out
        ),
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )


def see_settings_of_bot_answers(message):
    language_code = groups[message.chat.id].lang_code

    # --- Detect characteristics_of_sub ---

    if groups[message.chat.id].answer_length == "as you need":
        answer_length = translate_text(language_code, "as bot need")
    else:
        answer_length = translate_text(language_code, "as you need")

    # --- Buttons ---

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="group",
    )
    markup.add(back_button)

    # --- Edit 'Group' message ---
    bot.edit_message_text(
        templates[language_code]["bot_answers_in_group.txt"].format(
            temperature=groups[message.chat.id].temperature,
            answers_frequency=groups[message.chat.id].trigger_probability,
            temporary_memory_size=groups[message.chat.id].temporary_memory_size,
            presense_penalty=groups[message.chat.id].presence_penalty,
            frequency_penalty=groups[message.chat.id].frequency_penalty,
            length=answer_length,
            sphere=groups[message.chat.id].sphere,
        ),
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )
