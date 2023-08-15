from __main__ import *


# --- set_up functions ---
@error_handler
def extend_sub(message):

    if groups[message.chat.id].subscription == "USER":
        pay = accept_payment(message, "You buy USER subscription", 399)
    elif groups[message.chat.id].subscription == "SMALL BUSINESS":
        pay = accept_payment(message, "You buy SMALL BUSINESS subscription", 699)
    elif groups[message.chat.id].subscription == "BIG BUSINESS":
        pay = accept_payment(message, "You buy BIG BUSINESS subscription", 1299)  
    else:
        bot.send_message(message.chat.id, "Problem")
        pay = False

    if pay:
        groups[message.chat.id].extend_sub(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
        groups[message.chat.id].track_sub(message.chat.id, new=True)
    else:
        bot.send_message(message.chat.id, groups[message.chat.id].templates[previous_language_code]["buy_was_canceled.txt"])