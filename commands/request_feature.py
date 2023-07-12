from __main__ import *


# --- Request feature ---
@bot.message_handler(commands=["request_feature"], func=time_filter)
@error_handler
def request_feature_command(message):
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.reply_to(message, templates[language_code]["request_feature.txt"])
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, feature_request_reply_handler)
