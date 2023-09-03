from __main__ import *


# ---------- Main message ----------

def inline_mode_additional_settings(message):

    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    gpt_answers_additional_settigns_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_inline_mode_model_additional_settings.txt"], callback_data="inline_mode_model_additional_settings"
    )
    
    smile='❌'
    if groups[message.chat.id].num_inline_gpt_suggestions == 1:
        smile='✅'
    button1 = types.InlineKeyboardButton(
        text="{} 1️⃣".format(smile), callback_data="change_inline_gpt_suggestions_num_1"
    )
    
    smile='❌'
    if groups[message.chat.id].num_inline_gpt_suggestions == 2:
        smile='✅'
    button2 = types.InlineKeyboardButton(
        text="{} 2️⃣".format(smile), callback_data="change_inline_gpt_suggestions_num_2"
    )
    
    smile='❌'
    if groups[message.chat.id].num_inline_gpt_suggestions == 3:
        smile='✅'
    button3 = types.InlineKeyboardButton(
        text="{} 3️⃣".format(smile), callback_data="change_inline_gpt_suggestions_num_3"
    )
    
    smile='❌'
    if groups[message.chat.id].num_inline_gpt_suggestions == 4:
        smile='✅'
    button4 = types.InlineKeyboardButton(
        text="{} 4️⃣".format(smile), callback_data="change_inline_gpt_suggestions_num_4"
    )
    
    
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="choose_inline_mode",
    )

    # Adding buttons to keyboard
    customization_markup.add(button1)
    customization_markup.add(button2)
    customization_markup.add(button3)
    customization_markup.add(button4)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["additional_settings_inline.txt"], 
        message.chat.id, 
        message.message_id, 
        reply_markup=customization_markup,
        parse_mode="HTML",
    )