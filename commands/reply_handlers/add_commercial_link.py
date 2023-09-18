from __main__ import *


# --- reply handler for bug reports ---
@error_handler
def add_commercial_link_reply_handler(inner_message):

    language_code = groups[inner_message.chat.id].lang_code

    # try:
    username = inner_message.text.split(";")[0]
    num_of_messages = inner_message.text.split(";")[1]

    commercial_links[username] = int(num_of_messages)

    for group in groups:
        groups[group].commercial_links[username] = int(num_of_messages)
    # except:
    #     bot.send_message(inner_message.chat.id, "ERROR")