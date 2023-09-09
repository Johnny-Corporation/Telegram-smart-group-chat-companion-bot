from __main__ import *


# ---------- Main message ----------


# --- customizations functions ---
def models_switcher(message):
    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    smile = "❌"
    if groups[message.chat.id].model == "gpt-4":
        smile = "✅"
    gpt_4_button = types.InlineKeyboardButton(
        text="{smile} GPT-4".format(smile=smile),
        callback_data="switch_to_gpt_4",
    )

    smile = "❌"
    if groups[message.chat.id].model == "gpt-3.5-turbo":
        smile = "✅"
    gpt_35_turbo_button = types.InlineKeyboardButton(
        text=templates["en"]["button_gpt35turbo.txt"].format(smile=smile),
        callback_data="switch_to_gpt35turbo",
    )
    
    smile = "❌"
    if groups[message.chat.id].model == "gigachat":
        smile = "✅"
    gigachat_button = types.InlineKeyboardButton(
        text="{smile} Sber GigaChat".format(smile=smile),
        callback_data="switch_to_gigachat",
    )

    smile = "❌"
    if groups[message.chat.id].model == "vicuna":
        smile = "✅"
    vicuna_button = types.InlineKeyboardButton(
        text=templates["en"]["button_vicuna.txt"].format(smile=smile),
        callback_data="switch_to_vicuna",
    )
    
    smile = "❌"
    if groups[message.chat.id].model == "yandexgpt":
        smile = "✅"
    yandexgpt_button = types.InlineKeyboardButton(
        text=f"{smile} YandexGPT",
        callback_data="switch_to_yandexgpt",
    )

    smile = "❌"
    if groups[message.chat.id].model == "lama":
        smile = "✅"
    lama_button = types.InlineKeyboardButton(
        text=templates["en"]["button_lama.txt"].format(smile=smile),
        callback_data="switch_to_lama",
    )

    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(gpt_4_button)
    customization_markup.add(gigachat_button)
    customization_markup.add(yandexgpt_button)
    customization_markup.add(gpt_35_turbo_button)
    customization_markup.add(vicuna_button)
    if str(message.chat.id) in developer_chat_IDs:
        customization_markup.add(lama_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["models.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=customization_markup,
        parse_mode="HTML",
    )


# ---------- Ahead functions ----------
# --- Switcher ---
@error_handler
def switch_model(message):
    model = message.model
    language_code = groups[message.chat.id].lang_code

    customization_markup = types.InlineKeyboardMarkup()

    groups[message.chat.id].model = model
    # --- Buttons ---
    smile = "❌"
    if groups[message.chat.id].model == "gpt-4":
        smile = "✅"
    gpt_4_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_gpt_4.txt"].format(smile=smile),
        callback_data="switch_to_gpt_4",
    )
    
    smile = "❌"
    if groups[message.chat.id].model == "gigachat":
        smile = "✅"
    gigachat_button = types.InlineKeyboardButton(
        text="{smile} Sber GigaChat".format(smile=smile),
        callback_data="switch_to_gigachat",
    )
    
    smile = "❌"
    if groups[message.chat.id].model == "yandexgpt":
        smile = "✅"
    yandexgpt_button = types.InlineKeyboardButton(
        text="{smile} YandexGPT".format(smile=smile),
        callback_data="switch_to_yandexgpt",
    )
    

    smile = "❌"
    if groups[message.chat.id].model == "gpt-3.5-turbo":
        smile = "✅"
    gpt_35_turbo_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_gpt35turbo.txt"].format(smile=smile),
        callback_data="switch_to_gpt35turbo",
    )

    smile = "❌"
    if groups[message.chat.id].model == "vicuna":
        smile = "✅"
    vicuna_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_vicuna.txt"].format(smile=smile),
        callback_data="switch_to_vicuna",
    )

    smile = "❌"
    if groups[message.chat.id].model == "lama":
        smile = "✅"
    lama_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_lama.txt"].format(smile=smile),
        callback_data="switch_to_lama",
    )

    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="settings",
    )

    # Adding buttons to keyboard
    customization_markup.add(gpt_4_button)
    customization_markup.add(gigachat_button)
    customization_markup.add(yandexgpt_button)
    customization_markup.add(gpt_35_turbo_button)
    customization_markup.add(vicuna_button)
    if str(message.chat.id) in developer_chat_IDs:
        customization_markup.add(lama_button)
    customization_markup.add(back_button)

    # Sending message with keyboard
    bot.edit_message_text(
        templates[language_code]["models.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=customization_markup,
        parse_mode="HTML",
    )
