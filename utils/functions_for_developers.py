from os import listdir
from __main__ import *

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

@error_handler
def get_promocodes(inner_message):
    bot.send_message(inner_message.chat.id, f"BIG BUSINESS: {big_business_promocode}\nSMALL BUSINESS: {small_business_promocode}\nUSER BUSINESS: {user_promocode}\nGet 100000 tokens: {promocode_100000}")

