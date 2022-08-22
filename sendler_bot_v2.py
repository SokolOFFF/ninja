import telebot
import requests
from decimal import Decimal

import config
import database
import coins_and_links

bot = telebot.TeleBot(config.TOKEN_SENDLER)


sellersForSCoin = {}
buyersForSCoin = {}

def find_sellers_for_stable_coin():
    url = config.BP2P_URL
    for scoin in coins_and_links.stable_coins:
        sellers = []
        param = {
            "asset": f"{scoin}",
            "fiat": "USD",
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
        try:
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
                sellersForSCoin[scoin] = sellers
            else:
                print(f"Cant connect to Binance P2P, status code: {respond.status_code}")
                find_sellers_for_stable_coin()
                return 1
        except Exception as e:
            print("Error occurred while parsing sellers. Error: ", e)
            find_sellers_for_stable_coin()
            return 1


def find_buyers_for_stable_coin():
    url = config.BP2P_URL
    for scoin in coins_and_links.stable_coins:
        buyers = []
        param = {
            "asset": f"{scoin}",
            "fiat": "RUB",
            "page": 1,
            "payTypes": ['Tinkoff'],
            "rows": 10,
            "tradeType": "BUY"
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
        try:
            respond = requests.post(url=url, headers=headers, json=param)
            if respond.status_code == 200:
                data = respond.json()['data']
                for ad in data:
                    buyer = {}
                    buyer['nickname'] = ad['advertiser']['nickName']
                    buyer['price'] = Decimal(ad['adv']['price'])
                    buyer['minamount'] = Decimal(ad['adv']['minSingleTransAmount'])
                    buyer['maxamount'] = Decimal(ad['adv']['dynamicMaxSingleTransAmount'])
                    buyer['available'] = Decimal(ad['adv']['tradableQuantity'])
                    buyer['finishrate'] = Decimal(ad['advertiser']['monthFinishRate']) * 100
                    buyers.append(buyer)
                buyersForSCoin[scoin] = buyers
            else:
                print(f"Cant connect to Binance P2P, status code: {respond.status_code}")
                find_buyers_for_stable_coin()
                return 1
        except Exception as e:
            print("Error occurred while parsing buyers. Error: ", e)
            find_buyers_for_stable_coin()
            return 1



def get_exchange_rate():
    try:
        respond = requests.get(config.TINKOFF_EXCHANGE_API)
        if respond.status_code == 200:
            rates = respond.json()['payload']['rates']
            for rate in rates:
                if rate['category'] == 'DebitCardsTransfers' and rate['fromCurrency']['name'] == 'USD' and rate['toCurrency']['name'] == 'RUB':
                    tinkoffRate = Decimal(rate['buy'])
                    return tinkoffRate
        else:
            return get_exchange_rate()
    except Exception as e:
        print("Error occurred while parsing rate. Error: ", e)
        return get_exchange_rate()



def count_futureAmount(subLimit, buyerPrice, sellerPrice, exchangeRate):
    profit = Decimal(subLimit) / Decimal(buyerPrice) * Decimal(sellerPrice) * Decimal(exchangeRate)
    return profit

def sendAll(text):
    for id in database.get_subscribers():
        try:
            bot.send_message(id, text=text, parse_mode='html')
        except Exception as e:
            print(e, id)

def main():
    print('finding buyers..')
    find_buyers_for_stable_coin()
    print('finding sellers..')
    find_sellers_for_stable_coin()
    print('finding exchange rate..')
    tinkoffRate = get_exchange_rate()

    for scoin in coins_and_links.stable_coins:
        for sub in database.get_subscribers():
            subLimit = Decimal(database.get_moneyamount(sub))
            for p2pseller in sellersForSCoin[scoin]:
                sellerPrice = p2pseller['price']
                for p2pbuyer in buyersForSCoin[scoin]:
                    buyerPrice = p2pbuyer['price']
                    if subLimit > p2pbuyer['minamount'] and subLimit < p2pbuyer['maxamount']: # add checker with seller
                        futureAmountInRubs = count_futureAmount(subLimit, buyerPrice, sellerPrice, tinkoffRate)
                        profit = (futureAmountInRubs-subLimit) / subLimit * 100
                        if Decimal(profit) >= 0.0:
                            print('found idea > 0%')
                        if Decimal(futureAmountInRubs) > Decimal(subLimit) and Decimal(profit) >= Decimal(database.get_threshold(sub)):
                            sendAll(f"<b>RATS!!!</b>\n\n<i>Available to do like this:</i>\n" \
                                        f"   buy <b>{scoin}</b> on <i><u>{p2pbuyer['nickname']}</u></i> by <b><i>{format(p2pbuyer['price'], '.4f')} RUBs</i></b>\n" \
                                        f"   sell <b>{scoin}</b> to <i><u>{p2pseller['nickname']}</u></i> by <b><i>{format(p2pseller['price'], '.4f')} USD</i></b>\n" \
                                        f"   exchange <b>USD</b> by <b><i>{format(tinkoffRate, '.4f')} RUBs</i></b> on <u>Tinkoff</u>\n\n" \
                                        f"   <i>Seller info:</i>\n" \
                                        f"   <i>available to buy:</i> <b>{p2pbuyer['available']} {scoin}</b>,\n" \
                                        f"   <i>min amount:</i> <b>{p2pbuyer['minamount']} RUBs</b>,\n" \
                                        f"   <i>max amount:</i> <b>{p2pbuyer['maxamount']} RUBs</b>\n" \
                                        f"   <i>nick name:</i> <u>{p2pbuyer['nickname']}</u>\n" \
                                        f"   <i>finish rate:</i> <u>{str(p2pbuyer['finishrate'])[0:5:]}%</u>\n\n" \
                                        f"   <i>Buyer info:</i>\n" \
                                        f"   <i>available to buy:</i> <b>{p2pseller['available']} {scoin}</b>,\n" \
                                        f"   <i>min amount:</i> <b>{p2pseller['minamount']} USDs</b>,\n" \
                                        f"   <i>max amount:</i> <b>{p2pseller['maxamount']} USDs</b>\n" \
                                        f"   <i>nick name:</i> <u>{p2pseller['nickname']}</u>\n" \
                                        f"   <i>finish rate:</i> <u>{str(p2pseller['finishrate'])[0:5:]}%</u>\n\n" \
                                        f"<i>Profit:</i>\n" \
                                        f"   <b>{subLimit}</b> RUBs -> <b>{str(futureAmountInRubs)[0:len(str(futureAmountInRubs))-18:]}</b> RUBs\n" \
                                        f"   <i>profit:</i> <b>{str(profit)[0:8:]}%</b>\n\n" \
                                        f"<i>Fast links:</i>\n" \
                                        f"   <i>P2P buy: <u>{coins_and_links.P2PFastLinks[scoin]['BUY']}</u></i>\n" \
                                        f"   <i>P2P sell: <u>{coins_and_links.P2PFastLinks[scoin]['SELL']}</u></i>\n" \
                                        f"   <i>Tinkoff rate: <u>'posmotri v banke'</u></i>\n")
                            print(f"Found idea for: {sub}. Profit: {str(profit)[0:8:]}%")


print('SEARCHING FOR BITCHES!!!')
while True:
    main()
