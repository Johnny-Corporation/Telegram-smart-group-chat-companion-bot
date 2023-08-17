from __main__ import *
from utils.functions_for_developers import *


def reply_keyboard_buttons_handler(message, commands):

    if message.chat.id<0:

        print(commands)

        
        if groups[message.chat.id].activated == False:
            print(commands)
            if message.text == commands[0]:
                send_welcome_text_and_load_data(message.chat.id, message.from_user.id, groups[message.chat.id].lang_code)
                return
            elif message.text == commands[1]:
                about(message)
                return
            else:
                return

        i = 2
        if groups[message.chat.id].enabled==True:
            i = 4
 
        if message.text == commands[0]:
            if groups[message.chat.id].enabled==False:
                enable(message)
            else:
                clean_memory(message)
                disable(message)
            return True

        elif message.text == commands[1]:
            question_to_bot(message)
            return True
        
        elif message.text == commands[2] and i == 4:
            view_mode(message)
            return True
        
        elif message.text == commands[3] and i == 4:
            change_mode(message)
            return True
        
        elif message.text == commands[i]:
            group(message)
            return True

        elif message.text == commands[i+1]:
            settings(message)
            return True

        elif message.text == commands[i+2]:
            report_bug(message)
            return True

        elif message.text == commands[i+3]:
            request_feature(message)
            return True

        # elif message.text == commands[12]:
        #     support_us_command(message)
        #     return True
        
    elif message.chat.id>0:

        if message.text == commands[0]:
            if groups[message.chat.id].enabled==False:
                enable(message)
                return True
            else:
                clean_memory(message)
                return True

        elif message.text == commands[1]:
            question_to_bot(message)
            return True

        elif message.text == commands[2]:
            account(message)
            return True

        elif message.text == commands[3]:
            settings(message)
            return True

        elif message.text == commands[4]:
            report_bug(message)
            return True

        elif message.text == commands[5]:
            request_feature(message)
            return True

        # elif message.text == commands[9]:
        #     support_us_command(message)
        #     return True
    
    return False
