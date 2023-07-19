from __main__ import *


# --- Tokens info ---
@bot.message_handler(commands=["subs_list"], func=time_filter and member_filter)
@error_handler
def subs_list_command(message):
    language_code = groups[message.chat.id].lang_code

    bot.send_message(message.chat.id, templates[language_code]["sub_free_description.txt"], parse_mode = "HTML")
    bot.send_message(message.chat.id, templates[language_code]["sub_user_description.txt"], parse_mode = "HTML")
    bot.send_message(message.chat.id, templates[language_code]["sub_small_business_description.txt"], parse_mode = "HTML")
    bot.send_message(message.chat.id, templates[language_code]["sub_big_business_description.txt"], parse_mode = "HTML")
