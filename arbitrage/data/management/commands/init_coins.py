from data.models import Fiat, Payment, Coin

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Init data'

    def handle(self, *args, **kwargs):
        rub = Fiat.objects.get_or_create(name='RUB')[0]
        usd = Fiat.objects.get_or_create(name='USD')[0]
        euro = Fiat.objects.get_or_create(name='EUR')[0]

        tink_rub = Payment.objects.get_or_create(name='Tinkoff', fiat=rub)[0]
        tink_usd = Payment.objects.get_or_create(name='Tinkoff', fiat=usd)[0]
        tink_euro = Payment.objects.get_or_create(name='Tinkoff', fiat=euro)[0]

        raif_rub = Payment.objects.get_or_create(name='Raiffeisenbank', fiat=rub)[0]

        qiwi_rub = Payment.objects.get_or_create(name='QIWI', fiat=rub)[0]

        usdt = Coin.objects.get_or_create(name='USDT')[0]
        busd = Coin.objects.get_or_create(name='BUSB')[0]
