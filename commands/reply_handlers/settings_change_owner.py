from __main__ import *


# --- reply handler for enter promocode
@error_handler
def change_owner_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    
    try:
        val = str(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["change_owner_of_group_caanceled.txt"],
        )
        return
    
    if "@" in val:
        val = val[1:]
    
    get_user = groups[groups[inner_message.chat.id].owner_id].change_owner_of_group(val)

    if get_user == {}:
        bot.send_message(inner_message.chat.id, templates[language_code]["user_unregistrated.txt"])
        return
    
    prev_owner = groups[inner_message.chat.id].owner_id
    new_owner = get_user["ChatID"]

    groups[prev_owner].id_groups.remove(inner_message.chat.id)
    groups[new_owner].characteristics_of_sub = {}
    groups[chat_id].subscription = groups[new_owner].subscription
    characteristics_of_sub = take_info_about_sub(groups[chat_id].subscription)
    groups[chat_id].characteristics_of_sub[groups[chat_id].subscription] = characteristics_of_sub
    groups[inner_message.chat.id].owner_id = new_owner

    bot.send_message(inner_message.chat.id, templates[language_code]["owner_was_changed.txt"])
