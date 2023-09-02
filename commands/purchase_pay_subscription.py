from __main__ import *


# ---------- Pay Subscription message ----------

def rus_payment(message, type_of_sub):

    language_code = groups[message.chat.id].lang_code

    type_of_sub == "pro"

    #create price with all allowed discounts
    price = 999
    for discount in groups[message.chat.id].discount_subscription.values():
        price = price * discount
    

    accept_payment(message, price)
