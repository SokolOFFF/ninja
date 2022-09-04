from data.models import Fiat, Payment, Coin, Currencies

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Init data'

    def handle(self, *args, **kwargs):
        rub = Fiat.objects.get_or_create(name='RUB')[0]
        usd = Fiat.objects.get_or_create(name='USD')[0]
        euro = Fiat.objects.get_or_create(name='EUR')[0]

        tink_rub = Payment.objects.get_or_create(name='TinkoffNew', fiat=rub)[0]
        tink_usd = Payment.objects.get_or_create(name='TinkoffNew', fiat=usd)[0]
        tink_euro = Payment.objects.get_or_create(name='TinkoffNew', fiat=euro)[0]

        raif_rub = Payment.objects.get_or_create(name='RaiffeisenBankRussia', fiat=rub)[0]

        qiwi_rub = Payment.objects.get_or_create(name='QIWI', fiat=rub)[0]

        usdt = Coin.objects.get_or_create(name='USDT')[0]
        busd = Coin.objects.get_or_create(name='BUSD')[0]

        usd_rub_rate = Currencies.objects.get_or_create(name='USDRUB', figi='USD000UTSTOM')[0]
        eur_rub_rate = Currencies.objects.get_or_create(name='EURRUB', figi='EUR000UTSTOM')[0]
        gbp_rub_rate = Currencies.objects.get_or_create(name='GBPRUB', figi='TCS0013HQ5F0')[0]
