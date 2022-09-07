from data.models import Fiat, Payment, Coin, Currency, Link

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Init data'

    def handle(self, *args, **kwargs):

        # Fiats table creation
        rub = Fiat.objects.get_or_create(name='RUB')[0]
        usd = Fiat.objects.get_or_create(name='USD')[0]
        euro = Fiat.objects.get_or_create(name='EUR')[0]


        # Payments table creation
        tink_rub = Payment.objects.get_or_create(name='TinkoffNew', fiat=rub)[0]
        tink_usd = Payment.objects.get_or_create(name='TinkoffNew', fiat=usd)[0]
        tink_euro = Payment.objects.get_or_create(name='TinkoffNew', fiat=euro)[0]

        raif_rub = Payment.objects.get_or_create(name='RaiffeisenBankRussia', fiat=rub)[0]

        qiwi_rub = Payment.objects.get_or_create(name='QIWI', fiat=rub)[0]

        # Stable coins table creation
        usdt = Coin.objects.get_or_create(name='USDT')[0]
        busd = Coin.objects.get_or_create(name='BUSD')[0]

        # Currency table creation
        usd_rub_rate = Currency.objects.get_or_create(name='USDRUB', figi='USD000UTSTOM')[0]
        eur_rub_rate = Currency.objects.get_or_create(name='EURRUB', figi='EUR000UTSTOM')[0]
        gbp_rub_rate = Currency.objects.get_or_create(name='GBPRUB', figi='TCS0013HQ5F0')[0]

        # Links table creation
            # TINKOFF BANK P2P BINANCE
        p2pbin_usdtrub_buy_tinkoff = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_TinkoffNew_BUY',
                                                                link='https://p2p.binance.com/en/trade/TinkoffNew/USDT?fiat=RUB',
                                                                description='Link to buy USDT by Tinkoff RUBs on P2P Binance')
        p2pbin_usdtrub_sell_tinkoff = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_TinkoffNew_SELL',
                                                                link='https://p2p.binance.com/en/trade/sell/USDT?fiat=RUB&payment=TinkoffNew',
                                                                description='Link to sell USDT by Tinkoff RUBs on P2P Binance')
        p2pbin_usdtusd_sell_tinkoff = Link.objects.get_or_create(short_name='USDTUSD_P2PBIN_TinkoffNew_SELL',
                                                                 link='https://p2p.binance.com/en/trade/sell/USDT?fiat=USD&payment=TinkoffNew',
                                                                 description='Link to sell USDT by Tinkoff USDs on P2P Binance')
        p2pbin_usdtusd_buy_tinkoff = Link.objects.get_or_create(short_name='USDTUSD_P2PBIN_TinkoffNew_BUY',
                                                                 link='https://p2p.binance.com/en/trade/TinkoffNew/USDT?fiat=USD',
                                                                 description='Link to buy USDT by Tinkoff USDs on P2P Binance')
        p2pbin_busdrub_buy_tinkoff = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_TinkoffNew_BUY',
                                                                link='https://p2p.binance.com/en/trade/TinkoffNew/BUSD?fiat=RUB',
                                                                description='Link to buy BUSD by Tinkoff RUBs on P2P Binance')
        p2pbin_busdrub_sell_tinkoff = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_TinkoffNew_SELL',
                                                                 link='https://p2p.binance.com/en/trade/sell/BUSD?fiat=RUB&payment=TinkoffNew',
                                                                 description='Link to sell BUSD by Tinkoff RUBs on P2P Binance')
        p2pbin_busdusd_sell_tinkoff = Link.objects.get_or_create(short_name='BUSDUSD_P2PBIN_TinkoffNew_SELL',
                                                                 link='https://p2p.binance.com/en/trade/sell/BUSD?fiat=USD&payment=TinkoffNew',
                                                                 description='Link to sell BUSD by Tinkoff USDs on P2P Binance')
        p2pbin_busdusd_buy_tinkoff = Link.objects.get_or_create(short_name='BUSDUSD_P2PBIN_TinkoffNew_BUY',
                                                                link='https://p2p.binance.com/en/trade/TinkoffNew/BUSD?fiat=USD',
                                                                description='Link to buy BUSD by Tinkoff USDs on P2P Binance')
            # RAIFFEISEN BANK P2P BINANCE
        p2pbin_usdtrub_buy_raiffeisen = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_RaiffeisenBankRussia_BUY',
                                                                link='https://p2p.binance.com/en/trade/RaiffeisenBankRussia/USDT?fiat=RUB',
                                                                description='Link to buy USDT by Raiffeisen RUBs on P2P Binance')
        p2pbin_usdtrub_sell_raiffeisen = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_RaiffeisenBankRussia_SELL',
                                                                 link='https://p2p.binance.com/en/trade/sell/USDT?fiat=RUB&payment=RaiffeisenBankRussia',
                                                                 description='Link to sell USDT by Raiffeisen RUBs on P2P Binance')
        p2pbin_busdrub_buy_raiffeisen = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_RaiffeisenBankRussia_BUY',
                                                                link='https://p2p.binance.com/en/trade/RaiffeisenBankRussia/BUSD?fiat=RUB',
                                                                description='Link to buy BUSD by Raiffeisen RUBs on P2P Binance')
        p2pbin_busdrub_sell_raiffeisen = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_RaiffeisenBankRussia_SELL',
                                                                 link='https://p2p.binance.com/en/trade/sell/BUSD?fiat=RUB&payment=RaiffeisenBankRussia',
                                                                 description='Link to sell BUSD by Raiffeisen RUBs on P2P Binance')

            # QIWI BANK P2P BINANCE
        p2pbin_usdtrub_buy_qiwi = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_QIWI_BUY',
                                                                   link='https://p2p.binance.com/en/trade/QIWI/USDT?fiat=RUB',
                                                                   description='Link to buy USDT by QIWI RUBs on P2P Binance')
        p2pbin_usdtrub_sell_qiwi = Link.objects.get_or_create(short_name='USDTRUB_P2PBIN_QIWI_SELL',
                                                                    link='https://p2p.binance.com/en/trade/sell/USDT?fiat=RUB&payment=QIWI',
                                                                    description='Link to sell USDT by QIWI RUBs on P2P Binance')
        p2pbin_busdrub_buy_qiwi = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_QIWI_BUY',
                                                                   link='https://p2p.binance.com/en/trade/QIWI/BUSD?fiat=RUB',
                                                                   description='Link to buy BUSD by QIWI RUBs on P2P Binance')
        p2pbin_busdrub_sell_qiwi = Link.objects.get_or_create(short_name='BUSDRUB_P2PBIN_QIWI_SELL',
                                                                    link='https://p2p.binance.com/en/trade/sell/BUSD?fiat=RUB&payment=QIWI',
                                                                    description='Link to sell BUSD by QIWI RUBs on P2P Binance')
            # Tinkoff USD change
        tinkoff_usd_change = Link.objects.get_or_create(short_name='TINKOFF_USD_CHANGE',
                                                        link='https://www.tinkoff.ru/invest/currencies/USDRUB/',
                                                        description='Link to change USD to RUB in Tinkoff investments')