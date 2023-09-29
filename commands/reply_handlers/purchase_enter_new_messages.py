from __main__ import *
from utils.yoomoney import *

# --- reply handler for set sphere
def enter_new_messages_reply_handler(inner_message):
    reply_blacklist[inner_message.chat.id].remove(inner_message.reply_to_message.message_id)
    language_code = groups[inner_message.chat.id].lang_code
    try:
        val = int(inner_message.text)

        if val <= 0:
            bot.reply_to(inner_message, "❌")
            bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
            return
        elif val > 1000000:
            bot.reply_to(inner_message, "❌")
            bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
            return

    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
        return
    
    
    #apply discounts
    for discount in groups[inner_message.chat.id].discount_message.values():
        if discount!=1:
            val = val * 1-discount
    


    if groups[inner_message.chat.id].subscription == "Free":

        accept_payment(inner_message, val*10, 'more_messages', inner_message.text) 

    elif groups[inner_message.chat.id].subscription == "Pro":

        accept_payment(inner_message, val*5, 'more_messages', inner_message.text)

    else:
        bot.send_message(inner_message.chat.id, "Problem")