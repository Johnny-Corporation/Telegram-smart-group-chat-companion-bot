from __main__ import *


# --- Set sphere of conservation ---
@bot.message_handler(commands=["set_sphere"], func=time_filter)
@error_handler
def set_sphere_command(message):
    language_code = groups[message.chat.id].lang_code
    if groups[message.chat.id].sphere == "":
        sphere_in = "Not set"
    else:
        sphere_in = groups[message.chat.id].sphere
    bot_reply = bot.reply_to(
        message,
        templates[language_code]["set_sphere.txt"].format(sphere=sphere_in),
        parse_mode="HTML",
    )
    reply_blacklist[message.chat.id].append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, set_sphere_reply_handler)
