from __main__ import *


# --- customizations functions ---
@bot.message_handler(commands=["customization"], func=time_filter and member_filter)
def customization_command(message):

    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    dyn_gen_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_dyn_gen.txt"], callback_data="dyn_gen"
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(dyn_gen_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        groups[message.chat.id].templates[language_code]["customization.txt"], 
        message.chat.id, 
        message.message_id, 
        reply_markup=customization_markup,
        parse_mode="HTML",
    )
