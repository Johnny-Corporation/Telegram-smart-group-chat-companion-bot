from os import listdir
from __main__ import *
from utils.db_controller import Controller

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
    path = (
        "output\\clients_info\\"
        + listdir("output\\clients_info")[int(inner_message.text)]
    )
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
        print(i)
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
    path = (
        "output\\groups_info\\"
        + listdir("output\\groups_info")[int(inner_message.text)]
    )
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
        print(i)
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


@error_handler
def get_promocodes(inner_message):
    bot.send_message(
        inner_message.chat.id,
        f"Subscription 'Pro': {sub_pro_promocode}\nDiscount 50% ob buying the sub: {discount_on_sub_50}\nGet 100 messages: {promocode_100}",
    )


def ask_newsletter(message):
    bot_reply = bot.reply_to(
        message,
        translate_text(
            groups[message.chat.id].lang_code, "Send your text in reply to this message"
        ),
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
            "This message will be sent to all users and groups! Confirm?",
        ),
        reply_markup=markup,
    )


def send_newsletter(message):
    chat_id = groups[message.chat.id]
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
    bot.send_message(
        message.chat.id,
        translate_text(
            groups[message.chat.id].lang_code,
            "Sending newsletter...",
        ),
    )
    for chat_id_ in groups:
        bot.send_message(int(chat_id_), text)
    bot.send_message(
        message.chat.id,
        translate_text(
            groups[message.chat.id].lang_code,
            f"Done sending! Sent to {len(groups)} groups and users in total including you.",
        ),
    )
