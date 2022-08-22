from django.db import models


class Fiat(models.Model):
    name = models.CharField(max_length=10, primary_key=True)


class Payment(models.Model):
    name = models.CharField(max_length=50)
    fiat = models.ForeignKey(Fiat, on_delete=models.SET_NULL)


class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    rate = models.FloatField()
    author = models.CharField(max_length=50)
