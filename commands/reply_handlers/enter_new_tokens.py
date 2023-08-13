from __main__ import *
from commands.yoomoney import *

# --- reply handler for set sphere
@error_handler
def enter_new_tokens_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["new_tokens_calnceled.txt"]
        )
        return
    

    

    if groups[inner_message.chat.id].subscription == "Free":

        pay = accept_payment(inner_message, groups[inner_message.chat.id].templates[language_code]["tokens_buy_text.txt"].format(val=val,sub="Free"), val*0.0004) 

    elif groups[inner_message.chat.id].subscription == "USER":

        pay = accept_payment(inner_message, groups[inner_message.chat.id].templates[language_code]["tokens_buy_text.txt"].format(val=val,sub="USER"), val*0.0003)

    elif groups[inner_message.chat.id].subscription == "SMALL BUSINESS":

        pay = accept_payment(inner_message, groups[inner_message.chat.id].templates[language_code]["tokens_buy_text.txt"].format(val=val,sub="SMALL BUSINESS"), val*0.00025)

    elif groups[inner_message.chat.id].subscription == "BIG BUSINESS":

        pay = accept_payment(inner_message, groups[inner_message.chat.id].templates[language_code]["tokens_buy_text.txt"].format(val=val,sub="BIG BUSINESS"), val*0.00023)
    else:
        bot.send_message(inner_message.chat.id, "Problem")

    if pay:
        groups[inner_message.chat.id].add_purchase_of_tokens(
            inner_message.chat.id,
            val
        )
        groups[inner_message.chat.id].tokens_limit = groups[inner_message.chat.id].groups[inner_message.chat.id].tokens_limit + val

        for group in groups[inner_message.chat.id].id_groups:
            groups[group].tokens_limit = groups[inner_message.chat.id].tokens_limit

        bot.send_message(
            inner_message.chat.id,
            groups[message.chat.id].templates[language_code]["new_tokens.txt"],
            parse_mode="HTML",
        )
    else:
        bot.send_message(inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["buy_was_canceled.txt"])