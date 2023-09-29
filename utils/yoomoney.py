from __main__ import *
import threading
import time
import random
from yoomoney import Client
from yoomoney import Quickpay

token = yoomoney_token
client = Client(token)


def accept_payment(message, cost, type_of_own="update", messages=0):
    def payment_with_timeout(url, timeout=120.0):
        result = [
            None
        ]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

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
        if type_of_own == 'update' or type_of_own == 'extend':

            for name in groups[message.chat.id].discount_subscription.keys():
                value = groups[message.chat.id].discount_subscription[name]
                discounts = ''
                if not name == "total_sum":
                    discounts = discounts + f'{translate_text(language_code, name)}: {(value)*100}%\n'

            bot.send_message(
                message.chat.id,
                templates[language_code]["info_about_buy_of_sub.txt"].format(
                    cost=cost,
                    discounts=discounts
                ),
                reply_markup=markup,
                parse_mode="HTML",
            )
            groups[message.chat.id].discount_subscription = {}
            groups[message.chat.id].discount_subscription["total sum"] = 1

        elif type_of_own == 'more_messages':

            discounts = ' '
            for name in groups[message.chat.id].discount_message.keys():
                value = groups[message.chat.id].discount_message[name]
                discounts = ''
                if not name == "total sum":
                    discounts = discounts + f'{translate_text(language_code, name)}: {(1-value)*100}%\n'

            bot.send_message(
                message.chat.id,
                templates[language_code]["info_about_buy_of_messages.txt"].format(
                    count=messages,
                    sub=groups[message.chat.id].subscription,
                    cost=cost,
                    discounts=discounts
                ),
                reply_markup=markup,
                parse_mode="HTML",
            )
            groups[message.chat.id].discount_message = {}
            groups[message.chat.id].discount_message["total sum"] = 1
        start_time = time.time()

        # Запускаем таймеры, пока не истечет общее время ожидания
        while time.time() - start_time < timeout and result[0] is None:
            timer = threading.Timer(2.0, lambda: check_payment(label))
            timer.start()
            timer.join()

        if result[0] is None:
            result[0] = False

        if result[0]:
            if type_of_own == "update":

                #Referral check
                if groups[message.chat.id].invited:
                    groups[groups[message.chat.id].referrer_id].discount_subscription["referral discount"] = 0.70
                    groups[message.chat.id].invited = False

                groups[message.chat.id].add_new_user(
                    message.chat.id,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                    "Pro",
                    100,
                )
                groups[message.chat.id].load_subscription(message.chat.id)
                groups[message.chat.id].track_sub(message.chat.id, new=True)

                for group_id in groups[message.chat.id].id_groups:
                    groups[group_id].subscription = groups[message.chat.id].subscription
                    groups[group_id].permissions[groups[group_id].subscription][
                        "messages_limit"
                    ] = groups[message.chat.id].permissions[
                        groups[message.chat.id].subscription
                    ][
                        "messages_limit"
                    ]
                    groups[group_id].permissions[groups[group_id].subscription][
                        "dynamic_gen_permission"
                    ] = groups[message.chat.id].permissions[
                        groups[message.chat.id].subscription
                    ][
                        "dynamic_gen_permission"
                    ]
                    groups[group_id].permissions[groups[group_id].subscription][
                        "voice_output_permission"
                    ] = groups[message.chat.id].permissions[
                        groups[message.chat.id].subscription
                    ][
                        "voice_output_permission"
                    ]
                    groups[group_id].permissions[groups[group_id].subscription][
                        "sphere_permission"
                    ] = groups[message.chat.id].permissions[
                        groups[message.chat.id].subscription
                    ][
                        "sphere_permission"
                    ]
            elif type_of_own == "extend":
                groups[message.chat.id].extend_sub(
                    message.chat.id,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.username,
                )
                groups[message.chat.id].track_sub(message.chat.id, new=True)
            elif type_of_own == "more_messages":
                groups[message.chat.id].add_purchase_of_messages(message.chat.id, messages)
                # groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"] = (
                #     groups[message.chat.id].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"] + val
                # )

                for group in groups[message.chat.id].id_groups:
                    groups[group].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"] = groups[
                        message.chat.id
                    ].characteristics_of_sub[groups[message.chat.id].subscription]["messages_limit"]

                bot.send_message(
                    message.chat.id,
                    templates[language_code]["new_messages.txt"],
                    parse_mode="HTML",
                )
        else:
            bot.send_message(
                message.chat.id,
                groups[message.chat.id].templates[language_code][
                    "buy_was_canceled.txt"
                ],
            )

    # Генерация случайного 8-значного числа для label
    label = random.randint(10000000, 99999999)

    # Создание формы оплаты
    quickpay = Quickpay(
        receiver="4100118270605528",
        quickpay_form="shop",
        targets="Buy product",
        paymentType="SB",
        sum=cost,  # cost
        label=label,
    )

    # Вызов функции с передачей ссылки
    threading.Thread(
        target=payment_with_timeout, args=(quickpay.redirected_url, 120.0)
    ).start()


def support(message, cost):
    # Создание формы оплаты

    def payment_with_timeout(url, timeout=300.0):
        result = [
            None
        ]  # используем список вместо прямого значения, чтобы иметь возможность изменить его в любом потоке

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
            reply_markup=markup,
            parse_mode="HTML",
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
