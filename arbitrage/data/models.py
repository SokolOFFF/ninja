from datetime import datetime

from django.db import models


class Fiat(models.Model):
    name = models.CharField(max_length=10, primary_key=True)


class Payment(models.Model):
    name = models.CharField(max_length=50)
    fiat = models.ForeignKey(Fiat, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('name', 'fiat'),)


class Coin(models.Model):
    name = models.CharField(max_length=10)


# TODO: add amount range and rates
class P2POrder(models.Model):
    TYPES_CHOICES = (('BUY', 'BUY'),
                     ('SELL', 'SELL')
                     )
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    rate = models.FloatField()
    author = models.CharField(max_length=50)
    coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=TYPES_CHOICES, max_length=4)
    parsing_time = models.DateTimeField(default=datetime.now)