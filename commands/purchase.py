from __main__ import *


# ---------- Main message ----------

# --- Purchase ---
@bot.message_handler(commands=["purchase"], func=time_filter)
@error_handler
def purchase(message, back_from=False):

    language_code = groups[message.chat.id].lang_code

    if message.chat.type == 'private':

        purchase_markup = types.InlineKeyboardMarkup()

        if groups[message.chat.id].subscription == "Free":
                # --- Buttons ---
            user_button = types.InlineKeyboardButton(
                text=groups[message.chat.id].templates[language_code]["button_user.txt"],
                callback_data="easy",
            )
            small_business_button = types.InlineKeyboardButton(
                text=groups[message.chat.id].templates[language_code]["button_small_business.txt"],
                callback_data="middle",
            )
            big_business_button = types.InlineKeyboardButton(
                text=groups[message.chat.id].templates[language_code]["button_big_business.txt"],
                callback_data="pro",
            )


            purchase_markup.add(user_button)
            purchase_markup.add(small_business_button)
            purchase_markup.add(big_business_button)

        else:
            extend_sub_button = types.InlineKeyboardButton(
                text=groups[message.chat.id].templates[language_code]["button_extend_sub.txt"],
                callback_data="extend_sub",
            )
            update_sub_button = types.InlineKeyboardButton(
                text=groups[message.chat.id].templates[language_code]["button_update_sub.txt"],
                callback_data="update_sub",
            )

            purchase_markup.add(extend_sub_button)
            purchase_markup.add(update_sub_button)
        
        messages_button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_more_messages.txt"],
            callback_data="more_messages",
        )
        promocode_button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_promocode.txt"],
            callback_data="promocode",
        )

        # Adding buttons to keyboard
        
        purchase_markup.add(messages_button)
        purchase_markup.add(promocode_button)

        back_button = types.InlineKeyboardButton(
            text="<<<",
            callback_data="back_to_account",
        )
        purchase_markup.add(back_button)

        # Seconding keyboard
        bot.edit_message_text(
            groups[message.chat.id].templates[language_code]["purchase.txt"].format(plan=groups[message.chat.id].subscription),
            message.chat.id, 
            message.message_id,
            reply_markup=purchase_markup,
            parse_mode="HTML",
        )


    else:
        bot.reply_to(message, groups[message.chat.id].templates[language_code]["buy_unavaible_in_group.txt"].format(bot_username=bot_username))


