from __main__ import *


# --- set_up functions ---
@bot.message_handler(commands=["update_sub"], func=time_filter and member_filter)
@error_handler
def update_sub(message):

    if message.chat.type == 'private':
        language_code = groups[message.chat.id].lang_code

        purchase_markup = types.InlineKeyboardMarkup()

        # --- Buttons ---
        user_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_user.txt"],
            callback_data="easy",
        )
        small_business_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_small_business.txt"],
            callback_data="middle",
        )
        big_business_button = types.InlineKeyboardButton(
            text=templates[language_code]["button_big_business.txt"],
            callback_data="pro",
        )

        purchase_markup.add(user_button)
        purchase_markup.add(small_business_button)
        purchase_markup.add(big_business_button)

        # Seconding keyboard
        bot.send_message(
            message.chat.id,
            templates[language_code]["update_sub.txt"].format(plan=groups[message.chat.id].subscription),
            reply_markup=purchase_markup,
            parse_mode="HTML",
        )
    else:
        bot.reply_to(message, templates[language_code]["buy_unavaible_in_group.txt"].format(bot_username=bot_username))