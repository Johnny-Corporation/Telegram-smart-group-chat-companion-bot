from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["set_up"], func=time_filter and member_filter)
@error_handler
def set_up_command(message):
    language_code = groups[message.chat.id].lang_code

    set_up_markup = types.InlineKeyboardMarkup()

    # --- Buttons ---
    temp_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_temp.txt"],
        callback_data="temperature",
    )
    answer_probability_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_ans.txt"],
        callback_data="answer_probability",
    )
    memory_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_memory.txt"],
        callback_data="memory_length",
    )
    if message.chat.id < 0:
        owner_button = types.InlineKeyboardButton(
            text="Change owner of group",
            callback_data="change_owner",
        )
        set_up_markup.add(owner_button)
    freq_penalty_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_variety.txt"],
        callback_data="variety",
    )
    pres_penalty_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_creativity.txt"],
        callback_data="creativity",
    )
    len_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_length_answer.txt"],
        callback_data="answer_length",
    )
    sphere_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_set_sphere.txt"],
        callback_data="sphere",
    )

    # Adding buttons to keyboard
    set_up_markup.add(temp_button)
    set_up_markup.add(answer_probability_button)
    set_up_markup.add(memory_button)
    set_up_markup.add(freq_penalty_button)
    set_up_markup.add(pres_penalty_button)
    set_up_markup.add(len_button)
    set_up_markup.add(sphere_button)

    # Seconding keyboard
    bot.send_message(
        message.chat.id,
        groups[message.chat.id].templates[language_code]["set_up_functions.txt"],
        reply_markup=set_up_markup,
        parse_mode="HTML",
    )
