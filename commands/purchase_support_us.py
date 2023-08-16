"""Now that's draft"""

from __main__ import *


# --- Dynamic generation ---
@bot.message_handler(commands=["support_us"], func=time_filter)
@error_handler
def support_us_command(message):
    
    language_code = groups[message.chat.id].lang_code
    bot_reply = bot.send_message(message.chat.id, templates[language_code]["how_much_money.txt"], parse_mode="HTML")

    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, support_us_reply_handler)
