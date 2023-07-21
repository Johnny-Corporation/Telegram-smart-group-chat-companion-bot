from __main__ import *


# --- Question to bot  ------
@bot.message_handler(commands=["question_to_bot"], func=time_filter and member_filter)
@error_handler
def question_to_bot_command(message):
    language_code = groups[message.chat.id].lang_code

    bot_reply = bot.reply_to(message, groups[message.chat.id].templates[language_code]["question_to_bot.txt"])
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, question_to_bot_reply_handler)
