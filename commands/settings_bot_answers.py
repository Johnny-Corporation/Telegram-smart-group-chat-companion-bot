from __main__ import *



# ---------- Main message ----------

@bot.message_handler(commands=["bot_answers_settings"], func=time_filter)
@error_handler
def bot_answers_settings(message):
    language_code = groups[message.chat.id].lang_code


    # --- Buttons ---

    set_up_markup = types.InlineKeyboardMarkup()

    #probability
    if message.chat.id<0:
        answer_probability_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_set_ans.txt"],
            callback_data="answer_probability",
        )
        set_up_markup.add(answer_probability_button)

    #temperature
    temp_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_temp.txt"],
        callback_data="temperature",
    )

    #length of bot memory
    memory_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_memory.txt"],
        callback_data="memory_length",
    )

    #frequency_penalty
    freq_penalty_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_variety.txt"],
        callback_data="variety",
    )

    #presence penalty
    pres_penalty_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_creativity.txt"],
        callback_data="creativity",
    )

    #length of bot's answers
    len_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_length_answer.txt"],
        callback_data="answer_length",
    )

    #sphere of conservation
    sphere_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_set_sphere.txt"],
        callback_data="sphere",
    )

    #Back to settings
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="back_to_settings",
    )

    # Adding buttons to keyboard
    set_up_markup.add(sphere_button)
    set_up_markup.add(freq_penalty_button, pres_penalty_button)
    set_up_markup.add(memory_button, temp_button)
    set_up_markup.add(len_button)
    set_up_markup.add(back_button)
    
    

    # --- Edit 'Settings' message ---
    bot.edit_message_text(
        templates[language_code]["set_up_functions.txt"], 
        message.chat.id, 
        message.message_id, 
        reply_markup=set_up_markup,
        parse_mode="HTML",)
    



# ---------- From buttons messages ----------

# --- Set probability ---
@error_handler
def set_probability(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["change_probability.txt"].format(
            probability=groups[message.chat.id].trigger_probability
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_probability_reply_handler)


# --- Set temp ---
@error_handler
def set_temperature(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["change_temp.txt"].format(
            temperature=groups[message.chat.id].temperature
        ),
        parse_mode="HTML",
    )
    bot.register_for_reply(bot_reply, set_temp_reply_handler)


# --- Set memory size ---
@error_handler
def set_temp_memory_size(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["change_temp_memory_size.txt"].format(
            memory=groups[message.chat.id].temporary_memory_size
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_memory_size_reply_handler)


# --- Set frequency penalty (variety of answers) ---
@error_handler
def set_frequency_penalty(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["set_frequency_penalty.txt"].format(
            frequency_penalty=groups[message.chat.id].frequency_penalty
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_frequency_penalty_reply_handler)


# --- Set presence penalty (creativity of answers) ---
@error_handler
def set_presence_penalty(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["set_presence_penalty.txt"].format(
            frequency_penalty=groups[message.chat.id].frequency_penalty
        ),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_presence_penalty_reply_handler)


# --- Set answers' length ---
@error_handler
def set_length_answer_command(message):
    language_code = groups[message.chat.id].lang_code

    length_markup = types.InlineKeyboardMarkup()

    long_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_long.txt"], callback_data="long"
    )
    medium_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_medium.txt"], callback_data="medium"
    )
    short_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_short.txt"], callback_data="short"
    )
    any_button = types.InlineKeyboardButton(
        text=templates[language_code]["button_any_length.txt"], callback_data="any"
    )

    length_markup.add(long_button)
    length_markup.add(medium_button)
    length_markup.add(short_button)
    length_markup.add(any_button)

    bot.reply_to(
        message,
        templates[language_code]["set_length_answer.txt"],
        reply_markup=length_markup,
        parse_mode="HTML",
    )


# --- Set sphere of conservation ---
@error_handler
def set_sphere_command(message):
    language_code = groups[message.chat.id].lang_code
    if groups[message.chat.id].sphere == "":
        sphere_in = "Not set"
    else:
        sphere_in = groups[message.chat.id].sphere
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["set_sphere.txt"].format(sphere=sphere_in),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_sphere_reply_handler)
