from tinkoff.invest import Client

TINKOFF_TOKEN = 't.6fnOuctj37giwnpnjIYCflRrgzAIJBGtFBO4ttYO43oGCvRC7fnMQ6PPWu6Byk-yGVTKtVAz2BAVNM93tcrFzA'

def convert_price_to_float (price):
    float_price = price.units + price.nano / 10**9
    return float_price

def get_rate_of(figi='USD000UTSTOM'):
    with Client(TINKOFF_TOKEN) as client:
        market_data = client.market_data
        lastprice = convert_price_to_float(market_data.get_last_prices(figi=[figi]).last_prices[0].price)
        return lastprice
