import requests

from data.models import P2POrder, Fiat, Payment, Coin

BP2P_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

BINANCE_REQUEST_HEADER = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}


def get_new_p2p_orders():
    print('Get new p2p orders ...')
    for trade_type in P2POrder.TYPES_CHOICES:
        for coin in Coin.objects.all():
            print(f'Handle coin {coin.name}')
            # TODO: check that the system can send 1 request with all possible payments
            for payment in Payment.objects.all():
                print(f'By {payment.name}')
                param = {
                    'asset': coin.name,
                    'fiat': payment.fiat.name,
                    'page': 1,
                    'payTypes': [payment.name],
                    'rows': 10,
                    'tradeType': trade_type[0]
                }
                print(param)
                respond = requests.post(url=BP2P_URL, headers=BINANCE_REQUEST_HEADER,
                                        json=param, timeout=10)
                if respond.status_code == 200:
                    try:
                        data = respond.json()['data']
                        if not data is None:
                            # TODO: make insertion using only 1 request
                            for order in data:
                                P2POrder.objects.create(payment=payment, coin=coin,
                                                        rate=float(order['adv']['price']),
                                                        author=order['advertiser']['nickName'],
                                                        type=trade_type[0], )
                        else:
                            print(f'Response is empty. Respond: {respond.json()}')
                    except Exception as e:
                        raise ValueError("Error occurred while parsing sellers. Error: ", e)
                else:
                    raise RuntimeError(f'Cant connect to Binance P2P, status code: {respond.status_code}')
    print('Finish of p2p orders getting')
# TODO: make deletion of old orders
