from __main__ import *
from utils.functions_for_developers import *


def reply_keyboard_buttons_handler(message, commands):
    groups[
        message.chat.id
    ].busy = False  # When resetting memory for example if lama didn't answer for some reason we need to reset busy status each button press to keep Johnny alive
    if message.chat.id < 0:
        (commands)

        if groups[message.chat.id].activated == False:
            (commands)
            if message.text == commands[0]:
                send_welcome_text_and_load_data(
                    message,
                    message.chat.id,
                    message.from_user.id,
                    groups[message.chat.id].lang_code,
                )
                return
            elif message.text == commands[1]:
                about(message)
                return
            else:
                return

        i = 1
        if groups[message.chat.id].enabled == True:
            i = 3
        if message.text == commands[0]:
            if groups[message.chat.id].enabled == False:
                enable(message)
            else:
                clean_memory(message)
                disable(message)
            return True

        elif message.text == commands[i]:
            menu(message)
            return True

        elif message.text == commands[1] and i == 3:
            change_mode(message)
            return True
        elif message.text == commands[2] and i == 3:
            groups[message.chat.id].messages_history.clear()
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "✅")

    elif message.chat.id > 0:
        if message.text == commands[0]:
            if groups[message.chat.id].enabled == False:
                enable(message)
                return True
            else:
                clean_memory(message)
                return True

        elif message.text == commands[1]:
            menu(message)
            return True

    return False
