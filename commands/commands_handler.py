from __main__ import *
from utils.functions_for_developers import *


def reply_keyboard_buttons_handler(message, commands):

    if message.chat.id<0:

        if message.text == commands[0]:
            if groups[message.chat.id].enabled==False:
                enable_command(message)
            else:
                disable_command(message)
            return True

        elif message.text == commands[1]:
            question_to_bot_command(message)
            return True

        elif message.text == commands[2]:
            clean_memory_command(message)
            return True

        elif message.text == commands[3]:
            if groups[message.chat.id].trigger_probability>0:
                dialog_enable_command(message)
                return True
            else:
                dialog_disable_command(message)
                return True

        elif message.text == commands[4]:
            if groups[message.chat.id].trigger_probability>0:
                manual_enable_command(message)
                return True
            else:
                manual_disable_command(message)
                return True
        
        elif message.text == commands[5]:
            view_mode_command(message)
            return True
        
        elif message.text == commands[6]:
            group_info_command(message)
            return True

        elif message.text == commands[7]:
            account_info_command(message)
            return True

        elif message.text == commands[8]:
            settings_command(message)
            return True

        elif message.text == commands[9]:
            purchase(message)
            return True

        elif message.text == commands[10]:
            report_bug_command(message)
            return True

        elif message.text == commands[11]:
            request_feature_command(message)
            return True

        # elif message.text == commands[12]:
        #     support_us_command(message)
        #     return True
        
    elif message.chat.id>0:

        if message.text == commands[0]:
            question_to_bot_command(message)
            return True

        elif message.text == commands[1]:
            clean_memory_command(message)
            return True

        elif message.text == commands[2]:
            if groups[message.chat.id].trigger_probability>0:
                manual_enable_command(message)
                return True
            else:
                manual_disable_command(message)
                return True
        
        elif message.text == commands[3]:
            view_mode_command(message)
            return True

        elif message.text == commands[4]:
            account_info_command(message)
            return True

        elif message.text == commands[5]:
            settings_command(message)
            return True

        elif message.text == commands[6]:
            purchase(message)
            return True

        elif message.text == commands[7]:
            report_bug_command(message)
            return True

        elif message.text == commands[8]:
            request_feature_command(message)
            return True

        # elif message.text == commands[9]:
        #     support_us_command(message)
        #     return True
    
    return False
