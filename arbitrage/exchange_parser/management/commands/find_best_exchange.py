from time import sleep

from exchange_parser.p2p_binance_parser import get_new_p2p_orders
from data.models import Fiat, P2POrder, Payment, Coin

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            find_best_exchange()
            sleep(3)


MSG_TEMPLATE = "Found exchange rate with {profit:.2f} %:" \
               "\n- {order1} " \
               "\n- {order2} "


def find_best_exchange():
    print('Trying to find best exchange ...')
    check_var_1()


def check_var_1():
    USD_RUB = 59.89

    rub = Fiat.objects.get(name='RUB')
    usd = Fiat.objects.get(name='USD')
    usdt = Coin.objects.get(name='USDT')

    tin_rub = Payment.objects.get(name='Tinkoff', fiat=rub)
    tin_usd = Payment.objects.get(name='Tinkoff', fiat=usd)

    buy_rub = P2POrder.objects.filter(type='BUY', payment=tin_rub, coin=usdt)
    if len(buy_rub) == 0:
        print('No orders for selling of RUB')
        exit()
    buy_rub = sorted(buy_rub, key=lambda x: x.rate)[0]

    sell_usd = P2POrder.objects.filter(type='SELL', payment=tin_usd, coin=usdt)
    if len(sell_usd) == 0:
        print('No orders for buying of USD')
        exit()
    sell_usd = sorted(sell_usd, key=lambda x: x.rate, reverse=True)[0]
    result = 1 / buy_rub.rate * sell_usd.rate * USD_RUB
    if result > .5:
        print(MSG_TEMPLATE.format(order1=buy_rub, order2=sell_usd,
                                  profit=(result - 1) * 100
                                  ))
