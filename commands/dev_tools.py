from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["dev_tools"], func=time_filter)
@error_handler
def dev_tools(message, edit: bool = False):
    if str(message.chat.id) not in developer_chat_IDs:
        bot.reply_to(message, "ACCESS DENIED")
        bot.reply_to(message, "🖕")
        return

    chat_id = message.chat.id
    dev_tools_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    button1 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Kill bot"),
        callback_data="kill_bot",
    )
    button2 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Kill bot and run reserver"),
        callback_data="kill_bot_run_reserver",
    )
    dev_tools_markup.add(button1, button2)
    # --------------------------------------
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get logs"),
        callback_data="get_logs",
    )
    dev_tools_markup.add(button)
    # --------------------------------------
    button1 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get user"),
        callback_data="get_user",
    )
    button2 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get group"),
        callback_data="get_group",
    )
    dev_tools_markup.add(button1, button2)
    # --------------------------------------
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Database file"),
        callback_data="get_db_file",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Available promocodes"),
        callback_data="get_promocodes",
    )
    button1 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Add promocode"),
        callback_data="add_promocode",
    )
    button2 = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Delete promocode"),
        callback_data="delete_promocode",
    )
    dev_tools_markup.add(button)
    dev_tools_markup.add(button1, button2)
    button = types.InlineKeyboardButton(
        text=translate_text(
            groups[chat_id].lang_code, "Add new language(s) (not working on server!)"
        ),
        callback_data="add_lang",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(
            groups[chat_id].lang_code,
            "Add default langs: ru,de,es (not working on server!)",
        ),
        callback_data="add_default_langs",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get current output"),
        callback_data="get_cur_out",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get all archived outputs"),
        callback_data="get_all_outs",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Add current output to archive"),
        callback_data="copy_cur_out_to_archive",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Add commercial link"),
        callback_data="add_commercial_link",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Send newsletter to all users"),
        callback_data="ask_newsletter",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Create survey"),
        callback_data="ask_data_for_survey",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "Get current survey statistics"),
        callback_data="get_survey_stat",
    )
    dev_tools_markup.add(button)
    button = types.InlineKeyboardButton(
        text=translate_text(groups[chat_id].lang_code, "💀Close dev tools"),
        callback_data="close_message",
    )
    dev_tools_markup.add(button)
    # Sending keyboard
    bot.send_message(
        chat_id,
        translate_text(groups[chat_id].lang_code, "----- DEVELOPER TOOLS -----"),
        reply_markup=dev_tools_markup,
        parse_mode="HTML",
    )
    bot.delete_message(message.chat.id, message.message_id)
