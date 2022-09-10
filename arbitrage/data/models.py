from django.utils.timezone import now
from django.db import models


class Fiat(models.Model):
    name = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=50)
    fiat = models.ForeignKey(Fiat, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('name', 'fiat'),)

    def __str__(self):
        return f'{self.name}_{self.fiat}'


class Coin(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# TODO: add amount range
# TODO: add order link
# TODO: add user model
class P2POrder(models.Model):
    TYPES_CHOICES = (('BUY', 'BUY'),
                     ('SELL', 'SELL')
                     )
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    rate = models.FloatField()
    author = models.CharField(max_length=50)
    coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=TYPES_CHOICES, max_length=4)
    lower_limit = models.FloatField(default=0.0)
    upper_limit = models.FloatField(default=0.0)
    parsing_time = models.DateTimeField(default=now)
    def __str__(self):
        return f'P2P order {self.type} by {self.author} ' \
               f'for {self.coin} by {self.payment} with {self.rate}. Limits: {self.lower_limit} - {self.upper_limit}'

class Currency(models.Model):
    name = models.CharField(max_length=10, default='USDRUB')
    figi = models.CharField(max_length=20, default='000000')

    def __str__(self):
        return f'Currency name: {self.name}, figi: {self.figi}'


class User(models.Model):
    telegram_id = models.CharField(max_length= 20)
    money_amount = models.IntegerField(default=15000)
    spread = models.FloatField(default=1.0)
    is_subscribed = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f'Telegram id: {self.telegram_id}, money amount: {self.money_amount}, spread: {self.spread}, is subs: {self.is_subscribed}'

class Link(models.Model):
    short_name = models.CharField(max_length=20)
    link = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f'Name: {self.short_name},\n   Link: {self.link},\n   Description: {self.description}'

class Circle(models.Model):
    msg_text = models.TextField()
    variant = models.IntegerField(default=0)
    spread = models.FloatField()
    lower_limit = models.FloatField()
    upper_limit = models.FloatField()
    creating_time = models.DateTimeField(default=now)

class BestchangePayment(models.Model):
    name = models.CharField(max_length=10)
    bestchange_id = models.IntegerField()
    def __str__(self):
        return f'Name: {self.name},\n  Bestchange id: {self.bestchange_id}'
class BestchangeExchange(models.Model):
    payment_from = models.ForeignKey(BestchangePayment, on_delete=models.SET_NULL, null=True, related_name="payment_from")
    payment_to = models.ForeignKey(BestchangePayment, on_delete=models.SET_NULL, null=True, related_name="payment_to")
    rate = models.FloatField()
    min_sum = models.FloatField()
    max_sum = models.FloatField()
    exchanger_name = models.CharField(max_length=40)
    parsing_time = models.DateTimeField(default=now)


class BinanceSpotPrice(models.Model):
    symbol = models.CharField(max_length=20, default="")
    price = models.FloatField()
    parsing_time = models.DateTimeField(default=now)
