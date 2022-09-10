from exchange_parser.bestchange_api import BestChange
from data.models import BestchangePayment, BestchangeExchange

api = BestChange(cache_seconds=1, load=False)

def get_new_bestchange_exchanges():
    print('Getting bestchange rates..')
    api.load()
    all_rates = api.rates()
    print('Parsing rates..')
    payments = BestchangePayment.objects.all()
    for payment_from in payments:
        for payment_to in payments:
            if payment_to.name == payment_from.name:
                continue
            current_rates = all_rates.filter(payment_from.bestchange_id, payment_to.bestchange_id)
            for rate in current_rates:
                name = api.exchangers().get_by_id(rate['exchange_id'])
                price = rate['rate']
                min_sum = rate['min_sum']
                max_sum = rate['max_sum']
                BestchangeExchange.objects.get_or_create(payment_from=payment_from, payment_to=payment_to, rate=price, min_sum=min_sum, max_sum=max_sum, exchanger_name=name)


    print('Finish of parsing..')