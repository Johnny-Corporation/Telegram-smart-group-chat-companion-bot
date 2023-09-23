from __main__ import *


# --- Start ---
@bot.message_handler(commands=["start"], func=time_filter)
@error_handler
def start(message):
    # Referral checking

    if message.text.startswith("/start referral"):
        invited_user_id = message.chat.id

        referrer_id = int((message.text.split()[1]).split("_")[1])

        if not referrer_id == message.chat.id and invited_user_id not in groups:
            invited_user = bot.get_chat_member(message.chat.id, invited_user_id)

            bot.send_message(
                referrer_id,
                templates[groups[referrer_id].lang_code]["referral_success.txt"].format(
                    invited_user=invited_user.user.username
                ),
            )

            # Bonuses to referrer
            groups[referrer_id].discount_subscription["Referral discount"] = 0.95
            groups[referrer_id].discount_message["Referral discount"] = 0.95

            init_new_group(message.chat.id, inviting=True, referrer_id=referrer_id)
            return


    if (message.chat.id not in groups) or (not groups[message.chat.id].lang_code):
        init_new_group(message.chat.id)
    else:
        help(message)

    

    



    
