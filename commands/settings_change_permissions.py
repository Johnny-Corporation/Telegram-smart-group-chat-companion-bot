from __main__ import *


# ---------- Main message ----------

# --- customizations functions ---


def change_permissions_settings(message):
    language_code = groups[message.chat.id].lang_code

    # Choose group

    characteristics_of_sub_markup = types.InlineKeyboardMarkup()



    for num, id_group in enumerate(groups[message.chat.id].groups_id):

        chat_info = bot.get_chat(id_group)
        group_name = chat_info.title
        
        group_button = types.InlineKeyboardButton(
            text=group_name, callback_data=f"change-permissions_{id_group}"
        )

        # bot.edit_message_text(
        #     templates[language_code]["customization.txt"],
        #     message.chat.id,
        #     message.message_id,
        #     reply_markup=characteristics_of_sub_markup,
        #     parse_mode="HTML",
        # )

    

    # --- Buttons ---
    permission_asnwer_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"], callback_data="permission_dyn_gen"
    )
    permission_language_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"], callback_data="voice_out"
    )
    permission_special_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"], callback_data="voice_out"
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_settings",
    )

    # Adding buttons to keyboard
    characteristics_of_sub_markup.add(permission_asnwer_settings_button)
    characteristics_of_sub_markup.add(permission_language_settings_button)
    characteristics_of_sub_markup.add(permission_special_settings_button)
    characteristics_of_sub_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=characteristics_of_sub_markup,
        parse_mode="HTML",
    )


def change_permissions_of_group(message, group_id):

    # --- Buttons ---
    permission_asnwer_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"], callback_data="dyn_gen"
    )
    permission_language_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"], callback_data="voice_out"
    )
    permission_special_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"], callback_data="voice_out"
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_settings",
    )

    # Adding buttons to keyboard
    characteristics_of_sub_markup.add(permission_asnwer_settings_button)
    characteristics_of_sub_markup.add(permission_language_settings_button)
    characteristics_of_sub_markup.add(permission_special_settings_button)
    characteristics_of_sub_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=characteristics_of_sub_markup,
        parse_mode="HTML",
    )