from time import sleep
from datetime import datetime, timedelta

from data.models import Fiat, P2POrder, Payment, Coin, Currency, Link, Circle, User, BestchangePayment, BestchangeExchange, CryptoCurrency, BinanceSpotPrice

from django.core.management.base import BaseCommand

from exchange_parser.tinkoff_rates_parser import get_rate_of

from exchange_parser.sender_bot import sendAll

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            find_best_exchange()
            sleep(10)


MSG_TEMPLATE = "Found exchange rate with {profit:.2f} %:" \
               "\n- {order1} " \
               "\n- {order2} "

def msg_template(circle_num, profit, order1, order2):
    if circle_num == 1:
        link_short_name_order_1 = '{coin}{fiat}_P2PBIN_{payment}_{type}'.format(coin=order1.coin.name,
                                                                                fiat=order1.payment.fiat.name,
                                                                                payment=order1.payment.name,
                                                                                type=order1.type)
        link_short_name_order_2 = '{coin}{fiat}_P2PBIN_{payment}_{type}'.format(coin=order2.coin.name,
                                                                                fiat=order2.payment.fiat.name,
                                                                                payment=order2.payment.name,
                                                                                type=order2.type)

        return f'Found exchange rate with {profit:.2f}%:' \
               f'\n- {order1}' \
               f'\n   link: {Link.objects.get(short_name=link_short_name_order_1).link}' \
               f'\n- {order2}' \
               f'\n   link: {Link.objects.get(short_name=link_short_name_order_2).link}' \
               f'\n- Exchange on Tinkoff Investments' \
               f'\n   link: {Link.objects.get(short_name="TINKOFF_USD_CHANGE").link}'
    elif circle_num == 2:
        link_short_name_order_1 = '{coin}{fiat}_P2PBIN_{payment}_{type}'.format(coin=order1.coin.name,
                                                                                fiat=order1.payment.fiat.name,
                                                                                payment=order1.payment.name,
                                                                                type=order1.type)
        link_short_name_order_2 = '{coin}{fiat}_P2PBIN_{payment}_{type}'.format(coin=order2.coin.name,
                                                                                fiat=order2.payment.fiat.name,
                                                                                payment=order2.payment.name,
                                                                                type=order2.type)

        return f'Found exchange rate with {profit:.2f}:' \
               f'\n- Exchange on Tinkoff Investments' \
               f'\n   link: {Link.objects.get(short_name="TINKOFF_USD_CHANGE").link}' \
               f'\n- {order1}' \
               f'\n   link: {Link.objects.get(short_name=link_short_name_order_1).link}' \
               f'\n- {order2}' \
               f'\n   link: {Link.objects.get(short_name=link_short_name_order_2).link}'


def msg_template_v2(circle_num, profit, order1, binance_price, order2):
    crypto_name = order1.payment_to.name
    coin_name = order2.coin.name
    link_to_bestchange = Link.objects.get(short_name=f'QIWI{crypto_name}_BESTCHANGE').link
    link_to_binance_spot = f'www.binance.com/en/trade/{crypto_name}_{coin_name}?_from=markets&theme=dark&type=spot'
    link_to_binance_p2p = '{coin}{fiat}_P2PBIN_{payment}_{type}'.format(coin=coin_name, fiat='RUB',
                                                                        payment=order2.payment.name, type=order2.type)
    return f'Found exchange rate with {profit:.2f}%:' \
               f'\n- Buy {crypto_name} on Bestchange' \
               f'\n- {order1}' \
               f'\n   link: {link_to_bestchange}' \
               f'\n Sell {crypto_name} by {coin_name} with price: {binance_price}' \
               f'\n   link: {link_to_binance_spot}' \
               f'\n- {order2}' \
               f'\n   link: {Link.objects.get(short_name=link_to_binance_p2p).link}'
def find_best_exchange():
    print('Trying to find best exchange ...')
    print()
    print('Looking for the first circle..')
    check_var_1()
    print('Looking for the second circle..')
    check_var_2()
    print('Looking for the third circle..')
    check_var_3()
    print('Mailing..')
    mailing()
    print('-------------------------------')

def check_var_1():
    USD_RUB = get_rate_of(Currency.objects.get(name='USDRUB').figi)

    rub = Fiat.objects.get(name='RUB')
    usd = Fiat.objects.get(name='USD')
    usdt = Coin.objects.get(name='USDT')

    rub_payments = Payment.objects.filter(fiat=rub).all()
    tin_usd = Payment.objects.get(name='TinkoffNew', fiat=usd)

    now = datetime.now()
    start = now - timedelta(minutes=3)

    old_orders = P2POrder.objects.filter(parsing_time__lte=start)
    if len(old_orders) > 0:
        print(' -- Deleting old orders')
        old_orders.delete()

    buy_rub = P2POrder.objects.filter(type='BUY', payment__in=rub_payments, coin=usdt, parsing_time__range=[start, now])
    if len(buy_rub) == 0:
        print('No orders for selling of RUB')
        return

    buy_rub = sorted(buy_rub, key=lambda x: x.rate)

    sell_usd = P2POrder.objects.filter(type='SELL', payment=tin_usd, coin=usdt, parsing_time__range=[start, now])
    if len(sell_usd) == 0:
        print('No orders for buying of USD')
        return
    sell_usd = sorted(sell_usd, key=lambda x: x.rate, reverse=True)

    old_circles = Circle.objects.filter(variant=1)
    if len(old_circles) > 0:
        print(' -- Deleting old circles')
        old_circles.delete()

    for buy in buy_rub:
        for sell in sell_usd:
            result = 1 / buy.rate * sell.rate * USD_RUB
            if result > 1:
                #print(msg_template(1, (result - 1) * 100, buy, sell))
                # TODO: understand how to deal with USD limits, for now it's just RUB limits
                Circle.objects.get_or_create(msg_text=msg_template(1, (result - 1) * 100, buy, sell), variant=1,
                                             spread=(result - 1) * 100, lower_limit=buy.lower_limit, upper_limit=buy.upper_limit)

    #sendAll(msg_template(1, (result - 1) * 100, buy_rub, sell_usd))
    #print(MSG_TEMPLATE.format(order1=buy_rub, order2=sell_usd,profit=(result - 1) * 100))



def check_var_2():
    USD_RUB = get_rate_of(Currency.objects.get(name='USDRUB').figi)

    rub = Fiat.objects.get(name='RUB')
    usd = Fiat.objects.get(name='USD')
    usdt = Coin.objects.get(name='USDT')

    rub_payments = Payment.objects.filter(fiat=rub).all()
    tin_usd = Payment.objects.get(name='TinkoffNew', fiat=usd)

    now = datetime.now()
    start = now - timedelta(minutes=3)

    old_orders = P2POrder.objects.filter(parsing_time__lte=start)
    if len(old_orders) > 0:
        print(' -- Deleting old orders')
        old_orders.delete()

    buy_usd = P2POrder.objects.filter(type='BUY', payment=tin_usd, coin=usdt, parsing_time__range=[start, now])
    if len(buy_usd) == 0:
        print('No orders for selling of USD')
        return
    buy_usd = sorted(buy_usd, key=lambda x: x.rate)

    sell_rub = P2POrder.objects.filter(type='SELL', payment__in=rub_payments, coin=usdt, parsing_time__range=[start, now])
    if len(sell_rub) == 0:
        print('No orders for buying of RUB')
        return
    sell_rub = sorted(sell_rub, key=lambda x: x.rate, reverse=True)

    old_circles = Circle.objects.filter(variant=2)
    if len(old_circles) > 0:
        print(' -- Deleting old circles')
        old_circles.delete()


    for buy in buy_usd:
        for sell in sell_rub:
            result = 1 / USD_RUB / buy.rate * sell.rate
            if result > 1:
                #print(msg_template(2, (result - 1) * 100, buy, sell))
                # TODO: understand how to deal with USD limits, for now it's just RUB limits
                Circle.objects.get_or_create(msg_text=msg_template(2, (result - 1) * 100, buy, sell), variant=2,
                                             spread=(result - 1) * 100, lower_limit=sell.lower_limit, upper_limit=sell.upper_limit)

                #print(MSG_TEMPLATE.format(order1=buy_usd, order2=sell_rub,profit=(result - 1) * 100))
    #sendAll(msg_template(2, (result - 1) * 100, buy_usd, sell_rub))

def check_var_3():
    qiwi = BestchangePayment.objects.get(name='QIWI')

    rub = Fiat.objects.get(name='RUB')
    usdt = Coin.objects.get(name='USDT')

    rub_payments = Payment.objects.filter(fiat=rub).all()

    now = datetime.now()
    start = now - timedelta(minutes=3)

    old_orders = P2POrder.objects.filter(parsing_time__lte=start)
    if len(old_orders) > 0:
        print(' -- Deleting old orders')
        old_orders.delete()

    old_exchanges = BestchangeExchange.objects.filter(parsing_time__lte=start)
    if len(old_exchanges) > 0:
        print(' -- Deleting old exchanges')
        old_exchanges.delete()

    old_prices = BinanceSpotPrice.objects.filter(parsing_time__lte=start)
    if len(old_prices) > 0:
        print(' -- Deleting old prices')
        old_prices.delete()

    old_circles = Circle.objects.filter(variant=3)
    if len(old_circles) > 0:
        print(' -- Deleting old circles')
        old_circles.delete()

    cryptocurrencies = CryptoCurrency.objects.all()
    coins = Coin.objects.all()

    for crypto in cryptocurrencies:
        buy_cryptocurrency = BestchangeExchange.objects.filter(payment_from=qiwi, payment_to=BestchangePayment.objects.get(name=crypto.name),
                                                               parsing_time__range=[start, now])
        if len(buy_cryptocurrency) == 0:
            print('No orders for buying cryptocurrency throw QIWI')
            return
        buy_cryptocurrency = sorted(buy_cryptocurrency, key=lambda x: x.rate)
        for coin in coins:
            if crypto.name == "KMD" and coin.name == "BUSD":
                continue
            binance_spot = BinanceSpotPrice.objects.filter(symbol=crypto.name+coin.name, parsing_time__range=[start, now])
            if len(binance_spot) == 0:
                print(f'No prices for buying of {crypto.name}')
                continue
            binance_spot_price = binance_spot[0].price
            sell_rub = P2POrder.objects.filter(type='SELL', payment__in=rub_payments, coin=coin,
                                               parsing_time__range=[start, now])
            if len(sell_rub) == 0:
                print('No orders for buying of RUB')
                continue
            sell_rub = sorted(sell_rub, key=lambda x: x.rate, reverse=True)
            for buy in buy_cryptocurrency:
                for sell in sell_rub:
                    result = 1 / buy.rate * binance_spot_price * sell.rate
                    #print(crypto.name, buy.rate, binance_spot_price, coin.name, sell.rate, result)
                    #print(result)
                    if result > 1:
                        Circle.objects.get_or_create(msg_text=msg_template_v2(3, (result - 1) * 100, buy, binance_spot_price, sell), variant=3,
                                                     spread=(result - 1) * 100, lower_limit=max(sell.lower_limit, buy.min_sum),
                                                     upper_limit=min(sell.upper_limit, buy.max_sum))

def mailing():
    subscribers = User.objects.filter(is_subscribed=True)
    circles = Circle.objects.all()
    circles = sorted(circles, key=lambda x: x.spread, reverse=True)
    for subscriber in subscribers:
        best_circles = []
        for circle in circles:

            # TODO: fix limits
            if circle.spread >= subscriber.spread and subscriber.money_amount <= circle.upper_limit and subscriber.money_amount >= circle.lower_limit:
                if len(best_circles) < 5:
                    best_circles.append(circle)

        if len(best_circles) != 0:
            sendAll(subscriber.telegram_id, f'Found {len(best_circles)} best circles:   ')
            for best_circles in best_circles:
                sendAll(subscriber.telegram_id, best_circles.msg_text + f'\n{subscriber.money_amount} -> {subscriber.money_amount + subscriber.money_amount / 100 * circle.spread}')
