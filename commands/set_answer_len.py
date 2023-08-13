from __main__ import *


# --- Set answers' length ---
@bot.message_handler(commands=["set_length_answer"], func=time_filter and member_filter)
@error_handler
def set_length_answer_command(message):
    language_code = groups[message.chat.id].lang_code

    length_markup = types.InlineKeyboardMarkup()

    long_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_long.txt"], callback_data="long"
    )
    medium_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_medium.txt"], callback_data="medium"
    )
    short_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_short.txt"], callback_data="short"
    )
    any_button = types.InlineKeyboardButton(
        text=groups[message.chat.id].templates[language_code]["button_any_length.txt"], callback_data="any"
    )

    length_markup.add(long_button)
    length_markup.add(medium_button)
    length_markup.add(short_button)
    length_markup.add(any_button)

    bot.reply_to(
        message,
        groups[message.chat.id].templates[language_code]["set_length_answer.txt"].format(
            presense_penalty=groups[message.chat.id].presense_penalty
        ),
        reply_markup=length_markup,
        parse_mode="HTML",
    )
