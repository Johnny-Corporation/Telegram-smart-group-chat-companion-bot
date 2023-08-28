from __main__ import *


# ---------- Main message ----------

# --- Purchase ---
def purchase(message):

    language_code = groups[message.chat.id].lang_code

    if message.chat.type == 'private':

        purchase_markup = types.InlineKeyboardMarkup()

        messages_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_more_messages.txt"],
            callback_data="more_messages",
        )
        purchase_markup.add(messages_button)

        if groups[message.chat.id].subscription == "Free":
                # --- Buttons ---
            sub_button = types.InlineKeyboardButton(
                text=templates[language_code]["button_pro.txt"],
                callback_data="pro",
            )


            purchase_markup.add(sub_button)

        else:
            extend_sub_button = types.InlineKeyboardButton(
                text=templates[language_code]["button_extend_sub.txt"],
                callback_data="extend_sub",
            )

            purchase_markup.add(extend_sub_button)
        
        promocode_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_promocode.txt"],
            callback_data="promocode",
        )

        # Adding buttons to keyboard
        
        purchase_markup.add(promocode_button)

        back_button = types.InlineKeyboardButton(
            text="<<<",
            callback_data="menu",
        )
        purchase_markup.add(back_button)

        # Seconding keyboard
        bot.edit_message_text(
            templates[language_code]["purchase.txt"].format(plan=groups[message.chat.id].subscription),
            message.chat.id, 
            message.message_id,
            reply_markup=purchase_markup,
            parse_mode="HTML",
        )


    else:
        bot.reply_to(message, templates[language_code]["buy_unavaible_in_group.txt"].format(bot_username=bot_username))


