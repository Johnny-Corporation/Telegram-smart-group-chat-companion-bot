from __main__ import *


# --- set_up functions ---
@error_handler
def extend_sub(message):

    language_code = groups[message.chat.id].lang_code

    if groups[message.chat.id].subscription == "USER":
        accept_payment(message, "You buy USER subscription", 399)
    elif groups[message.chat.id].subscription == "SMALL BUSINESS" or groups[message.chat.id].subscription == "SMALL BUSINESS (trial)":
        accept_payment(message, "You buy SMALL BUSINESS subscription", 699)
    elif groups[message.chat.id].subscription == "BIG BUSINESS":
        accept_payment(message, "You buy BIG BUSINESS subscription", 1299)  
    else:
        bot.send_message(message.chat.id, "Problem")