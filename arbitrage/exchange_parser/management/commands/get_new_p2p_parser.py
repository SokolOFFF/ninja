from exchange_parser.p2p_binance_parser import get_new_p2p_orders

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        get_new_p2p_orders()