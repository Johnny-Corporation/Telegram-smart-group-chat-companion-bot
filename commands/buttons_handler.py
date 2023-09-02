from __main__ import *
from os import _exit
from utils.functions_for_developers import *


@bot.callback_query_handler(func=lambda call: True)
@error_handler
def keyboard_buttons_handler(call):
    previous_language_code = groups[call.message.chat.id].lang_code

    call_data = call.data
    if "apply_lang" in call.data:
        call_data = "apply_lang"
    # if "group_permission" in call.data:
    #     call_data

    print(f"CALL DATA:     {call_data}")
    print(f"LNGUAGE SET: {groups[call.message.chat.id].lang_code}")

    match call_data:
        case "menu":
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

        # ---FOR MATVEY---
        case "generate_image":
            ask_gen_image_prompt(call.message)

        # Choosing mode

        case "auto_mode":
            auto_enable(message=call.message)
        case "dialog_mode":
            dialog_enable(message=call.message)
        case "manual_mode":
            manual_enable(message=call.message)

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
        case "bot_answers":
            bot_answers_settings(call.message)
        case "special_features":
            special_features_settings(call.message)
        case "permissions_of_group":
            change_permission_settings(call.message)

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

        case "change_lang":
            change_language(call.message.chat.id, call.message.message_id)
        case "change_owner":
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

            print("QQQQQQQQQQ         ", lang[0])

            groups[call.message.chat.id].lang_code = lang[0]

            language_code = lang[0]

            try:
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
            except:
                None

            bot.delete_message(call.message.chat.id, call.message.message_id)
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
            send_file("output/DB.sqlite", call.message.chat.id, bot)
        case "get_promocodes":
            get_promocodes(call.message)
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

        # Purchase the subscription

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
        elif call.message.chat.id < 0:
            markup = load_buttons(
                types,
                groups,
                call.message.chat.id,
                groups[call.message.chat.id].lang_code,
            )
