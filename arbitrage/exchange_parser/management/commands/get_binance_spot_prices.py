from time import sleep

from exchange_parser.binance_spot_parser import get_cryptocurrencies_prices

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            get_cryptocurrencies_prices()
            sleep(10)
