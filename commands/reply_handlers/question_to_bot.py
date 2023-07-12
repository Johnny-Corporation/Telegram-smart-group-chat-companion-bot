from __main__ import *


# --- reply handler for question to bot
@error_handler
def question_to_bot_reply_handler(inner_message):
    bot.reply_to(inner_message, groups[inner_message.chat.id].one_answer(inner_message))
