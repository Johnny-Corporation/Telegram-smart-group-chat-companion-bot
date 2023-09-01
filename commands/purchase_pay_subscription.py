from __main__ import *


# ---------- Pay Subscription message ----------

def rus_payment(message, type_of_sub):

    language_code = groups[message.chat.id].lang_code

    type_of_sub == "pro"

    price = 999

    # --- Discount ---
    if groups[message.chat.id].total_spent_messages <= 15 and groups[message.chat.id].subscription == "Free":
        bot.send_message(message.chat.id, templates[language_code]["discount_yes.txt"])
        price = price * 0.8

    accept_payment(message, price)
