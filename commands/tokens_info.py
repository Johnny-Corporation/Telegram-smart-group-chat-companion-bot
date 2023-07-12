from __main__ import *


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"], func=time_filter)
@error_handler
def tokens_info_command(message):
    language_code = groups[message.chat.id].lang_code
    total_tokens = groups[message.chat.id].total_spent_tokens
    bot.reply_to(
        message,
        templates[language_code]["tokens.txt"].format(
            dollars=tokens_to_dollars(
                groups[message.chat.id].model,
                total_tokens[0],
                total_tokens[1],
            ),
            spent_tokens=sum(groups[message.chat.id].total_spent_tokens),
        ),
    )
