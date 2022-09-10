import requests

from data.models import Coin, CryptoCurrency, BinanceSpotPrice

def get_cryptocurrencies_prices():
    url = 'https://api.binance.com/api/v3/ticker/price'

    symbols = []
    stable_coins = Coin.objects.all()
    cryptocurrencies = CryptoCurrency.objects.all()

    print("Getting binance spot prices..")

    for scoin in stable_coins:
        for coin in cryptocurrencies:
            symbols.append(f"{coin}{scoin}")

    symbols = str(symbols).replace(' ', '').replace("'", '"')
    param = {'symbols': symbols}
    try:
        respond = requests.get(url=url, params=param)
        data = respond.json()
        for symbol in data:
            cryptocurrency_price = BinanceSpotPrice.objects.get_or_create(symbol=symbol['symbol'], price=symbol['price'])

    except Exception as e:
        print(e)

    print("Finished getting prices")