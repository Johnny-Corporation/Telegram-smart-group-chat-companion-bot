from __main__ import *


# --- customizations functions ---
@bot.message_handler(commands=["customization"], func=time_filter)
@error_handler
def customization_command(message):
    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    dyn_gen_button = types.InlineKeyboardButton(
        text="Enable/disable dynamic generation", callback_data="dyn_gen"
    )
    change_lang_button = types.InlineKeyboardButton(
        text="Change the language", callback_data="change_lang"
    )
    voice_in_button = types.InlineKeyboardButton(
        text="Change the language", callback_data="change_lang"
    )

    # Adding buttons to keyboard
    customization_markup.add(dyn_gen_button)
    customization_markup.add(change_lang_button)

    # Sending message with keyboard
    language_code = groups[message.chat.id].lang_code
    bot.send_message(
        message.chat.id,
        templates[language_code]["customization.txt"],
        reply_markup=customization_markup,
        parse_mode="HTML",
    )
