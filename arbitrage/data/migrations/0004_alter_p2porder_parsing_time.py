# Generated by Django 4.1 on 2022-08-22 21:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_p2porder_parsing_time_alter_payment_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p2porder',
            name='parsing_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
