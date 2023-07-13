from __main__ import *
from os import _exit, listdir
from utils.functions_for_developers import *


@bot.callback_query_handler(func=lambda call: True)
@error_handler
def keyboard_buttons_handler(call):
    previous_language_code = groups[call.message.chat.id].lang_code
    match call.data:
        # Bot settings

        case "temperature":
            set_temp_command(call.message)
        case "answer_probability":
            set_probability_command(call.message)
        case "memory_length":
            set_temp_memory_size_command(call.message)
        case "variety":
            set_frequency_penalty_command(call.message)
        case "creativity":
            set_presence_penalty_command(call.message)
        case "answer_length":
            set_length_answer_command(call.message)
        case "sphere":
            set_sphere_command(call.message)

        # Customization

        case "change_lang":
            change_language_command(call.message)
        case "dyn_gen":
            dynamic_generation_command(call.message)

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

        case "en":
            groups[call.message.chat.id].lang_code = "en"
            bot.send_message(call.message.chat.id, "Language changed to english ")
            language_code = "en"
        case "ru":
            groups[call.message.chat.id].lang_code = "ru"
            bot.send_message(call.message.chat.id, "Язык изменен на русский")
        case "de":
            groups[call.message.chat.id].lang_code = "de"
            bot.send_message(call.message.chat.id, "Sprache auf Deutsch geändert")
        case "es":
            groups[call.message.chat.id].lang_code = "es"
            bot.send_message(call.message.chat.id, "Idioma cambiado a español")

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
        # Unexpected case

        case _:
            logger.warning(f"Unexpected callback data: {call.data}")

    if not previous_language_code:
        send_welcome_text_and_load_data(
            call.message.chat.id, groups[call.message.chat.id].lang_code
        )
