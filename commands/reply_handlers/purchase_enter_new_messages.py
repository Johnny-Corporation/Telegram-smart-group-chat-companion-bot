from __main__ import *
from utils.yoomoney import *

# --- reply handler for set sphere
@error_handler
def enter_new_messages_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["new_messages_calnceled.txt"]
        )
        return
    

    

    if groups[inner_message.chat.id].subscription == "Free":

        print(val)

        accept_payment(inner_message, templates[language_code]["messages_buy_text.txt"].format(val=val,sub="Free"), val*5, 'more_messages') 

    elif groups[inner_message.chat.id].subscription == "USER":

        accept_payment(inner_message, templates[language_code]["messages_buy_text.txt"].format(val=val,sub="USER"), val*4.5, 'more_messages')

    elif groups[inner_message.chat.id].subscription == "SMALL BUSINESS":

        accept_payment(inner_message, templates[language_code]["messages_buy_text.txt"].format(val=val,sub="SMALL BUSINESS"), val*3.5, 'more_messages')

    elif groups[inner_message.chat.id].subscription == "BIG BUSINESS":

        accept_payment(inner_message, templates[language_code]["messages_buy_text.txt"].format(val=val,sub="BIG BUSINESS"), val*3, 'more_messages')
    else:
        bot.send_message(inner_message.chat.id, "Problem")