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
            inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["change_owner_of_group_caanceled.txt"],
        )
        return
    
    if "@" in val:
        val = val[1:]
    
    get_user = groups[groups[inner_message.chat.id].owner_id].change_owner_of_group(val)

    if get_user == {}:
        bot.send_message(inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["user_unregistrated.txt"])
        return
    
    prev_owner = groups[inner_message.chat.id].owner_id
    new_owner = get_user["ChatID"]

    groups[prev_owner].id_groups.remove(inner_message.chat.id)

    groups[inner_message.chat.id].subscription = get_user["TypeOfSubscription"]
    groups[inner_message.chat.id].allowed_groups = get_user["NumAllowedGroups"]
    groups[inner_message.chat.id].tokens_limit = get_user["TokensTotal"]
    groups[inner_message.chat.id].dynamic_gen_permission = get_user["DYNAMIC_GENERATION"]
    groups[inner_message.chat.id].voice_input_permission = get_user["VOICE_INPUT"]
    groups[inner_message.chat.id].voice_output_permission = get_user["VOICE_OUTPUT"]
    groups[inner_message.chat.id].sphere_permission = get_user["SphereContext"]
    groups[inner_message.chat.id].temperature_permission = get_user["Temperature"]
    groups[inner_message.chat.id].frequency_penalty_permission = get_user["FrequencyPenalty"]
    groups[inner_message.chat.id].presense_penalty_permission = get_user["PresensePenalty"]
    groups[inner_message.chat.id].temporary_memory_size_limit = get_user["TemporaryMemorySize"]
    groups[inner_message.chat.id].owner_id = new_owner

    bot.send_message(inner_message.chat.id, groups[inner_message.chat.id].templates[language_code]["owner_waas_changed.txt"])
