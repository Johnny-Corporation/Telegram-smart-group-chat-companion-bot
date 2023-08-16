from __main__ import *


# --- reply handler for set temp
@error_handler
def support_us_reply_handler(inner_message):

    None

    # def support(inner_message):
    #     language_code = groups[inner_message.chat.id].lang_code
    #     try:
    #         val = float(inner_message.text)
    #     except ValueError:
    #         bot.send_message(
    #             inner_message.chat.id, templates[language_code]["support_declined.txt"]
    #         )
    #         return

    #     pay = support(inner_message, val)

    #     if pay:
    #         bot.reply_to(
    #             inner_message,
    #             templates[language_code]["thanks_for_supporting.txt"]
    #         )
    #         return
        
    #     bot.send_message(
    #         inner_message.chat.id, templates[language_code]["support_declined.txt"]
    #     )

    # # create a scheduler
    # sub_scheduler = BackgroundScheduler()

    # # schedule a task to print a number after 2 seconds
    # sub_scheduler.add_job(support, 'date', run_date=start_date + relativedelta(=3), args=[inner_message], misfire_grace_time=86400)

    # # start the scheduler
    # sub_scheduler.start()

    