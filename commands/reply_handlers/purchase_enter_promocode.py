from __main__ import *


# --- reply handler for enter promocode
@error_handler
def enter_promocode_reply_handler(inner_message):

    language_code = groups[inner_message.chat.id].lang_code
    
    try:
        val = str(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["enter_promocode_canceled.txt"]
        )
        bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
        return
    
    code_back = check_code(promocodes, inner_message.text)
    
    if len(code_back) == 3:

        if code_back[0]>=1:
            groups[inner_message.chat.id].add_purchase_of_messages(inner_message.chat.id, code_back[0])

            bot.send_message(inner_message.chat.id, templates[language_code]["more_100000_messages.txt"].format(messages=groups[inner_message.chat.id].characteristics_of_sub[groups[inner_message.chat.id].subscription]["messages_limit"]))
            
            promocodes[code_back[-1]] = generate_code()
        elif code_back[0]<1:

            print(f"INTERESTING SITUATION:   {code_back[1]}")

            if code_back[1] == 'messages':
                groups[inner_message.chat.id].discount_message["Promocode discount"] = code_back[0]
            elif code_back[1] == 'subscription':
                groups[inner_message.chat.id].discount_subscription["Promocode discount"] = code_back[0]
            else:
                print('ELSE ELSE ELSE ELSE ELSE ELSE')
                groups[inner_message.chat.id].discount_subscription["Promocode discount"] = code_back[0]
                groups[inner_message.chat.id].discount_message["Promocode discount"] = code_back[0]

            bot.send_message(inner_message.chat.id, templates[language_code]["promocode_discount_50.txt"].format(type_=code_back[1]))

            # if code_back[-1] != 'JOHNNY':
            #     promocodes[code_back[-1]] = generate_code()


    elif len(code_back) == 4:
        groups[inner_message.chat.id].add_new_user(inner_message.chat.id, inner_message.from_user.first_name, inner_message.from_user.last_name, inner_message.from_user.username, code_back[0], code_back[1])
        groups[inner_message.chat.id].load_subscription(inner_message.chat.id)

        for group_id in groups[inner_message.chat.id].id_groups:
            groups[group_id].subscription = groups[inner_message.chat.id].subscription
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["messages_limit"] = groups[inner_message.chat.id].characteristics_of_sub[groups[inner_message.chat.id].subscription]["messages_limit"]
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["dynamic_gen_permission"] = groups[inner_message.chat.id].characteristics_of_sub[groups[inner_message.chat.id].subscription]["dynamic_gen_permission"]
            groups[group_id].characteristics_of_sub[groups[group_id].subscription]["voice_output_permission"] = groups[inner_message.chat.id].characteristics_of_sub[groups[inner_message.chat.id].subscription]["voice_output_permission"]

        groups[inner_message.chat.id].track_sub(inner_message.chat.id, new=True)

        promocodes[code_back[-1]] = generate_code()

    else:
        bot.send_message(
            inner_message.chat.id, templates[language_code]["promocode_incorrect.txt"]
        )

    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)

    

    