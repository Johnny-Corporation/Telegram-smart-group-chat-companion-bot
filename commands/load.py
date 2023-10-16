from __main__ import *


# --- Help ---
@bot.message_handler(commands=["load", "help"], func=time_filter)
@error_handler
def help(message):

    if groups[message.chat.id].activated == False:
        change_language(message.chat.id)

    language_code = groups[message.chat.id].lang_code
    markup = load_buttons(
        types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id
    )

    bot.send_message(message.chat.id, templates[language_code]["load.txt"], parse_mode="HTML", reply_markup=markup)