from __main__ import *


# --- Enable ---
def enable(message):
    language_code = groups[message.chat.id].lang_code

    if message.chat.type == "private":
        groups[message.chat.id].enabled = True
        markup_commands = load_buttons(
            types,
            groups,
            message.chat.id,
            language_code,
            owner_id=groups[message.chat.id].owner_id,
        )
        groups[message.chat.id].trigger_probability = 1
        bot.reply_to(
            message,
            templates[language_code]["enabled_user.txt"],
            reply_markup=markup_commands,
            parse_mode="HTML",
        )
    else:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text=templates[language_code]["button_enable_auto.txt"],
            callback_data="auto_mode",
        )
        markup.add(button)
        button = types.InlineKeyboardButton(
            text=templates[language_code]["button_enable_dialog.txt"],
            callback_data="dialog_mode",
        )
        markup.add(button)
        button = types.InlineKeyboardButton(
            text=templates[language_code]["button_enable_manual.txt"],
            callback_data="manual_mode",
        )
        markup.add(button)

        bot.send_message(
            message.chat.id,
            templates[language_code]["enabled.txt"],
            reply_markup=markup,
            parse_mode="HTML",
        )


# --- Auto mode Enable ---
@error_handler
def choose_prob(message):
    language_code = groups[message.chat.id].lang_code

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="0.2",
        callback_data="choose-prob_0.2",
    )
    button2 = types.InlineKeyboardButton(
        text="0.4",
        callback_data="choose-prob_0.4",
    )
    button3 = types.InlineKeyboardButton(
        text="0.7",
        callback_data="choose-prob_0.7",
    )
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    bot.edit_message_text(
        templates[language_code]["choose_probability_in_buttons.txt"],
        message.chat.id,
        message.message_id,
        reply_markup=markup,
        parse_mode="HTML",
    )


def auto_enable(message, prob):
    language_code = groups[message.chat.id].lang_code

    groups[message.chat.id].enabled = True

    groups[message.chat.id].trigger_probability = prob

    markup_commands = load_buttons(
        types,
        groups,
        message.chat.id,
        language_code,
        owner_id=groups[message.chat.id].owner_id,
    )

    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(
        message.chat.id,
        templates[language_code]["enabled_auto.txt"].format(
            probability=groups[message.chat.id].trigger_probability
        ),
        reply_markup=markup_commands,
        parse_mode="HTML",
    )


# --- Dialog mode enable ---
@error_handler
def dialog_enable(message):
    groups[message.chat.id].enabled = True
    language_code = groups[message.chat.id].lang_code

    groups[message.chat.id].trigger_probability = 1

    markup_commands = load_buttons(
        types,
        groups,
        message.chat.id,
        language_code,
        owner_id=groups[message.chat.id].owner_id,
    )

    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(
        message.chat.id,
        templates[language_code]["enabled_dialog.txt"],
        reply_markup=markup_commands,
        parse_mode="HTML",
    )


# --- Manual mode enable ---
@error_handler
def manual_enable(message):
    groups[message.chat.id].enabled = True
    language_code = groups[message.chat.id].lang_code

    groups[message.chat.id].trigger_probability = 0

    markup_commands = load_buttons(
        types,
        groups,
        message.chat.id,
        language_code,
        owner_id=groups[message.chat.id].owner_id,
    )

    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(
        message.chat.id,
        templates[language_code]["enabled_manual.txt"],
        reply_markup=markup_commands,
        parse_mode="HTML",
    )


# --- Disable ---
@error_handler
def disable(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = False

    groups[message.chat.id].messages_history = []

    markup = load_buttons(
        types,
        groups,
        message.chat.id,
        language_code,
        owner_id=groups[message.chat.id].owner_id,
    )

    bot.send_message(message.chat.id, "😴", reply_markup=markup)
