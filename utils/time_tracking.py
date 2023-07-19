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
        return ['BIG BUSINESS', 10, 1000000000000, 5000000, True, True, True, True, True, True, True]

    elif promocode_in == small_business_promocode:
        return ['SMALL BUSINESS', 5, 100, 3000000, True, True, True, True, True, True, True]

    elif promocode_in == user_promocode:
        return ['USER', 3, 50, 1000000, False, True, False, False, False, False, False]

    elif promocode_in == promocode_100000:
        return [100000]

    else:
        return []


# create a scheduler
promocode_scheduler = BackgroundScheduler()

# add a job that runs every day
promocode_scheduler.add_job(get_exist_code, 'interval', days=7)

# start the scheduler
promocode_scheduler.start()