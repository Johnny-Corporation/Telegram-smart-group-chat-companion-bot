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
sub_pro_promocode = generate_code()
discount_on_sub_50 = generate_code()
discount_for_public = 'JOHNNY'
promocode_100 = generate_code()


def get_exist_code():
    global sub_pro_promocode, promocode_100, discount_on_sub_50
    sub_pro_promocode = generate_code()
    discount_on_sub_50 = generate_code()
    promocode_100 = generate_code()

def check_code(promocode_in):
    global sub_pro_promocode, promocode_100, discount_on_sub_50, discount_for_public

    if promocode_in == sub_pro_promocode:
        sub_pro_promocode = generate_code()
        return ['Pro', 100]
    elif promocode_in == discount_on_sub_50:
        discount_on_sub_50 = generate_code()
        return [0.50]
    elif promocode_in == discount_for_public:
        return [0.50]
    elif promocode_in == promocode_100:
        promocode_100 = generate_code()
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

