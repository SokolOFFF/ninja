# Generated by Django 4.1 on 2022-09-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_bestchangeexchange_parsing_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]
