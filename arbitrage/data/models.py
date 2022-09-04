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
    parsing_time = models.DateTimeField(default=now)
    def __str__(self):
        return f'P2P order {self.type} by {self.author} ' \
               f'for {self.coin} by {self.payment} with {self.rate}'

class Currencies(models.Model):
    name = models.CharField(max_length=10, default='USDRUB')
    figi = models.CharField(max_length=20, default='000000')

    def __str__(self):
        return f'Currency name: {self.name}, figi: {self.figi}'
