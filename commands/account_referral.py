from __main__ import *


# --- Referral ---
def referral(message):
    language_code = groups[message.chat.id].lang_code

    #Create link
    link = f"https://t.me/{bot_username}?start=referral_{message.chat.id}"

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text=templates[language_code]["button_referral_link.txt"],
        url=link
    )
    markup.add(button1)
    bot.send_message(
        message.chat.id, 
        templates[language_code]["account_referral.txt"],
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )