from time import sleep

from exchange_parser.bestchange_parser import get_new_bestchange_exchanges

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            get_new_bestchange_exchanges()
            sleep(10)
