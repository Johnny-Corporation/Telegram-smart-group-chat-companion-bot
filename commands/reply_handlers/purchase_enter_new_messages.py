from __main__ import *
from utils.yoomoney import *

# --- reply handler for set sphere
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

        accept_payment(inner_message, val*10, 'more_messages', val) 

    elif groups[inner_message.chat.id].subscription == "Pro":

        accept_payment(inner_message, val*5, 'more_messages', val)

    else:
        bot.send_message(inner_message.chat.id, "Problem")