# TODO: add more coins:
# TODO:      add coins names to array 'coins'
# TODO:      add coins' ids to 'bestchangeCoinId'
# TODO:      add new links to bestchangeFactLinks
# TODO:      add to acceptable spots


# 31 coins here -->
coins = ['BTC', 'ETH', 'LTC', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 'TRX', 'SHIB', 'AVAX', 'BNB', 'KMD', 'LUNA', 'MATIC',
         'UNI', 'LINK', 'XLM', 'NEAR', 'ATOM', 'XMR', 'ALGO', 'VET', 'MANA', 'XTZ', 'EOS', 'MKR', 'ZEC', 'NEO', 'BAT',
         'WAVES']
stable_coins = ['USDT', 'BUSD']

bestchangeCoinId = {
    'BTC': 93,
    'ETH': 139,
    'LTC': 99,
    'XRP': 161,
    'ADA': 181,
    'SOL': 82,
    'DOGE': 115,
    'DOT': 201,
    'TRX': 185,
    'SHIB': 32,
    'AVAX': 217,
    'BNB': 16,
    'KMD': 134,
    'LUNA': 2,
    'MATIC': 138,
    'UNI': 202,
    'LINK': 197,
    'XLM': 182,
    'NEAR': 76,
    'ATOM': 198,
    'XMR': 149,
    'ALGO': 216,
    'VET': 8,
    'MANA': 227,
    'XTZ': 175,
    'EOS': 178,
    'MKR': 213,
    'ZEC': 162,
    'NEO': 177,
    'BAT': 61,
    'WAVES': 133
}

bestchangeFastLinks = {
    'BTC': 'https://www.bestchange.ru/qiwi-to-bitcoin.html',
    'ETH': 'https://www.bestchange.ru/qiwi-to-ethereum.html',
    'LTC': 'https://www.bestchange.ru/qiwi-to-litecoin.html',
    'XRP': 'https://www.bestchange.ru/qiwi-to-ripple.html',
    'ADA': 'https://www.bestchange.ru/qiwi-to-cardano.html',
    'SOL': 'https://www.bestchange.ru/qiwi-to-solana.html',
    'DOGE': 'https://www.bestchange.ru/qiwi-to-dogecoin.html',
    'DOT': 'https://www.bestchange.ru/qiwi-to-polkadot.html',
    'TRX': 'https://www.bestchange.ru/qiwi-to-tron.html',
    'SHIB': 'https://www.bestchange.ru/qiwi-to-shiba-inu-bep20.html',
    'AVAX': 'https://www.bestchange.ru/qiwi-to-avalanche.html',
    'BNB': 'https://www.bestchange.ru/qiwi-to-binance-coin-bep2.html',
    'KMD': 'https://www.bestchange.ru/qiwi-to-komodo.html',
    'LUNA': 'https://www.bestchange.ru/qiwi-to-terra.html',
    'MATIC': 'https://www.bestchange.ru/qiwi-to-polygon.html',
    'UNI': 'https://www.bestchange.ru/qiwi-to-uniswap.html',
    'LINK': 'https://www.bestchange.ru/qiwi-to-chainlink.html',
    'XLM': 'https://www.bestchange.ru/qiwi-to-stellar.html',
    'NEAR': 'https://www.bestchange.ru/qiwi-to-near.html',
    'ATOM': 'https://www.bestchange.ru/qiwi-to-cosmos.html',
    'XMR': 'https://www.bestchange.ru/qiwi-to-monero.html',
    'ALGO': 'https://www.bestchange.ru/qiwi-to-algorand.html',
    'VET': 'https://www.bestchange.ru/qiwi-to-vechain.html',
    'MANA': 'https://www.bestchange.ru/qiwi-to-decentraland.html',
    'XTZ': 'https://www.bestchange.ru/qiwi-to-tezos.html',
    'EOS': 'https://www.bestchange.ru/qiwi-to-eos.html',
    'MKR': 'https://www.bestchange.ru/qiwi-to-maker.html',
    'ZEC': 'https://www.bestchange.ru/qiwi-to-zcash.html',
    'NEO': 'https://www.bestchange.ru/qiwi-to-neo.html',
    'BAT': 'https://www.bestchange.ru/qiwi-to-bat.html',
    'WAVES': 'https://www.bestchange.ru/qiwi-to-waves.html'
}

acceptableSpots = {
    'BTC': ['USDT', 'BUSD'],
    'ETH': ['USDT', 'BUSD'],
    'LTC': ['USDT', 'BUSD'],
    'XRP': ['USDT', 'BUSD'],
    'ADA': ['USDT', 'BUSD'],
    'SOL': ['USDT', 'BUSD'],
    'DOGE': ['USDT', 'BUSD'],
    'DOT': ['USDT', 'BUSD'],
    'TRX': ['USDT', 'BUSD'],
    'SHIB': ['USDT', 'BUSD'],
    'AVAX': ['USDT', 'BUSD'],
    'BNB': ['USDT', 'BUSD'],
    'KMD': ['USDT'],
    'LUNA': ['USDT', 'BUSD'],
    'MATIC': ['USDT', 'BUSD'],
    'UNI': ['USDT', 'BUSD'],
    'LINK': ['USDT', 'BUSD'],
    'XLM': ['USDT', 'BUSD'],
    'NEAR': ['USDT', 'BUSD'],
    'ATOM': ['USDT', 'BUSD'],
    'XMR': ['USDT', 'BUSD'],
    'ALGO': ['USDT', 'BUSD'],
    'VET': ['USDT', 'BUSD'],
    'MANA': ['USDT', 'BUSD'],
    'XTZ': ['USDT', 'BUSD'],
    'EOS': ['USDT', 'BUSD'],
    'MKR': ['USDT', 'BUSD'],
    'ZEC': ['USDT', 'BUSD'],
    'NEO': ['USDT', 'BUSD'],
    'BAT': ['USDT', 'BUSD'],
    'WAVES': ['USDT', 'BUSD']
}

binanceP2PFastLinks = {
    'USDT': 'https://p2p.binance.com/en/trade/sell/USDT?fiat=RUB&payment=Tinkoff',
    'BUSD': 'https://p2p.binance.com/en/trade/sell/BUSD?fiat=RUB&payment=Tinkoff'
}

P2PFastLinks = {
    'USDT': {
        'SELL': 'https://p2p.binance.com/en/trade/sell/USDT?fiat=USD&payment=Tinkoff',
        'BUY': 'https://p2p.binance.com/en/trade/buy/USDT?fiat=RUB&payment=Tinkoff'
    },
    'BUSD': {
        'SELL': 'https://p2p.binance.com/en/trade/sell/BUSD?fiat=USD&payment=Tinkoff',
        'BUY': 'https://p2p.binance.com/en/trade/buy/BUSD?fiat=RUB&payment=Tinkoff'
    }
}
