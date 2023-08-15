from __main__ import *


# --- Enable ---
@bot.message_handler(commands=["enable"], func=time_filter)
@error_handler
def enable(message):
    language_code = groups[message.chat.id].lang_code


    if message.chat.type != "private":

        if not check_file_existing(message.from_user.first_name,"output\\clients_info"):
            return
        if message.from_user.id not in groups.keys():
            bot.send_message(message.chat.id, f"Please, sign in in private messages in @{bot_username}. It will take less than a minute")
            return
                    


    groups[message.chat.id].enabled = True

    print(f"OWNER_ID IN ENABLED COMMAND:  {groups[message.chat.id].owner_id}")

    markup_commands = load_buttons(types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id)

    if message.chat.type == "private":
        groups[message.chat.id].trigger_probability = 1
        bot.reply_to(
            message, groups[message.chat.id].templates[language_code]["enabled_user.txt"], reply_markup=markup_commands, parse_mode="HTML"
        )
    else:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_enable_auto.txt"],
            callback_data="auto_mode",
        )
        markup.add(button)
        button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_enable_dialog.txt"],
            callback_data="dialog_mode",
        )
        markup.add(button)
        button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_enable_manual.txt"],
            callback_data="manual_mode",
        )
        markup.add(button)

        print("I AM IN ENABLED COMMAND")
        print(f"MARKUP OF BUTTONS: {markup}")

        bot.send_message(
            message.chat.id,
            groups[message.chat.id].templates[language_code]["enabled.txt"],
            reply_markup=markup,
            parse_mode="HTML",
        )



# --- Auto mode Enable ---
@error_handler
def auto_enable(message):
    language_code = groups[message.chat.id].lang_code

    markup_commands = load_buttons(types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id)

    bot.send_message(
        message.chat.id,
        groups[message.chat.id].templates[language_code]["enabled_auto.txt"].format(
            probability=groups[message.chat.id].trigger_probability
        ),
        reply_markup=markup_commands,
        parse_mode="HTML",
    )

# --- Dialog mode enable ---
@error_handler
def dialog_enable(message):

    language_code = groups[message.chat.id].lang_code

    markup_commands = load_buttons(types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id)


    groups[message.chat.id].trigger_probability = 1

    bot.send_message(message.chat.id, groups[message.chat.id].templates[language_code]["enabled_dialog.txt"],reply_markup=markup_commands)

# --- Manual mode enable ---
@error_handler
def manual_enable(message):

    language_code = groups[message.chat.id].lang_code

    markup_commands = load_buttons(types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id)
        
    groups[message.chat.id].trigger_probability = 0
    bot.reply_to(
        message, groups[message.chat.id].templates[language_code]["enabled_manual.txt"], reply_markup=markup_commands, parse_mode="HTML"
    )




# --- Disable ---
@bot.message_handler(commands=["disable"], func=time_filter)
@error_handler
def disable(message):
    language_code = groups[message.chat.id].lang_code
    groups[message.chat.id].enabled = False

    markup = load_buttons(types, groups, message.chat.id, language_code, owner_id=groups[message.chat.id].owner_id)

    bot.send_message(message.chat.id, groups[message.chat.id].templates[language_code]["disabled.txt"], reply_markup=markup)
