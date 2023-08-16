from __main__ import *
from os import _exit, listdir
from utils.functions_for_developers import *


@bot.callback_query_handler(func=lambda call: True)
@error_handler
def keyboard_buttons_handler(call):
    previous_language_code = groups[call.message.chat.id].lang_code

    call_data = call.data
    if "apply_lang" in call.data:
        call_data = "apply_lang"

    match call_data:


        #Choosing mode

        case 'auto_mode':
            auto_enable(message=call.message)
        case 'dialog_mode':
            dialog_enable(message=call.message)
        case 'manual_mode':
            manual_enable(message=call.message)
    

        #Account info
        
        case "purchase":
            purchase(message=call.message)
        case "about_sub":
            sub_info(message=call.message)
        case "back_to_account":
            account(message=call.message, back_from=True)


        #Group info

        case "see_settings_of_bot_answers":
            see_settings_of_bot_answers(message=call.message)
        case "see_settings_of_special_functions":
            see_settings_of_special_functions(message=call.message)
        case "back_to_group":
            group(message=call.message, back_from=True)


        #Translations

        case 'back_to_settings':
            settings(message=call.message, back_from=True)
        case 'bot_answers':
            bot_answers_settings(call.message)
        case 'special_features':
            special_features_settings(call.message)
            

        # Set up funcs

        case "temperature":
            if groups[call.message.chat.id].permissions[groups[call.message.chat.id].subscription]["temperature_permission"] == True:
                set_temp(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "answer_probability":
            set_probability(call.message)
        case "memory_length":
            set_temp_memory_size(call.message)
        case "variety":
            if groups[call.message.chat.id].permissions[groups[call.message.chat.id].subscription]["temperature_permission"] == True:
                set_frequency_penalty(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "creativity":
            if groups[call.message.chat.id].permissions[groups[call.message.chat.id].subscription]["temperature_permission"] == True:
                set_presence_penalty(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "answer_length":
            set_length_answer(call.message)
        case "sphere":
            if groups[call.message.chat.id].permissions[groups[call.message.chat.id].subscription]["temperature_permission"] == True:
                set_sphere(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "change_lang":
            change_language(call.message.chat.id)
        case "change_owner":
            change_owner_of_group(call.message)
            

        # Customization

        case "dyn_gen":

            if groups[call.message.chat.id].permissions[groups[call.message.chat.id].subscription]["dynamic_gen_permission"] == True:

                if groups[call.message.chat.id].voice_out_enabled == True:
                    bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["voice_out_already_enabled.txt"])
                    groups[call.message.chat.id].voice_out_enabled = False

                enable_disable_dynamic_generation(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
            

        case "voice_out":
            if groups[call.message.chat.id].voice_output_permission == False:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"], parse_mode="HTML")
                return 
            

            if groups[call.message.chat.id].dynamic_gen == True:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["dyn_gen_already_enabled.txt"])
                groups[call.message.chat.id].dynamic_gen_permission = False

            
            enable_disable_voice_out(call.message)




        # Answer length

        case "long":
            groups[call.message.chat.id].answer_length = "in detail"
            bot.send_message(
                call.message.chat.id,
                groups[call.message.chat.id].templates[previous_language_code]["length_chosen.txt"],
            )
        case "medium":
            groups[
                call.message.chat.id
            ].answer_length = "not in detail, but not briefly"
            bot.send_message(
                call.message.chat.id,
                groups[call.message.chat.id].templates[previous_language_code]["length_chosen.txt"],
            )
        case "short":
            groups[call.message.chat.id].answer_length = "brief"
            bot.send_message(
                call.message.chat.id,
                groups[call.message.chat.id].templates[previous_language_code]["length_chosen.txt"],
            )
        case "any":
            groups[call.message.chat.id].answer_length = "as you need"
            bot.send_message(
                call.message.chat.id,
                groups[call.message.chat.id].templates[previous_language_code]["length_chosen.txt"],
            )

        # Language

        case "apply_lang":

            print(call)

            button_text, button_id = call.data.split('-')
            lang = check_language(button_text)

            groups[call.message.chat.id].lang_code = lang[0]
            bot.send_message(call.message.chat.id, translate_text(lang[1],f"Language changed to {lang[1]} "))
            language_code = lang[0]


        # DEV TOOLS

        case "kill_bot":
            bot.reply_to(call.message, "Exiting...")
            _exit(0)

        case "get_logs":
            send_file("output/info_logs.log", call.message.chat.id, bot)
            send_file("output/debug_logs.log", call.message.chat.id, bot)

        case "get_user_info":
            get_user_info(call.message)
        case "get_group_info":
            get_group_info(call.message)
        case "user_last_messages":
            get_last_20_messages_from_chat(call.message)
        case "group_last_messages":
            get_last_20_messages_from_chat(call.message)
        case "get_db_file":
            send_file("output/DB.sqlite", call.message.chat.id, bot)
        case "add_to_todo":
            add_to_todo(call.message)
        case "get_promocodes":
            get_promocodes(call.message)
        case "add_lang":
            try:
                language_code = groups[call.message.chat.id].lang_code
                reply_to = bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[language_code]["enter_language.txt"])
            except:
                reply_to = bot.send_message(call.message.chat.id, "Enter the language either as a code (ex. 'es') as a name (ex. 'spanish')")

            
                reply_blacklist[call.message.chat.id].append(reply_to.message_id)
                bot.register_for_reply(reply_to, change_language_reply_handler)
            while True:
                if groups[call.message.chat.id].lang_code != None:
                    break


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
        if call.message.chat.id>0:
            send_welcome_text_and_load_data(
                call.message.chat.id, call.from_user.id, groups[call.message.chat.id].lang_code
            )
        elif call.message.chat.id<0:
            markup = load_buttons(types, groups, call.message.chat.id, groups[call.message.chat.id].lang_code)
            bot.send_message(call.message.chat.id, "Activate bot below", reply_markup=markup)