from __main__ import *


# --- reply handler for feature requests ---
@error_handler
def feature_request_reply_handler(inner_message):

    reply_blacklist[inner_message.chat.id].remove(inner_message.reply_to_message.message_id)
    bot.clear_reply_handlers_by_message_id(inner_message.reply_to_message.message_id)

    language_code = groups[inner_message.chat.id].lang_code
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} (@{user.username}) 
            from group with name {inner_message.chat.title} requested a feature! 
            Here is what he said: 
            {inner_message.text}""",
        bot,
        developer_chat_IDs,
    )
    bot.reply_to(
        inner_message,
        templates[language_code]["feature_request_thanks.txt"],
    )
