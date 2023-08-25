from __main__ import *


# ---------- Main message ----------

# --- customizations functions ---
@bot.message_handler(commands=["special_features"], func=time_filter)
def special_features_settings(message):

    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    dyn_gen_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_dyn_gen.txt"], callback_data="dyn_gen"
    )
    voice_out_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_voice_out.txt"], callback_data="voice_out"
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_settings",
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

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        text="Come back",
        callback_data="back_to_settings",
    )
    markup.add(back_button)

    groups[message.chat.id].dynamic_gen = not groups[message.chat.id].dynamic_gen
    bot.edit_message_text(
        templates[language_code]["dynamic_generation.txt"].format(
            groups[message.chat.id].dynamic_gen
        ),
        message.chat.id, 
        message.message_id, 
        reply_markup=markup, 
        parse_mode='HTML'
    )

# --- Voice out ---
@error_handler
def enable_disable_voice_out(message):

    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        text="Come back",
        callback_data="back_to_settings",
    )
    markup.add(back_button)

    groups[message.chat.id].voice_out_enabled = not groups[message.chat.id].voice_out_enabled

    if groups[message.chat.id].voice_out_enabled == True:
        bot.edit_message_text(templates[language_code]["voice_out_enabled.txt"], message.chat.id, message.message_id, reply_markup=markup, parse_mode='html')
    elif groups[message.chat.id].voice_out_enabled == False:
        bot.edit_message_text(templates[language_code]["voice_out_disabled.txt"], message.chat.id, message.message_id, reply_markup=markup, parse_mode='html')