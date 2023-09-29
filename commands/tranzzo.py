"""This file is a draft, don't remove him, if this bot will get us a more and more profit, we connect this payment system"""

from __main__ import *


# e.g., if you're using Stripe, get this token from Strip
prices = [types.LabeledPrice(label="Working Time Machine", amount=5000)]


def send_invoice(message):
    title = "Your Invoice"
    description = "This is a description of your invoice."
    provider_token = provider_token
    currency = "usd"
    photo_url = "https://example.com/photo.jpg"
    start_parameter = "time-machine-example"
    invoice_payload = "HAPPY FRIDAYS COUPON"

    bot.send_invoice(
        message.chat.id,
        title,
        description,
        invoice_payload,
        provider_token,
        start_parameter,
        currency,
        prices,
        photo_url=photo_url,
    )


def create_invoice(message):
    title = "Your Invoice"
    description = "This is a description of your invoice."
    invoice_payload = "HAPPY FRIDAYS COUPON"
    provider_token = provider_token
    currency = "usd"
    prices = [types.LabeledPrice(label="Working hours", amount=2000)]

    bot.send_invoice(
        message.chat.id,
        title,
        description,
        invoice_payload,
        provider_token,
        currency,
        prices[0],
        photo_url=photo_url,
    )


@bot.message_handler(commands=["invoice"])
def command_invoice(message):
    send_invoice(message)


@bot.message_handler(commands=["buy"])
def english_pay(message):
    tranzzo_token = "535936410:LIVE:6338457969_87403557-8321-4e22-ad83-78eb2a82e3da"
    bot.send_invoice(
        message.chat.id,  # chat_id
        "Working Time Machine",  # title
        "Dwscription!",  # description
        "HAPPY FRIDAYS COUPON",  # invoice_payload
        tranzzo_token,  # provider_token
        "rub",  # currency
        prices,  # prices
        #  photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
        #  photo_height=512,  # !=0/None or picture won't be shown
        #  photo_width=512,
        #  photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter="time-machine-example",
    )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    (shipping_query)
    bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options,
        error_message="Oh, seems like our Dog couriers are having a lunch right now. Try again later!",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
        " try to pay again in a few minutes, we need a small rest.",
    )


@bot.message_handler(content_types=["successful_payment"])
def got_payment(message):
    bot.send_message(
        message.chat.id,
        "Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! "
        "Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!".format(
            message.successful_payment.total_amount / 100,
            message.successful_payment.currency,
        ),
        parse_mode="Markdown",
    )
