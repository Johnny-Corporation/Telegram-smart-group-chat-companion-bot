from __main__ import *


# --- Report bug ---
@bot.message_handler(commands=["report_bug"], func=time_filter and member_filter)
@error_handler
def report_bug_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, groups[message.chat.id].templates[language_code]["report_bug.txt"])
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, bug_report_reply_handler)
