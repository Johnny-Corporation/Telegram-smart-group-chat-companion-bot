from __main__ import *
import threading
import time
import random
from yoomoney import Client
from yoomoney import Quickpay

token = yoomoney_token
client = Client(token)

def accept_payment(message, type_of_buy, cost):

    def payment_with_timeout(url, timeout=300.0):
        result = [None]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

        def check_payment(label):
            # Проверяем историю операции
            history = client.operation_history(label=label)
            for operation in history.operations:
                if operation.status == "success":
                    result[0] = True
                else:
                    result[0] = False

        language_code = groups[message.chat.id].lang_code

        markup = types.InlineKeyboardMarkup()
        temp_button = types.InlineKeyboardButton(
            text=templates[language_code]["pay.txt"],
            url=url,
        )
        markup.add(temp_button)
        bot.send_message(
            message.chat.id,
            templates[language_code]["info_about_buy.txt"].format(type_of_buy=type_of_buy, cost=cost),
            reply_markup = markup,
            parse_mode = "HTML"
        )
        print(label)

        start_time = time.time()

        # Запускаем таймеры, пока не истечет общее время ожидания
        while time.time() - start_time < timeout and result[0] is None:
            timer = threading.Timer(2.0, lambda: check_payment(label))
            timer.start()
            timer.join()

        if result[0] is None:
            result[0] = False

        return result[0]

    # Генерация случайного 8-значного числа для label
    label = random.randint(10000000, 99999999)


    # Создание формы оплаты
    quickpay = Quickpay(
        receiver="4100118270605528",
        quickpay_form="shop",
        targets="Buy product",
        paymentType="SB",
        sum=cost,
        label=label,
    )

    # Вызов функции с передачей ссылки
    res = payment_with_timeout(quickpay.redirected_url, 300.0)
    return res


def support(message, cost):
    # Создание формы оплаты

    def payment_with_timeout(url, timeout=300.0):
        result = [None]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

        def check_payment(label):
            # Проверяем историю операции
            history = client.operation_history(label=label)
            for operation in history.operations:
                if operation.status == "success":
                    result[0] = True
                else:
                    result[0] = False

        language_code = groups[message.chat.id].lang_code

        markup = types.InlineKeyboardMarkup()
        temp_button = types.InlineKeyboardButton(
            text=templates[language_code]["pay.txt"],
            url=url,
        )
        markup.add(temp_button)
        bot.send_message(
            message.chat.id,
            templates[language_code]["info_about_support.txt"].format(cost=cost),
            reply_markup = markup,
            parse_mode = "HTML"
        )
        print(label)

        start_time = time.time()

        # Запускаем таймеры, пока не истечет общее время ожидания
        while time.time() - start_time < timeout and result[0] is None:
            timer = threading.Timer(2.0, lambda: check_payment(label))
            timer.start()
            timer.join()

        if result[0] is None:
            result[0] = False

        return result[0]

    # Генерация случайного 8-значного числа для label
    label = random.randint(10000000, 99999999)


    # Создание формы оплаты
    quickpay = Quickpay(
        receiver="4100118270605528",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=cost,
        label=label,
    )

    # Вызов функции с передачей ссылки
    res = payment_with_timeout(quickpay.redirected_url)
    return res