from __main__ import *


# --- reply handler for feature requests ---
@error_handler
def change_language_reply_handler(inner_message):
    if isinstance(inner_message, list):
        chat_id = inner_message[0]
        text = inner_message[1]
    else:
        chat_id = inner_message.chat.id
        text = inner_message.text

    lang_codes = text.split(",")
    for lc in lang_codes:
        lang_code = check_language(lc)

        if not lang_code:
            bot.send_message(
                chat_id,
                f"Sorry, the language '{lc}' is not supported or doesnt exist.",
            )
            continue

        language_code = lang_code[0]

        bot.send_message(
            chat_id,
            translate_text(language_code, "Loading... Please, wait a minute"),
        )

        translate_templates(language_code)

        bot.send_message(chat_id, "💛")
