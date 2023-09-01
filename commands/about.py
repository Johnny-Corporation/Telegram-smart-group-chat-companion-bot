from __main__ import *


# --- About ---
@bot.message_handler(commands=["about"], func=time_filter)
# @error_handler
def about(message, back_from=False):
    language_code = groups[message.chat.id].lang_code

    if not back_from:
        bot.reply_to(
            message,
            templates[language_code]["description.txt"].format(
                probability=groups[message.chat.id].trigger_probability
            ),
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        return

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(
        text="<<<",
        callback_data="menu",
    )
    markup.add(back_button)

    bot.edit_message_text(
        templates[language_code]["description.txt"].format(
            probability=groups[message.chat.id].trigger_probability
        ),
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
