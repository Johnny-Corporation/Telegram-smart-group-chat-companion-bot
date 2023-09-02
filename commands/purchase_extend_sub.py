from __main__ import *


# --- set_up functions ---
@error_handler
def extend_sub(message):

    language_code = groups[message.chat.id].lang_code

    #create price with all allowed discounts
    price = 999
    for discount in groups[message.chat.id].discount_subscription.values():
        price = price * discount

    accept_payment(message, price, 'extend')
