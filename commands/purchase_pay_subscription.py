from __main__ import *


# ---------- Pay Subscription message ----------

def rus_payment(message, type_of_sub):

    language_code = groups[message.chat.id].lang_code

    if type_of_sub == "free_sub":

        #Add user to db
        groups[message.chat.id].add_new_user(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'SMALL BUSINESS (trial)', 50)
        #Load and apply parameteres from db
        groups[message.chat.id].load_subscription(message.chat.id)
        #Apply new parameters to all groups
        for group_id in groups[message.chat.id].id_groups:
            groups[group_id].subscription = groups[message.chat.id].subscription
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["messages_limit"] = groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"]
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["dynamic_gen_permission"] = groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["dynamic_gen_permission"]
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["voice_output_permission"] = groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["voice_output_permission"]

        groups[message.chat.id].track_sub(message.chat.id, new=True)

    elif type_of_sub == "easy":

        price = 399

        # --- Discount ---
        if groups[message.chat.id].total_spent_messages <= 20 and groups[message.chat.id].subscription == "Free":
            bot.send_message(message.chat.id, templates[language_code]["discount_yes.txt"])
            price = price * 0.8

        accept_payment(message, "You buy USER subscription", price)

    elif type_of_sub == "middle":

        price = 799

        # --- Discount ---
        if groups[message.chat.id].total_spent_messages <= 20 and groups[message.chat.id].subscription == "Free":
            bot.send_message(message.chat.id, templates[language_code]["discount_yes.txt"])
            price = price * 0.8

        accept_payment(message, "You buy SMALL BUSINESS subscription", price)

    elif type_of_sub == "pro":

        price = 1899

        # --- Discount ---
        if groups[message.chat.id].total_spent_messages <= 20 and groups[message.chat.id].subscription == "Free":
            bot.send_message(message.chat.id, templates[language_code]["discount_yes.txt"])
            price = price * 0.8

        accept_payment(message, "You buy BIG BUSINESS subscription", price)
