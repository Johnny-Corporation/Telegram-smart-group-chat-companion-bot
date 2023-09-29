from __main__ import *


# --- reply handler for bug reports ---
# @error_handler
def add_promocode_reply_handler(inner_message):

    language_code = groups[inner_message.chat.id].lang_code

    try:

        if inner_message.text=='sub':

            promocodes[f"sub"] = generate_code()
            if len(form)==2:
                form = inner_message.text.split("_")
                promocodes[f"sub"] = form[1]
            bot.send_message(inner_message.chat.id, "Your sub promocode was added")
            return

        form = inner_message.text.split("_")

        if {form[0]} == 'discount':
            try: 
                num = float(form[0])
                if num > 100:
                    bot.send_message(inner_message.chat.id, f"Discount more 100%?!?!")
            except:
                bot.send_message(inner_message.chat.id, f"Incorrect type of sub")
                return
            

        promocodes[f"{form[0]}_{form[1]}_{form[2]}"] = generate_code()
        if len(form)==4:
            promocodes[f"{form[0]}_{form[1]}_{form[2]}"] = form[3]
        bot.send_message(inner_message.chat.id, f"Your {form[0]} promocode was added")
        return

    except:

        bot.send_message(inner_message.chat.id, 'incorrect format')

    # --- reply handler for bug reports ---
# @error_handler
def delete_promocode_reply_handler(inner_message):

    language_code = groups[inner_message.chat.id].lang_code

    if inner_message.text in promocodes:
        promocodes.pop(inner_message.text, None)

        bot.send_message(inner_message.chat.id, f"Promocode {inner_message.text} was deleted")

    else:
        bot.send_message(inner_message.chat.id, 'There isnt such promocode')