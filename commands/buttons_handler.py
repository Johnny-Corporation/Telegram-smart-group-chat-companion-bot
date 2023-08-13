from __main__ import *
from os import _exit, listdir
from utils.functions_for_developers import *


@bot.callback_query_handler(func=lambda call: True)
@error_handler
def keyboard_buttons_handler(call):
    previous_language_code = groups[call.message.chat.id].lang_code
    match call.data:

        #Translations

        case 'back_to_settings':
            settings_command(message=call.message, back_from=True)

        case 'set_up':
            set_up_command(call.message)

        case 'customization':
            customization_command(call.message)
            

        # Set up funcs

        case "temperature":
            if groups[call.message.chat.id].temperature_permission == True:
                set_temp_command(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "answer_probability":
            set_probability_command(call.message)
        case "memory_length":
            set_temp_memory_size_command(call.message)
        case "variety":
            if groups[call.message.chat.id].temperature_permission == True:
                set_frequency_penalty_command(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "creativity":
            if groups[call.message.chat.id].temperature_permission == True:
                set_presence_penalty_command(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "answer_length":
            set_length_answer_command(call.message)
        case "sphere":
            if groups[call.message.chat.id].temperature_permission == True:
                set_sphere_command(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
        case "change_lang":
            change_language(call.message.chat.id)
            

        # Customization

        case "dyn_gen":
            if groups[call.message.chat.id].temperature_permission == True:
                dynamic_generation_command(call.message)
            else:
                bot.send_message(
                    call.message.chat.id, 
                    groups[call.message.chat.id].templates[previous_language_code]["no_rights.txt"],
                    parse_mode = "HTML"
                )
            

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

        case "en":
            groups[call.message.chat.id].lang_code = "en"
            bot.send_message(call.message.chat.id, "Language changed to english ")
            language_code = "en"
        case "ru":
            groups[call.message.chat.id].lang_code = "ru"

            sent_message = bot.send_message(call.message.chat.id, "Загружаем язык... Подождите минутку")

            translate_templates("ru")

            groups[call.message.chat.id].templates = load_templates("templates\\")

            bot.delete_message(call.message.chat.id, sent_message.message_id)
            bot.send_message(call.message.chat.id, "Язык изменен на русский")
        case "other":

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


        # Purchase the subscription


        case "free_sub":

            groups[call.message.chat.id].add_new_user(call.message.chat.id, call.message.from_user.first_name, call.message.from_user.last_name, call.message.from_user.username, 'SMALL BUSINESS (trial)', 5, 100, 3000000, True, True, True, True, True, True, True)
            groups[call.message.chat.id].load_subscription(call.message.chat.id)
            for group_id in groups[call.message.chat.id].id_groups:
                groups[group_id].subscription = groups[call.message.chat.id].subscription
                groups[group_id].tokens_limit = groups[call.message.chat.id].tokens_limit
                groups[group_id].dynamic_gen_permission = groups[call.message.chat.id].dynamic_gen_permission
                groups[group_id].voice_input_permission = groups[call.message.chat.id].voice_input_permission
                groups[group_id].voice_output_permission = groups[call.message.chat.id].voice_output_permission

            groups[call.message.chat.id].track_sub(call.message.chat.id, new=True)

        case "easy":

            price = 399
            if groups[call.message.chat.id].total_spent_tokens[0] + groups[call.message.chat.id].total_spent_tokens[1] <= 30000 and groups[call.message.chat.id].subscription == "Free":
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["discount_yes.txt"])
                price = price * 0.8

            pay = accept_payment(call.message, "You buy USER subscription", price)

            if pay:
                groups[call.message.chat.id].add_new_user(call.message.chat.id, call.message.from_user.first_name, call.message.from_user.last_name, call.message.from_user.username, 'USER', 3, 50, 1000000, False, True, False, False, False, False, False)
                groups[call.message.chat.id].load_subscription(call.message.chat.id)
                for group_id in groups[call.message.chat.id].id_groups:
                    groups[group_id].subscription = groups[call.message.chat.id].subscription
                    groups[group_id].tokens_limit = groups[call.message.chat.id].tokens_limit
                    groups[group_id].dynamic_gen_permission = groups[call.message.chat.id].dynamic_gen_permission
                    groups[group_id].voice_input_permission = groups[call.message.chat.id].voice_input_permission
                    groups[group_id].voice_output_permission = groups[call.message.chat.id].voice_output_permission

                groups[call.message.chat.id].track_sub(call.message.chat.id, new=True)

            else:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["buy_was_canceled.txt"])

        case "middle":

            price = 699
            if groups[call.message.chat.id].total_spent_tokens[0] + groups[call.message.chat.id].total_spent_tokens[1] <= 30000 and groups[call.message.chat.id].subscription == "Free":
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["discount_yes.txt"])
                price = price * 0.8

            pay = accept_payment(call.message, "You buy SMALL BUSINESS subscription", price)

            if pay:
                groups[call.message.chat.id].add_new_user(call.message.chat.id, call.message.from_user.first_name, call.message.from_user.last_name, call.message.from_user.username, 'SMALL BUSINESS', 5, 100, 3000000, True, True, True, True, True, True, True)
                groups[call.message.chat.id].load_subscription(call.message.chat.id)
                for group_id in groups[call.message.chat.id].id_groups:
                    groups[group_id].subscription = groups[call.message.chat.id].subscription
                    groups[group_id].tokens_limit = groups[call.message.chat.id].tokens_limit
                    groups[group_id].dynamic_gen_permission = groups[call.message.chat.id].dynamic_gen_permission
                    groups[group_id].voice_input_permission = groups[call.message.chat.id].voice_input_permission
                    groups[group_id].voice_output_permission = groups[call.message.chat.id].voice_output_permission
        
                groups[call.message.chat.id].track_sub(call.message.chat.id, new=True)

            else:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["buy_was_canceled.txt"])

        case "pro":

            price = 1299
            if groups[call.message.chat.id].total_spent_tokens[0] + groups[call.message.chat.id].total_spent_tokens[1] <= 30000 and groups[call.message.chat.id].subscription == "Free":
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["discount_yes.txt"])
                price = price * 0.8

            pay = accept_payment(call.message, "You buy BIG BUSINESS subscription", price)

            if pay:

                groups[call.message.chat.id].add_new_user(call.message.chat.id, call.message.from_user.first_name, call.message.from_user.last_name, call.message.from_user.username, 'BIG BUSINESS', 10, 1000000000000, 5000000, True, True, True, True, True, True, True)
                groups[call.message.chat.id].load_subscription(call.message.chat.id)

                for group_id in groups[call.message.chat.id].id_groups:
                    groups[group_id].subscription = groups[call.message.chat.id].subscription
                    groups[group_id].tokens_limit = groups[call.message.chat.id].tokens_limit
                    groups[group_id].dynamic_gen_permission = groups[call.message.chat.id].dynamic_gen_permission
                    groups[group_id].voice_input_permission = groups[call.message.chat.id].voice_input_permission
                    groups[group_id].voice_output_permission = groups[call.message.chat.id].voice_output_permission

                groups[call.message.chat.id].track_sub(call.message.chat.id, new=True)

            else:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["buy_was_canceled.txt"])

        case "more_tokens":
            enter_purchase_of_tokens(call.message)
        case "promocode":
            enter_promocode(call.message)

        case "extend_sub":

            if groups[call.message.chat.id].subscription == "USER":
                pay = accept_payment(call.message, "You buy USER subscription", 399)
            elif groups[call.message.chat.id].subscription == "SMALL BUSINESS":
                pay = accept_payment(call.message, "You buy SMALL BUSINESS subscription", 699)
            elif groups[call.message.chat.id].subscription == "BIG BUSINESS":
                pay = accept_payment(call.message, "You buy BIG BUSINESS subscription", 1299)  
            else:
                bot.send_message(call.message.chat.id, "Problem")
                pay = False

            if pay:
                groups[call.message.chat.id].extend_sub(call.message.chat.id, call.message.from_user.first_name, call.message.from_user.last_name, call.message.from_user.username)
                groups[call.message.chat.id].track_sub(call.message.chat.id, new=True)
            else:
                bot.send_message(call.message.chat.id, groups[call.message.chat.id].templates[previous_language_code]["buy_was_canceled.txt"])
        
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
        send_welcome_text_and_load_data(
            call.message.chat.id, call.from_user.id, groups[call.message.chat.id].lang_code
        )
