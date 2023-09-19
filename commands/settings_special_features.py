from __main__ import *


# ---------- Main message ----------

# --- customizations functions ---


def special_features_settings(message):
    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    smile = "❌"
    if groups[message.chat.id].dynamic_gen == True:
        smile = "✅"
    dyn_gen_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"].format(smile=smile),
        callback_data="dyn_gen",
    )

    smile = "❌"
    if groups[message.chat.id].voice_out_enabled == True:
        smile = "✅"
    voice_out_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"].format(smile=smile),
        callback_data="voice_out",
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(dyn_gen_button)
    customization_markup.add(voice_out_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=customization_markup,
        parse_mode="HTML",
    )


# ---------- Ahead functions ----------

# --- Dynamic generation ---


@error_handler
def enable_disable_dynamic_generation(message):
    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    groups[message.chat.id].dynamic_gen = not groups[message.chat.id].dynamic_gen
    # --- Buttons ---
    smile = "❌"
    if groups[message.chat.id].dynamic_gen == True:
        smile = "✅"
    dyn_gen_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"].format(smile=smile),
        callback_data="dyn_gen",
    )

    smile = "❌"
    if groups[message.chat.id].voice_out_enabled == True:
        smile = "✅"
    voice_out_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"].format(smile=smile),
        callback_data="voice_out",
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(dyn_gen_button)
    customization_markup.add(voice_out_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=customization_markup,
        parse_mode="HTML",
    )


# --- Voice out ---


@error_handler
def enable_disable_voice_out(message):
    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    groups[message.chat.id].voice_out_enabled = not groups[
        message.chat.id
    ].voice_out_enabled
    # --- Buttons ---
    smile = "❌"
    if groups[message.chat.id].dynamic_gen == True:
        smile = "✅"
    dyn_gen_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"].format(smile=smile),
        callback_data="dyn_gen",
    )

    smile = "❌"
    if groups[message.chat.id].voice_out_enabled == True:
        smile = "✅"
    voice_out_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"].format(smile=smile),
        callback_data="voice_out",
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(dyn_gen_button)
    customization_markup.add(voice_out_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["customization.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=customization_markup,
        parse_mode="HTML",
    )
