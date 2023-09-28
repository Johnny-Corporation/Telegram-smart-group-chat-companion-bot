from os import listdir
from __main__ import *
from utils.db_controller import Controller
import plotly.express as px
from utils.functions import send_file

controller = Controller()
# ----------------------- Functions for devtools -----------------------


def get_user_info(message):
    users_list = listdir("output\\clients_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(
        message,
        translate_text(
            groups[message.chat.id].lang_code, "Choose user, reply to this message:"
        )
        + f"\n {users}",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, get_user_info_reply_handler)


@error_handler
def get_user_info_reply_handler(inner_message):
    try:
        path = (
            "output\\clients_info\\"
            + listdir("output\\clients_info")[int(inner_message.text)]
        )
    except IndexError:
        bot.send_message(
            inner_message.chat.id, "Index out of range, please select from given list"
        )
        return
    send_file(
        path,
        inner_message.chat.id,
        bot,
    )
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # between : and ,
        group_id = int(content.split(",")[0].replace('{"id":', ""))
    content_to_write = ""
    empty_history = True
    content_to_write = ""
    for i in controller.get_last_n_messages_from_chat(n=999999999, chat_id=group_id)[
        ::-1
    ]:
        (i)
        content_to_write += f"{i[0]}  = = = {i[1]}" + "\n"
        empty_history = False
    if not empty_history:
        with open("temp\\messages_history_client.txt", "w", encoding="utf-8") as f:
            f.write(content_to_write)
        send_file(
            "temp\\messages_history_client.txt",
            inner_message.chat.id,
            bot,
        )
    else:
        bot.send_message(inner_message.chat.id, "History is empty")


def get_group_info(message):
    users_list = listdir("output\\groups_info")
    users = "\n".join([f"{i}  -- {users_list[i]} " for i in range(len(users_list))])
    bot_reply = bot.reply_to(
        message,
        translate_text(
            groups[message.chat.id].lang_code, "Choose group, reply to this message:"
        )
        + f"\n {users}",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, get_group_info_reply_handler)


@error_handler
def get_group_info_reply_handler(inner_message):
    try:
        path = (
            "output\\groups_info\\"
            + listdir("output\\groups_info")[int(inner_message.text)]
        )
    except IndexError:
        bot.send_message(
            inner_message.chat.id, "Index out of range, please select from given list"
        )
        return
    send_file(
        path,
        inner_message.chat.id,
        bot,
    )
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # between : and ,
        group_id = int(content.split(",")[0].replace('{"id":', ""))
    content_to_write = ""
    empty_history = True
    content_to_write = ""
    for i in controller.get_last_n_messages_from_chat(n=999999999, chat_id=group_id)[
        ::-1
    ]:
        (i)
        content_to_write += f"{i[0]}  = = = {i[1]}" + "\n"
        empty_history = False
    if not empty_history:
        with open("temp\\messages_history_group.txt", "w", encoding="utf-8") as f:
            f.write(content_to_write)
        send_file(
            "temp\\messages_history_group.txt",
            inner_message.chat.id,
            bot,
        )
    else:
        bot.send_message(inner_message.chat.id, "History is empty")


def get_promocodes(inner_message):
    text = ""
    for promocode_key in promocodes:
        if "sub" in promocode_key:
            text += f"Get Subscription Pro: {promocodes[promocode_key]}\n"
        elif "messages" in promocode_key:
            text += f"Get {promocode_key.split('_')[1]} messages: {promocodes[promocode_key]}\n"
        elif "discount" in promocode_key:
            text += f"Get discount on {promocode_key.split('_')[1]}%: {promocodes[promocode_key]}\n"
    bot.send_message(inner_message.chat.id, text)


def add_promocode(message):
    bot_reply = bot.send_message(
        message.chat.id,
        f"Write your new promocode in format\n  -for discount, messages: type_value (type is discount or messages, value - num of messages or the % for dicount)\n  -for sub: sub\n*for public code add to basic form: _yourcode",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, add_promocode_reply_handler)


def delete_promocode(message):
    bot_reply = bot.send_message(
        message.chat.id,
        f"Write key of promocode to delete",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, delete_promocode_reply_handler)


def ask_newsletter(message, survey=False):
    if not survey:
        text = translate_text(
            groups[message.chat.id].lang_code,
            "Send your text in reply to this message. Attention! Do not use '|' symbol, it will be detected and parsed as survey!!!",
        )
    else:
        text = translate_text(
            groups[message.chat.id].lang_code,
            'Send question and possible answers in format: question|option1|option2|etc. For example: "how old are you?|Yes|No|Im a dog."',
        )
    bot_reply = bot.reply_to(
        message,
        text,
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, ask_news_letter_reply_handler)


def ask_news_letter_reply_handler(inner_message):
    markup = types.InlineKeyboardMarkup()
    groups[inner_message.chat.id].prepared_newsletter = inner_message.text

    button1 = types.InlineKeyboardButton(
        text="✅",
        callback_data="confirm_send_newsletter",
    )
    button2 = types.InlineKeyboardButton(
        text="❌",
        callback_data="decline_send_newsletter",
    )
    markup.add(button1, button2)

    bot.send_message(
        inner_message.chat.id,
        translate_text(
            groups[inner_message.chat.id].lang_code,
            "This message (survey) will be sent to all users and groups! Confirm?",
        ),
        reply_markup=markup,
    )


def send_newsletter(message):
    global survey_results
    text = groups[message.chat.id].prepared_newsletter
    if text is None:
        bot.send_message(
            message.chat.id,
            translate_text(
                groups[message.chat.id].lang_code,
                "WARNING: No prepared message was found, can't send newsletter!",
            ),
        )
        return
    survey = "|" in text
    bot.send_message(
        message.chat.id,
        translate_text(
            groups[message.chat.id].lang_code,
            ("Sending newsletter..." if not survey else "Sending survey..."),
        ),
    )
    if survey:
        keys_to_delete = list(survey_results.keys())
        for i in keys_to_delete:
            del survey_results[i]  # clearing the survey results before next survey
        question = text.split("|")[0]
        options = [i for i in text.split("|")[1:]]
        keyboard = types.InlineKeyboardMarkup()
        for option in options:
            button = types.InlineKeyboardButton(
                text=option, callback_data=f"survey_option_{option}"
            )
            survey_results[option] = []
            keyboard.add(button)
    for chat_id_ in groups:
        if survey:
            if chat_id_ > 0:
                bot.send_message(int(chat_id_), question, reply_markup=keyboard)
        else:
            bot.send_message(int(chat_id_), text)
    bot.send_message(
        message.chat.id,
        translate_text(
            groups[message.chat.id].lang_code,
            f"Done sending! Sent to {len(groups)} groups and users in total including you. If this was survey, it was sent only to groups and number is incorrect, i was lazy to count users sorry :(",
        ),
    )


def get_survey_stat(message):
    global survey_results
    if not survey_results:
        bot.send_message(message.chat.id, "No stats collected")
        return

    fig = px.bar(
        x=list(survey_results.keys()),
        y=[len(i) for i in survey_results.values()],
        color=list(survey_results.keys()),
    )
    bot.send_message(message.chat.id, "Rendering plot...")
    fig.write_image("temp\\stat.png")
    send_file("temp\\stat.png", message.chat.id, bot, send_size=False)

    for key, val in survey_results.items():
        content = f"Guys who choosed {key}  --> \n"
        for i, v in enumerate(val):
            if i == 10:
                bot.send_message(message.chat.id, content)
                content = "Continuation: \n"
            if v[1] != "@None":
                content += f"{v[1]}\n"
            else:
                content += f"[no_username](tg://user?id={val[0][0]})\n"
        bot.send_message(message.chat.id, content, parse_mode="Markdown")
    bot.send_message(message.chat.id, content, parse_mode="Markdown")
