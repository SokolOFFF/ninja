# Generated by Django 4.1 on 2022-09-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_user_rename_currencies_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='money_amount',
            field=models.IntegerField(default=15000),
        ),
        migrations.AlterField(
            model_name='user',
            name='spread',
            field=models.FloatField(default=1.0),
        ),
    ]