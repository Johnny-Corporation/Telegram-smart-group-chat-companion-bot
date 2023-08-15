from __main__ import *


# --- view mode ---
@bot.message_handler(commands=["view_mode"], func=time_filter)
@error_handler
def view_mode(message):
    if groups[message.chat.id].enabled == True:
        on_off = "enabled"
        if groups[message.chat.id].trigger_probability == 1:
            mode = "dialog"
        elif groups[message.chat.id].trigger_probability == 0:
            mode = "manual"
        else:
            mode = "auto"

        language_code = groups[message.chat.id].lang_code
        bot.send_message(
            message.chat.id,
            groups[message.chat.id].templates[language_code]["view_mode.txt"].format(on_off=on_off, mode=mode),
        )

    else:
        language_code = groups[message.chat.id].lang_code
        bot.send_message(
            message.chat.id, groups[message.chat.id].templates[language_code]["view_mode_disabled.txt"]
        )
