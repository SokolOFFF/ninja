from time import sleep
from datetime import datetime, timedelta

from data.models import Fiat, P2POrder, Payment, Coin, Currencies

from django.core.management.base import BaseCommand

from exchange_parser.tinkoff_rates_parser import get_rate_of


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            find_best_exchange()
            sleep(60)


MSG_TEMPLATE = "Found exchange rate with {profit:.2f} %:" \
               "\n- {order1} " \
               "\n- {order2} "


def find_best_exchange():
    print('Trying to find best exchange ...')
    check_var_1()


#TODO: rewrite getting usd figi to adequate format (line 32)
def check_var_1():
    USD_RUB = get_rate_of(Currencies.USDRUB_FIGI)

    rub = Fiat.objects.get(name='RUB')
    usd = Fiat.objects.get(name='USD')
    usdt = Coin.objects.get(name='USDT')

    tin_rub = Payment.objects.get(name='Tinkoff', fiat=rub)
    tin_usd = Payment.objects.get(name='Tinkoff', fiat=usd)

    now = datetime.now()
    start = now - timedelta(minutes=3)
    buy_rub = P2POrder.objects.filter(type='BUY', payment=tin_rub, coin=usdt, parsing_time__range=[start, now])
    if len(buy_rub) == 0:
        print('No orders for selling of RUB')
        return
    buy_rub = sorted(buy_rub, key=lambda x: x.rate)[0]

    sell_usd = P2POrder.objects.filter(type='SELL', payment=tin_usd, coin=usdt, parsing_time__range=[start, now])
    if len(sell_usd) == 0:
        print('No orders for buying of USD')
        return
    sell_usd = sorted(sell_usd, key=lambda x: x.rate, reverse=True)[0]
    result = 1 / buy_rub.rate * sell_usd.rate * USD_RUB
    if result > 1:
        print(MSG_TEMPLATE.format(order1=buy_rub, order2=sell_usd,
                                  profit=(result - 1) * 100
                                  ))
