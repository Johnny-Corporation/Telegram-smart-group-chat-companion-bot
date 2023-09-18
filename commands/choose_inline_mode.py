from __main__ import *


# ---------- Main message ----------

@infinite_retry
def inline_mode_settings(message):

    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    gpt_answers_additional_settings_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_inline_mode_model_additional_settings.txt"], callback_data="inline_mode_model_additional_settings"
    )
    
    
    smile='❌'
    show_gpt_inline_answers_additional_settings = False
    if groups[message.chat.id].inline_mode == "GPT":
        smile='✅'
        show_gpt_inline_answers_additional_settings = True
    gpt_answers_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_inline_mode_model.txt"].format(smile=smile), callback_data="inline_mode_model"
    )

    smile='❌'
    if groups[message.chat.id].inline_mode == "Google":
        smile='✅'
    google_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_inline_mode_google.txt"].format(smile=smile), callback_data="inline_mode_google"
    )
    smile='❌'
    if groups[message.chat.id].inline_mode == "Youtube":
        smile='✅'
    youtube_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_inline_mode_youtube.txt"].format(smile=smile), callback_data="inline_mode_youtube"
    )
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )

    # Adding buttons to keyboard
    if show_gpt_inline_answers_additional_settings:
        customization_markup.add(gpt_answers_additional_settings_button)
    customization_markup.add(gpt_answers_button)
    customization_markup.add(google_button)
    customization_markup.add(youtube_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["choose_inline_mode.txt"], 
        message.chat.id, 
        message.message_id, 
        reply_markup=customization_markup,
        parse_mode="HTML",
    )