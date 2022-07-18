import telebot
import requests
import random
from bs4 import BeautifulSoup
from Changer import BestChange
from time import sleep
from decimal import Decimal

import config
import database
import coins_and_links

bot = telebot.TeleBot(config.TOKEN_SENDLER)

global api
api = BestChange(cache_seconds=1, load=False)

sellersForSCoin = {}
marketPriceForCoin = {}
bestExchangersForCoin = {}

#TODO: UNDERSTAND HOW TO GET BESTCHANGERS FASTER

#TODO: GET RID OF SPAM

#TODO: CHECK COMMISSIONS

def find_stable_coins_price():
    url = config.BP2P_URL
    for scoin in coins_and_links.stable_coins:
        sellers = []
        param = {
            "asset": f"{scoin}",
            "fiat": "RUB",
            "page": 1,
            "payTypes": ['Tinkoff'],
            "rows": 10,
            "tradeType": "SELL"
        }
        headers = {
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
        respond = requests.post(url=url, headers=headers, json=param)
        if respond.status_code == 200:
            data = respond.json()['data']
            for ad in data:
                seller = {}
                seller['nickname'] = ad['advertiser']['nickName']
                seller['price'] = Decimal(ad['adv']['price'])
                seller['minamount'] = Decimal(ad['adv']['minSingleTransAmount'])
                seller['maxamount'] = Decimal(ad['adv']['dynamicMaxSingleTransAmount'])
                seller['available'] = Decimal(ad['adv']['tradableQuantity'])
                seller['finishrate'] = Decimal(ad['advertiser']['monthFinishRate']) * 100
                sellers.append(seller)
        else:
            print(f"Cant connect to Binance P2P, status code: {respond.status_code}")
        sellersForSCoin[scoin] = sellers


def parse_market_price():
    url = config.BAPI_BASE+config.BTICKER_PRICE_PATH
    symbols = []
    for scoin in coins_and_links.stable_coins:
        for coin in coins_and_links.coins:
            symbols.append(f"{coin}{scoin}")

    symbols = str(symbols).replace(' ', '').replace("'", '"')
    param = {'symbols' : symbols}
    respond = requests.get(url=url, params=param)
    data = respond.json()
    for symbol in data:
        marketPriceForCoin[symbol['symbol']] = symbol['price']

def parse_changers():
    api.load()
    rates = api.rates()
    for coin in coins_and_links.coins:
        coinRates = rates.filter(63, coins_and_links.bestchangeCoinId[coin])
        exchangers = []
        for rate in coinRates:
            exchanger = {}
            exchanger['name'] = api.exchangers().get_by_id(rate['exchange_id'])
            exchanger['rate'] = rate['rate']
            exchanger['minsum'] = rate['min_sum']
            exchanger['maxsum'] = rate['max_sum']
            exchangers.append(exchanger)
        bestExchangersForCoin[coin] = exchangers



def count_futureAmount(subLimit, changerPrice, marketPrice, scoinPrice):
    profit = Decimal(subLimit) / Decimal(changerPrice) * Decimal(marketPrice) * Decimal(scoinPrice)
    return profit

def sendAll(text):
    for id in database.get_subscribers():
        try:
            bot.send_message(id, text=text, parse_mode='html')
        except Exception as e:
            print(e, id)

def main():
    print(f'parsing bestchange')
    parse_changers()
    print('parsing market price')
    parse_market_price()
    print('parsing p2p')
    find_stable_coins_price()

    for coin in coins_and_links.coins:
        for scoin in coins_and_links.stable_coins:
            if scoin in coins_and_links.acceptableSpots[coin]:
                marketPrice = marketPriceForCoin[coin+scoin]
                for sub in database.get_subscribers():
                    for p2pseller in sellersForSCoin[scoin]:
                        subLimit = Decimal(database.get_moneyamount(sub))
                        for exchanger in bestExchangersForCoin[coin]:
                            changerPrice = exchanger['rate']
                            if subLimit > p2pseller['minamount'] and subLimit < p2pseller['maxamount'] and subLimit > exchanger['minsum'] and subLimit < exchanger['maxsum']:
                                futureAmountInRubs = count_futureAmount(subLimit, changerPrice, marketPrice, p2pseller['price'])
                                profit = (futureAmountInRubs-subLimit) / subLimit * 100
                                if Decimal(futureAmountInRubs) > Decimal(subLimit) and Decimal(profit) >= Decimal(database.get_threshold(sub)):
                                    sendAll(f"<b>RATS!!!</b>\n\n<i>Available to do like this:</i>\n   buy <b>{coin}</b> on <i><u>{exchanger['name']}</u></i> by <b><i>{format(changerPrice, '.9f')} RUBs</i></b>\n   sell <b>{coin}</b> by <b><i>{marketPrice} {scoin}</i></b> on Binance spot market\n   sell <b>{scoin}</b> by <b><i>{p2pseller['price']} RUBs</i></b> to <u>{p2pseller['nickname']}</u>\n\n   (<i>available to sell:</i> <b>{p2pseller['available']} {scoin}</b>,\n   <i>min amount:</i> <b>{p2pseller['minamount']} RUBs</b>,\n   <i>max amount:</i> <b>{p2pseller['maxamount']} RUBs</b>)\n\n<i>Seller info:</i>\n   <i>nick name:</i> <u>{p2pseller['nickname']}</u>\n   <i>finish rate:</i> <u>{str(p2pseller['finishrate'])[0:5:]}%</u>\n\n<i>Profit:</i>\n   <b>{subLimit}</b> RUBs -> <b>{str(futureAmountInRubs)[0:len(str(futureAmountInRubs))-18:]}</b> RUBs\n   <i>profit:</i> <b>{str(profit)[0:8:]}%</b>\n\n<i>Fast links:</i>\n   <i>Bestchange: <u>{coins_and_links.bestchangeFastLinks[coin]}</u></i>\n   <i>Binance spot: <u>https://www.binance.com/en/trade/{coin}_{scoin}?theme=dark&type=spot</u></i>\n   <i>Binance P2P: <u>{coins_and_links.binanceP2PFastLinks[scoin]}</u></i>\n")
                                    print(f"Found idea for: {sub}. Profit: {str(profit)[0:8:]}%")


print('SEARCHING FOR BITCHES!!!')
while(True):
    main()
