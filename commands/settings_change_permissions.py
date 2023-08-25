from __main__ import *


# ---------- Main message ----------

# --- customizations functions ---
@bot.message_handler(commands=["special_features"], func=time_filter)
def change_permission_settings(message):

    language_code = groups[message.chat.id].lang_code

    permissions_markup = types.InlineKeyboardMarkup()

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
    permissions_markup.add(permission_asnwer_settings_button)
    permissions_markup.add(permission_language_settings_button)
    permissions_markup.add(permission_special_settings_button)
    permissions_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"], 
        message.chat.id, 
        message.message_id, 
        reply_markup=permissions_markup,
        parse_mode="HTML",
    )
