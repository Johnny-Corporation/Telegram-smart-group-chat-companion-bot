from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["dev_tools"], func=time_filter and member_filter)
@error_handler
def dev_tools(message):
    if str(message.chat.id) not in developer_chat_IDs and (
        message.chat.id != -1001948424217
    ):  # Our group id
        bot.reply_to(message, "ACCESS DENIED")
        bot.reply_to(message, "🖕")
        return

    dev_tools_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    button = types.InlineKeyboardButton(
        text="Kill bot",
        callback_data="kill_bot",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get logs",
        callback_data="get_logs",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get info about user",
        callback_data="get_user_info",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get info about group",
        callback_data="get_group_info",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get last 20 messages from group",
        callback_data="group_last_messages",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get last 20 messages from user",
        callback_data="user_last_messages",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get database file",
        callback_data="get_db_file",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Add to Johnny.py TODO list",
        callback_data="add_to_todo",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text="Get avaible promocodes.",
        callback_data="get_promocodes",
    )
    dev_tools_markup.add(button)

    # Seconding keyboard
    bot.send_message(
        message.chat.id,
        "--- DEV TOOLS ---",
        reply_markup=dev_tools_markup,
        parse_mode="HTML",
    )
