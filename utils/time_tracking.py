import string
import random
from utils.db_controller import Controller
from apscheduler.schedulers.background import BackgroundScheduler
import time
from __main__ import *



# define the characters to use
chars = string.ascii_letters + string.digits

def generate_code(size=8, chars=chars):
    code = ''.join(random.choice(chars) for _ in range(size))
    return code

# ------- Promocodes --------
big_business_promocode = generate_code()
small_business_promocode = generate_code()
user_promocode = generate_code()
promocode_100000 = generate_code()

def get_exist_code():
    global big_business_promocode, small_business_promocode, user_promocode, promocode_100000
    big_business_promocode = generate_code()
    small_business_promocode = generate_code()
    user_promocode = generate_code()
    promocode_100000 = generate_code()

def check_code(promocode_in):
    global big_business_promocode, small_business_promocode, user_promocode, promocode_100000

    if promocode_in == big_business_promocode:
        return ['BIG BUSINESS', 1000]

    elif promocode_in == small_business_promocode:
        return ['SMALL BUSINESS', 700]

    elif promocode_in == user_promocode:
        return ['USER', 300]

    elif promocode_in == promocode_100000:
        return [100]

    else:
        return []


# create a scheduler
promocode_scheduler = BackgroundScheduler()

# add a job that runs every day
promocode_scheduler.add_job(get_exist_code, 'interval', days=7)

# start the scheduler
promocode_scheduler.start()



# create a scheduler
load_scheduler = BackgroundScheduler()

# create a scheduler
load_scheduler.start()

def typing(bot, message):

    def send(bot, message, message_id):
            
            try:

                bot.edit_message_text(f"Johnny is typing. ", message.chat.id, message_id)

                time.sleep(0.5)

                bot.edit_message_text(f"Johnny is typing.. ", message.chat.id, message_id)

                time.sleep(0.5)

                bot.edit_message_text(f"Johnny is typing... ", message.chat.id, message_id)

            except:
                None
    
    load_message = bot.send_message(message.chat.id, "Johnny is typing")

    label = random.randint(10000000, 99999999)
    id = 'loading_' + str(label)

    # add a job that runs every day
    load_scheduler.add_job(send, 'interval', seconds=0.5, args=[bot, message, load_message.message_id], id=id)

    return [load_message.message_id, id]

def stop_load(bot, message, message_id, id):
    load_scheduler.remove_job(id)

    bot.delete_message(message.chat.id, message_id)

