from __main__ import *
from os import _exit, listdir


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


# ----------------------- Functions for devtools -----------------------


def get_user_info(message):
    users_list = listdir("output\\clients_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(message, f"Choose user, reply to this message:\n {users}")
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, get_user_info_reply_handler)


@error_handler
def get_user_info_reply_handler(inner_message):
    try:
        send_file(
            "output\\clients_info\\"
            + listdir("output\\clients_info")[int(inner_message.text)],
            inner_message.chat.id,
            bot,
        )
    except:
        bot.reply_to(inner_message, "Invalid argument")


def get_group_info(message):
    users_list = listdir("output\\groups_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(message, f"Choose group, reply to this message:\n {users}")
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, get_group_info_reply_handler)


@error_handler
def get_group_info_reply_handler(inner_message):
    try:
        send_file(
            "output\\groups_info\\"
            + listdir("output\\groups_info")[int(inner_message.text)],
            inner_message.chat.id,
            bot,
        )
    except:
        bot.reply_to(inner_message, "Invalid argument")


def get_last_20_messages_from_chat(message):
    bot_reply = bot.reply_to(
        message,
        "Send an id in reply to this message, you can get it by viewing json file associated with group or client.",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, get_last_20_messages_from_chat_reply_handler)


@error_handler
def get_last_20_messages_from_chat_reply_handler(inner_message):
    try:
        messages = "\n".join(
            [
                f"{i[0]}: {i[1]}"
                for i in groups[int(inner_message.text)].messages_history[::-1]
            ]
        )
        bot.send_message(inner_message.chat.id, f"Last 20 messages:\n {messages}")
    except:
        bot.reply_to(inner_message, "Invalid argument")


def add_to_todo(message):
    bot_reply = bot.reply_to(
        message,
        "Send task in reply",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, add_to_todo_reply_handler)


@error_handler
def add_to_todo_reply_handler(inner_message):
    with open("Johnny.py", "a") as f:
        f.write(f"\n# [ ] {inner_message.text}\n")
    bot.reply_to(inner_message, "Done!")
