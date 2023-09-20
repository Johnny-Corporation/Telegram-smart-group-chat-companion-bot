from __main__ import *


# --- reply handler for set probability
@error_handler
def set_probability_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_probability_declined.txt"],
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return
    if (val < 0) or (val > 1):
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_probability_declined.txt"],
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return

    groups[inner_message.chat.id].trigger_probability = val
    bot.send_message(
        inner_message.chat.id,
        "✅",
        reply_markup=load_buttons(
            types,
            groups,
            inner_message.chat.id,
            groups[inner_message.chat.id].lang_code,
            groups[inner_message.chat.id].owner_id,
        ),
    )

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)


# --- reply handler for set sphere
@error_handler
def set_sphere_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = str(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["sphere_declined.txt"]
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return

    groups[inner_message.chat.id].sphere = val

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)

    groups[inner_message.chat.id].set_sphere_waiting_message_to_edit_edit_func(
        groups[inner_message.chat.id].set_sphere_waiting_message_to_edit
    )


# --- reply handler for set presense penalty
@error_handler
def set_presence_penalty_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_creativity_declined.txt"],
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return
    if val < 0 or val > 2:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id,
            templates[language_code]["set_creativity_declined.txt"],
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return

    groups[inner_message.chat.id].presence_penalty = val
    bot.reply_to(inner_message, "✅")

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)


# --- reply handler for set frequency penalty
@error_handler
def set_frequency_penalty_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = float(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["set_variety_declined.txt"]
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return
    if val < 0 or val > 2:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["set_variety_declined.txt"]
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return

    groups[inner_message.chat.id].frequency_penalty = val
    bot.reply_to(inner_message, "✅")

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)


# --- reply handler for set temp memory size
@error_handler
def set_memory_size_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["set_memory_declined.txt"]
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return
    if val <= 0:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["set_memory_declined.txt"]
        )
        bot.clear_reply_handlers_by_message_id(
            inner_message.reply_to_message.message_id
        )
        return

    if groups[inner_message.chat.id].temporary_memory_size_limit >= val:
        groups[inner_message.chat.id].change_memory_size = val
        bot.reply_to(inner_message, "✅")

    else:
        bot.reply_to(
            inner_message, templates[language_code]["no_rights.txt"], parse_mode="HTML"
        )

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
