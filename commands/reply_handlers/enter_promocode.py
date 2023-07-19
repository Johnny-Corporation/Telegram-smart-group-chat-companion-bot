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
        return
    
    code_back = check_code(inner_message.text)
    
    if len(code_back) == 1:
        groups[inner_message.chat.id].add_purchase_of_tokens(inner_message.chat.id, code_back[0])

        bot.send_message(inner_message.chat.id, templates[language_code]["more_100000_tokens.txt"].format(tokens=groups[inner_message.chat.id].tokens_limit))

    elif len(code_back) == 11:
        groups[inner_message.chat.id].add_new_user(inner_message.chat.id, inner_message.from_user.first_name, inner_message.from_user.last_name, inner_message.from_user.username, code_back[0], code_back[1], code_back[2], code_back[3], code_back[4], code_back[5], code_back[6], code_back[7], code_back[8], code_back[9], code_back[10])
        groups[inner_message.chat.id].load_subscription(inner_message.chat.id)
        for group_id in groups[inner_message.chat.id].id_groups:
            groups[group_id].subscription = groups[inner_message.chat.id].subscription
            grops[group_id].tokens_limit = groups[inner_message.chat.id].tokens_limit
            groups[group_id].dynamic_gen_permission = groups[inner_message.chat.id].dynamic_gen_permission
            groups[group_id].voice_input_permission = groups[inner_message.chat.id].voice_input_permission
            groups[group_id].voice_output_permission = groups[inner_message.chat.id].voice_output_permission

        groups[inner_message.chat.id].track_sub(inner_message.chat.id, new=True)

    else:
        bot.send_message(
            inner_message.chat.id, templates[language_code]["promocode_incorrect.txt"]
        )
        return

    

    