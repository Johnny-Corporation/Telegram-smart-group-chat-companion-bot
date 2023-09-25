from __main__ import *


# --- reply handler for enter promocode
# @error_handler
def change_owner_reply_handler(inner_message):
    language_code = groups[inner_message.chat.id].lang_code
    
    try:
        val = str(inner_message.text)
    except ValueError:
        bot.reply_to(inner_message, "❌")
        bot.send_message(
            inner_message.chat.id, templates[language_code]["change_owner_of_group_caanceled.txt"],
        )
        bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
        return


    if groups[inner_message.chat.id].owner_id != inner_message.from_user.id:
        bot.send_message(inner_message.chat.id, templates[language_code]["settings_owner_can_change.txt"])
        bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
        return

    if "@" in val:
        val = val[1:]
    
    get_user = groups[groups[inner_message.chat.id].owner_id].change_owner_of_group(val)

    if get_user == {}:
        bot.send_message(inner_message.chat.id, templates[language_code]["user_unregistrated.txt"])
        bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
        return

    new_owner = get_user["ChatID"]

    prev_owner = groups[inner_message.chat.id].owner_id

    groups[prev_owner].id_groups.remove(inner_message.chat.id)
    groups[inner_message.chat.id].characteristics_of_sub = {}
    groups[inner_message.chat.id].subscription = groups[new_owner].subscription
    characteristics_of_sub = take_info_about_sub(groups[inner_message.chat.id].subscription)
    groups[inner_message.chat.id].characteristics_of_sub[groups[inner_message.chat.id].subscription] = characteristics_of_sub
    groups[inner_message.chat.id].owner_id = new_owner
    groups[new_owner].id_groups.append(inner_message.chat.id)

    bot.send_message(inner_message.chat.id, templates[language_code]["owner_was_changed.txt"])

    # bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)
