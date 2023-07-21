from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["purchase"], func=time_filter and member_filter)
@error_handler
def purchase(message):

    if message.chat.type == 'private':
        language_code = groups[message.chat.id].lang_code

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
        
        tokens_button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_more_tokens.txt"],
            callback_data="more_tokens",
        )
        promocode_button = types.InlineKeyboardButton(
            text=groups[message.chat.id].templates[language_code]["button_promocode.txt"],
            callback_data="promocode",
        )

        # Adding buttons to keyboard
        
        purchase_markup.add(tokens_button)
        purchase_markup.add(promocode_button)

        # Seconding keyboard
        bot.send_message(
            message.chat.id,
            groups[message.chat.id].templates[language_code]["purchase.txt"].format(plan=groups[message.chat.id].subscription),
            reply_markup=purchase_markup,
            parse_mode="HTML",
        )


    else:
        bot.reply_to(message, groups[message.chat.id].templates[language_code]["buy_unavaible_in_group.txt"].format(bot_username=bot_username))