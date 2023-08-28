from __main__ import *


# --- set_up functions ---
@error_handler
def extend_sub(message):

    language_code = groups[message.chat.id].lang_code

    accept_payment(message, 999, 'extend')
