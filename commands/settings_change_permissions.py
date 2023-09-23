from __main__ import *


# ---------- Main message ----------

# --- customizations functions ---


def change_permissions_settings(message):
    language_code = groups[message.chat.id].lang_code

    characteristics_of_sub_markup = types.InlineKeyboardMarkup()


    # Choose group
    # --- Buttons ---
    for num, id_group in enumerate(groups[message.chat.id].id_groups):

        chat_info = bot.get_chat(id_group)
        group_name = chat_info.title

        group_button = types.InlineKeyboardButton(
            text=group_name, callback_data=f"change-permissions_{id_group}"
        )
        characteristics_of_sub_markup.add(group_button)
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )
    characteristics_of_sub_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["settings_permissions_of_groups.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=characteristics_of_sub_markup,
        parse_mode="HTML",
    )


def change_permissions_of_group(message, group_id):

    language_code = groups[message.chat.id].lang_code

    characteristics_of_sub_markup = types.InlineKeyboardMarkup()


    # --- Buttons ---

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["change_model"] == True:
        smile = "✅"
    button0 = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_change_model.txt"].format(emoji=smile),
        callback_data=f"change_permission=change_model={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["bot_answers"] == True:
        smile = "✅"
    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_set_up.txt"].format(emoji=smile),
        callback_data=f"change_permission=bot_answers={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["sphere"] == True:
        smile = "✅"
    sphere_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_set_sphere.txt"].format(emoji=smile),
        callback_data=f"change_permission=sphere={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["change_lang"] == True:
        smile = "✅"
    button2 = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_change_lang.txt"].format(emoji=smile),
        callback_data=f"change_permission=change_lang={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["special_features"] == True:
        smile = "✅"
    button3 = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_customization.txt"].format(emoji=smile),
        callback_data=f"change_permission=special_features={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["choose_inline_mode"] == True:
        smile = "✅"
    button4 = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_choose_inline_mode.txt"].format(emoji=smile),
        callback_data=f"change_permission=choose_inline_mode={group_id}",
    )

    smile = "❌"
    if groups[message.chat.id].permissions_of_groups[group_id]["change_owner"] == True:
        smile = "✅"
    owner_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_permission_change_owner.txt"].format(emoji=smile),
        callback_data=f"change_permission=change_owner={group_id}",
    )

    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_group_settings",
    )

    # Adding buttons to keyboard
    characteristics_of_sub_markup.add(button0)
    characteristics_of_sub_markup.add(button1)
    characteristics_of_sub_markup.add(sphere_button)
    characteristics_of_sub_markup.add(button2)
    characteristics_of_sub_markup.add(button3)
    characteristics_of_sub_markup.add(button4)
    characteristics_of_sub_markup.add(owner_button)
    characteristics_of_sub_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["settings_permissions_of_group.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=characteristics_of_sub_markup,
        parse_mode="HTML",
    )