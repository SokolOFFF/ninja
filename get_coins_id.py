from bestchange_api import BestChange

api = BestChange()
for id in range(300):
    coin = api.currencies().get_by_id(id)
    print(coin, id)