from __main__ import *


# --- reply handler for feature requests ---
@error_handler
def change_language_reply_handler(inner_message):

    lang_code = check_language(inner_message.text)

    if not lang_code:
        bot.send_message(inner_message.chat.id, f"Sorry, the language '{inner_message.text}' is not supported or doesnt exist.")
        return

    language_code = lang_code[0]

    sent_message = bot.send_message(inner_message.chat.id, translate_text(language_code, "Loading... Please, wait a minute"))

    translate_templates(language_code)

    bot.delete_message(inner_message.chat.id, sent_message.message_id)

    markup = load_buttons(types, groups, chat_id, language_code, owner_id=owner_id)
    bot.send_message(inner_message.chat.id, templates[lang_code[0]]["language_applied.txt"], reply_markup=markup)
    groups[inner_message.chat.id].lang_code = lang_code[0]
    