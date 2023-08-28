from __main__ import *


# --- Set sphere of conversation ---
@error_handler
def enter_purchase_of_messages(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.edit_message_text(
        message,
        templates[language_code]["enter_new_messages.txt"],
        parse_mode="HTML",
    )

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, enter_new_messages_reply_handler)
