from __main__ import *
from os import _exit
from utils.functions_for_developers import *
from utils.functions import translate_text


@bot.callback_query_handler(func=lambda call: True)
@error_handler
def keyboard_buttons_handler(call):
    previous_language_code = groups[call.message.chat.id].lang_code

    call_data = call.data
    if "apply_lang" in call.data:
        call_data = "apply_lang"
    if "choose-prob" in call.data:
        call_data = "choose-prob"
    if "commercial" in call.data:
        call_data = "commercial"
    if "confirm-commercial" in call.data:
        call_data = "confirm-commercial"
    if "add_commercial_link" in call.data:
        call_data = "add_commercial_link"
    if "permission-of-group" in call.data:
        call_data = "permission"
    if "change_permission" in call.data:
        call_data = "change_permission"
    if "change-permissions" in call.data:
        call_data = "change-permissions"

    # if "group_permission" in call.data:
    #     call_data

    # survey option
    if call_data.startswith("survey_option_"):
        if call.message.chat.id in already_pressed_survey:
            if call.message.chat.id < 0:
                bot.send_message(
                    call.message.chat.id,
                    translate_text(
                        groups[call.message.chat.id].lang_code,
                        "Someone in this group already voted!",
                    ),
                )
            elif call.message.chat.id > 0:
                bot.send_message(
                    call.message.chat.id,
                    translate_text(
                        groups[call.message.chat.id].lang_code,
                        "You have already voted!",
                    ),
                )
            return
        else:
            already_pressed_survey.append(call.message.chat.id)
        option = call_data.replace("survey_option_", "")
        user_info = bot.get_chat(call.message.chat.id)
        username = user_info.username
        survey_results[option].append([call.message.chat.id, "@" + str(username)])
        return

    match call_data:
        case "menu":
            menu(message=call.message, back_from=True)
        case "menu_from_reply":
            try:
                reply_blacklist[call.message.chat.id].remove(call.message.message_id)
            except:
                None
            bot.clear_reply_handlers_by_message_id(call.message.message_id)
            menu(message=call.message, back_from=True)

        case "question_to_bot":
            question_to_bot(message=call.message)
        case "report_bug":
            report_bug(message=call.message)
        case "request_feature":
            request_feature(message=call.message)
        case "about":
            about(message=call.message, back_from=True)
        case "close_message":
            bot.delete_message(call.message.chat.id, call.message.message_id)
        case "choose_inline_mode":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return
            inline_mode_settings(message=call.message)
        case "generate_image":
            ask_gen_image_prompt(call.message)
        case "other":
            other(message=call.message)
        case "other_from_reply":
            try:
                reply_blacklist[call.message.chat.id].remove(call.message.message_id)
            except:
                None
            bot.clear_reply_handlers_by_message_id(call.message.message_id)
            other(message=call.message)

        # Choosing mode

        case "auto_mode":
            choose_prob(message=call.message)
        case "choose-prob":
            prob = float(call.data.split("_")[1])
            auto_enable(message=call.message, prob=prob)

        case "dialog_mode":
            dialog_enable(message=call.message)
        case "manual_mode":
            manual_enable(message=call.message)

        # Inline mode

        case "inline_mode_model":
            johnny = groups[call.message.chat.id]
            if groups[call.message.chat.id].inline_mode != "GPT":
                # if johnny.subscription != "Pro":
                # target = bot.send_message(
                #     call.message.chat.id,
                #     templates[johnny.lang_code]["only_for_pro.txt"],
                # )
                # threading.Timer(
                #     5,
                #     bot.delete_message,
                #     args=(call.message.chat.id, target.message_id),
                # ).start()
                # else:
                groups[call.message.chat.id].inline_mode = "GPT"
                inline_mode_settings(message=call.message)
        case "inline_mode_google":
            if groups[call.message.chat.id].inline_mode != "Google":
                groups[call.message.chat.id].inline_mode = "Google"
                inline_mode_settings(message=call.message)
        case "inline_mode_youtube":
            if groups[call.message.chat.id].inline_mode != "Youtube":
                groups[call.message.chat.id].inline_mode = "Youtube"
                inline_mode_settings(message=call.message)

        # GPT inline additional settings
        case "change_inline_gpt_suggestions_num_1":
            if groups[call.message.chat.id].num_inline_gpt_suggestions != 1:
                groups[call.message.chat.id].num_inline_gpt_suggestions = 1
                inline_mode_additional_settings(message=call.message)
        case "change_inline_gpt_suggestions_num_2":
            if groups[call.message.chat.id].num_inline_gpt_suggestions != 2:
                if groups[call.message.chat.id].subscription != "Pro":
                    target = bot.send_message(
                        call.message.chat.id,
                        templates[groups[call.message.chat.id].lang_code][
                            "only_for_pro.txt"
                        ],
                    )
                    threading.Timer(
                        5,
                        bot.delete_message,
                        args=(call.message.chat.id, target.message_id),
                    ).start()
                else:
                    groups[call.message.chat.id].num_inline_gpt_suggestions = 2
                    inline_mode_additional_settings(message=call.message)
        case "change_inline_gpt_suggestions_num_3":
            if groups[call.message.chat.id].num_inline_gpt_suggestions != 3:
                if groups[call.message.chat.id].subscription != "Pro":
                    target = bot.send_message(
                        call.message.chat.id,
                        templates[groups[call.message.chat.id].lang_code][
                            "only_for_pro.txt"
                        ],
                    )
                    threading.Timer(
                        5,
                        bot.delete_message,
                        args=(call.message.chat.id, target.message_id),
                    ).start()
                else:
                    groups[call.message.chat.id].num_inline_gpt_suggestions = 3
                    inline_mode_additional_settings(message=call.message)
        case "change_inline_gpt_suggestions_num_4":
            if groups[call.message.chat.id].num_inline_gpt_suggestions != 4:
                if groups[call.message.chat.id].subscription != "Pro":
                    target = bot.send_message(
                        call.message.chat.id,
                        templates[groups[call.message.chat.id].lang_code][
                            "only_for_pro.txt"
                        ],
                    )
                    threading.Timer(
                        5,
                        bot.delete_message,
                        args=(call.message.chat.id, target.message_id),
                    ).start()
                else:
                    groups[call.message.chat.id].num_inline_gpt_suggestions = 4
                    inline_mode_additional_settings(message=call.message)

        # Account info

        case "purchase":
            purchase(message=call.message)
        case "about_sub":
            sub_info(message=call.message)
        case "referral":
            referral(message=call.message)
        case "account":
            account(message=call.message)

        # Group info

        case "see_settings_of_bot_answers":
            see_settings_of_bot_answers(message=call.message)
        case "see_settings_of_special_functions":
            see_settings_of_special_functions(message=call.message)
        case "group":
            group(message=call.message)

        # Translations

        # Settings

        case "settings":
            settings(message=call.message)
        case "settings_from_reply":
            try:
                reply_blacklist[call.message.chat.id].remove(call.message.message_id)
            except:
                None
            bot.clear_reply_handlers_by_message_id(call.message.message_id)
            settings(message=call.message)
        case "change_model":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return

            models_switcher(call.message)
        case "bot_answers":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return
            bot_answers_settings(call.message)
        case "bot_answers_from_reply":
            try:
                reply_blacklist[call.message.chat.id].remove(call.message.message_id)
            except:
                None
            bot.clear_reply_handlers_by_message_id(call.message.message_id)
            bot_answers_settings(call.message)
        case "special_features":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return

            special_features_settings(call.message)

        case "back_to_group_settings":
            change_permissions_settings(message=call.message)
        case "change-permissions":
            change_permissions_of_group(
                message=call.message, group_id=int(call.data.split("_")[1])
            )
        case "change_permission":
            group_id = int(call.data.split("=")[2])
            section = call.data.split("=")[1]

            groups[call.message.chat.id].permissions_of_groups[group_id][
                section
            ] = not groups[call.message.chat.id].permissions_of_groups[group_id][
                section
            ]

            change_permissions_of_group(message=call.message, group_id=group_id)

        case "permissions_of_group":
            change_permissions_settings(call.message)
        case "inline_mode_model_additional_settings":
            inline_mode_additional_settings(message=call.message)

        # Model switching
        case "switch_to_gpt_4":
            johnny = groups[call.message.chat.id]
            call.message.model = "gpt-4"
            if johnny.model != "gpt-4":
                if johnny.subscription != "Pro":
                    target = bot.send_message(
                        call.message.chat.id,
                        templates[johnny.lang_code]["GPT-4FORBIDDEN.txt"],
                    )
                    threading.Timer(
                        5,
                        bot.delete_message,
                        args=(call.message.chat.id, target.message_id),
                    ).start()
                else:
                    switch_model(call.message)
        case "switch_to_gpt35turbo":
            johnny = groups[call.message.chat.id]
            call.message.model = "gpt-3.5-turbo"
            if johnny.model != "gpt-3.5-turbo":
                switch_model(call.message)
        case "switch_to_lama":
            johnny = groups[call.message.chat.id]
            call.message.model = "lama"
            if johnny.model != "lama":
                switch_model(call.message)
        case "switch_to_vicuna":
            johnny = groups[call.message.chat.id]
            call.message.model = "vicuna"
            if johnny.model != "vicuna":
                switch_model(call.message)
        case "switch_to_gigachat":
            johnny = groups[call.message.chat.id]
            call.message.model = "gigachat"
            if johnny.model != "gigachat":
                switch_model(call.message)
        case "switch_to_yandexgpt":
            johnny = groups[call.message.chat.id]
            call.message.model = "yandexgpt"
            if johnny.model != "yandexgpt":
                switch_model(call.message)
        case "switch_to_bard":
            johnny = groups[call.message.chat.id]
            call.message.model = "bard"
            if johnny.model != "bard":
                switch_model(call.message)

        # Set up funcs

        case "settings_bot_answers":
            bot_answers_settings(call.message)
        case "temperature":
            set_temp(call.message)
        case "answer_probability":
            set_probability(call.message)
        case "variety":
            set_frequency_penalty(call.message)
        case "creativity":
            set_presence_penalty(call.message)
        case "answer_length":
            set_length_answer(call.message)
        case "sphere":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return

            if (
                groups[call.message.chat.id].characteristics_of_sub[
                    groups[call.message.chat.id].subscription
                ]["sphere_permission"]
                == True
            ):
                set_sphere_command(call.message)
            else:
                markup = types.InlineKeyboardMarkup()
                back_button = types.InlineKeyboardButton(
                    text="<<<",
                    callback_data="settings",
                )
                markup.add(back_button)
                bot.edit_message_text(
                    templates[previous_language_code]["no_rights.txt"],
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
        case "reset_theme_conversation":
            groups[call.message.chat.id].sphere = None
            set_sphere_command(call.message)

        case "change_lang":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return
            change_language(call.message.chat.id, call.message.message_id)
        case "change_owner":
            if (
                call.message.chat.id < 0
                and call.message.from_user != groups[call.message.chat.id].owner_id
            ):
                if (
                    groups[groups[call.message.chat.id].owner_id].permissions_of_groups[
                        call.message.chat.id
                    ][call_data]
                    == False
                ):
                    markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="settings",
                    )
                    markup.add(back_button)

                    bot.edit_message_text(
                        templates[previous_language_code][
                            "settings_have_no_permission.txt"
                        ],
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                    )
                    return
            change_owner_of_group(call.message)

        # Customization

        case "settings_customization":
            special_features_settings(call.message)

        case "dyn_gen":
            if (
                groups[call.message.chat.id].characteristics_of_sub[
                    groups[call.message.chat.id].subscription
                ]["dynamic_gen_permission"]
                == True
            ):
                if groups[call.message.chat.id].voice_out_enabled == True:
                    groups[call.message.chat.id].voice_out_enabled = False

                enable_disable_dynamic_generation(call.message)
            else:
                markup = types.InlineKeyboardMarkup()
                back_button = types.InlineKeyboardButton(
                    text="<<<",
                    callback_data="settings",
                )
                markup.add(back_button)
                bot.edit_message_text(
                    templates[previous_language_code]["no_rights.txt"],
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                    parse_mode="HTML",
                )

        case "voice_out":
            if groups[call.message.chat.id].dynamic_gen == True:
                groups[call.message.chat.id].dynamic_gen = False

            enable_disable_voice_out(call.message)

        # Answer length

        case "long":
            groups[call.message.chat.id].answer_length = "in detail"
            bot.send_message(
                call.message.chat.id,
                templates[previous_language_code]["length_chosen.txt"],
            )
        case "medium":
            groups[
                call.message.chat.id
            ].answer_length = "not in detail, but not briefly"
            bot.send_message(
                call.message.chat.id,
                templates[previous_language_code]["length_chosen.txt"],
            )
        case "short":
            groups[call.message.chat.id].answer_length = "brief"
            bot.send_message(
                call.message.chat.id,
                templates[previous_language_code]["length_chosen.txt"],
            )
        case "any":
            groups[call.message.chat.id].answer_length = "as you need"
            bot.send_message(
                call.message.chat.id,
                templates[previous_language_code]["length_chosen.txt"],
            )

        # Language

        case "apply_lang":
            button_text, button_id = call.data.split("-")
            lang = check_language(button_text)

            groups[call.message.chat.id].lang_code = lang[0]

            language_code = lang[0]

            markup = load_buttons(
                types,
                groups,
                call.message.chat.id,
                language_code,
                owner_id=groups[call.message.chat.id].owner_id,
            )
            bot.send_message(
                call.message.chat.id,
                translate_text(lang[1], f"Language changed to {lang[1]} "),
                reply_markup=markup,
            )
            if call.message.chat.id > 0:
                bot.delete_message(call.message.chat.id, call.message.message_id)

            if str(call.message.chat.id) in remembered_chats_ids:
                bot.send_message(
                    call.message.chat.id,
                    translate_text(
                        lang[1], f"Loading your data... Done! Bot remembered you!"
                    ),
                    reply_markup=markup,
                )
                remembered_chats_ids.remove(str(call.message.chat.id))

        # DEV TOOLS

        case "get_cur_out":
            create_archive("output", "temp\\output.zip")
            send_file("temp\\output.zip", call.message.chat.id, bot)
        case "get_all_outs":
            create_archive("outputs_archive", "temp\\outputs_archive.zip")
            send_file("temp\\outputs_archive.zip", call.message.chat.id, bot)
        case "kill_bot":
            bot.reply_to(call.message, "😵")
            _exit(0)
        case "kill_bot_run_reserver":
            bot.reply_to(call.message, "😵")
            0 / 0
        case "get_logs":
            send_file("output/info_logs.log", call.message.chat.id, bot)
            send_file("output/debug_logs.log", call.message.chat.id, bot)
        case "copy_cur_out_to_archive":
            copytree(
                "output",
                f"outputs_archive\\output_{str(datetime.now()).split('.')[0].replace(' ','_').replace(':','-')}",
            )
            bot.reply_to(call.message, "✅")

        case "get_user":
            get_user_info(call.message)
        case "get_group":
            get_group_info(call.message)
        case "get_db_file":
            send_file("output\\DB.sqlite", call.message.chat.id, bot)
        case "get_promocodes":
            get_promocodes(call.message)
        case "add_promocode":
            add_promocode(call.message)
        case "delete_promocode":
            delete_promocode(call.message)
        case "add_lang":
            language_code = groups[call.message.chat.id].lang_code
            reply_to = bot.send_message(
                call.message.chat.id,
                groups[call.message.chat.id].templates[language_code][
                    "enter_language.txt"
                ],
            )

            reply_blacklist[call.message.chat.id].append(reply_to.message_id)
            bot.register_for_reply(reply_to, change_language_reply_handler)
        case "add_default_langs":
            change_language_reply_handler([call.message.chat.id, "ru,es,de"])
        case "add_commercial_link":
            language_code = groups[call.message.chat.id].lang_code
            reply_to = bot.send_message(
                call.message.chat.id,
                "Write usename and num of messages in format 'username;num' (and don't forget add bot to channel)",
            )
            reply_blacklist[call.message.chat.id].append(reply_to.message_id)
            bot.register_for_reply(reply_to, add_commercial_link_reply_handler)

        case "ask_newsletter":
            ask_newsletter(call.message)

        case "ask_data_for_survey":
            ask_newsletter(call.message, survey=True)

        case "get_survey_stat":
            get_survey_stat(call.message)

        case "decline_send_newsletter":
            bot.send_message(
                call.message.chat.id,
                translate_text(
                    groups[call.message.chat.id].lang_code,
                    "Canceled. You can create new now",
                ),
            )
            groups[call.message.chat.id].prepared_newsletter = None

        case "confirm_send_newsletter":
            send_newsletter(call.message)

        case "get_error_details":
            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(
                text="Hide details",
                callback_data="hide_error_details",
            )
            markup.add(back_button)

            try:
                bot.edit_message_text(
                    errors_details[call.message.message_id],
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                )
            except:  # error text too long
                bot.edit_message_text(
                    "Output too long",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                )
                with open("temp\\error.txt", "w") as f:
                    f.write(errors_details[call.message.message_id])
                send_file("temp\\error.txt", call.message.chat.id, bot)

        case "hide_error_details":
            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(
                text="Show details",
                callback_data="get_error_details",
            )
            markup.add(back_button)

            bot.edit_message_text(
                errors_previews[call.message.message_id],
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup,
            )

        # Purchase the subscription

        case "free_messages":
            commercial(message=call.message)
        case "commercial":
            subscribe_to_channel(
                message=call.message,
                num=call.data.split("ㅤ")[2],
                channel_username=call.data.split("ㅤ")[1],
            )
        case "confirm-commercial":
            channel_username = call.data.split("ㅤ")[1]
            val = call.data.split("ㅤ")[2]

            check = check_on_channel_sub(
                bot, call.message.from_user.id, channel_username
            )
            if check:
                check_on_sub = groups[call.message.chat.id].commercial_links.pop(
                    channel_username, False
                )
                if check_on_sub == False:
                    commercial_markup = types.InlineKeyboardMarkup()
                    back_button = types.InlineKeyboardButton(
                        text="<<<",
                        callback_data="purchase",
                    )
                    commercial_markup.add(back_button)
                    bot.send_message(
                        call.message.chat.id,
                        templates[previous_language_code]["purchase_used_sub.txt"],
                        reply_markup=commercial_markup,
                        parse_mode="HTML",
                    )

                groups[call.message.chat.id].add_purchase_of_messages(
                    call.message.chat.id, int(val)
                )
                bot.send_message(
                    call.message.chat.id,
                    templates[previous_language_code]["new_messages.txt"],
                    parse_mode="HTML",
                )

                bot.delete_message(call.message.chat.id, call.message.message_id)
                return
            bot.answer_callback_query(
                call.id,
                text=templates[previous_language_code]["purchase_you_unsubscribed.txt"],
                show_alert=True,
            )

        case "free_sub":
            rus_payment(call.message, type_of_sub="free_sub")

        case "easy":
            rus_payment(call.message, type_of_sub="easy")

        case "middle":
            rus_payment(call.message, type_of_sub="middle")

        case "pro":
            rus_payment(call.message, type_of_sub="pro")

        case "more_messages":
            enter_purchase_of_messages(call.message)
        case "promocode":
            enter_promocode(call.message)

        case "extend_sub":
            extend_sub(call.message)

        case "update_sub":
            update_sub(call.message)

        case "change_owner":
            change_owner_of_group(call.message)

        case "rus_payment":
            # Генерация случайного 8-значного числа для label
            label = random.randint(10000000, 99999999)

            # Создание формы оплаты
            quickpay = Quickpay(
                receiver="4100118270605528",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=cost,
                label=label,
            )

        case "eng_pay":
            send_invoice(call.message)

        # Unexpected case

        case _:
            logger.warning(f"Unexpected callback data: {call.data}")

    if not previous_language_code:
        if call.message.chat.id > 0:
            send_welcome_text_and_load_data(
                call.message,
                call.message.chat.id,
                call.from_user.id,
                groups[call.message.chat.id].lang_code,
            )
        # elif call.message.chat.id < 0:
        #     markup = load_buttons(
        #         types,
        #         groups,
        #         call.message.chat.id,
        #         groups[call.message.chat.id].lang_code,
        #     )
        #     # bot.send_message(call.message.chat.id, 'ㅤ', reply_markup=markup)
