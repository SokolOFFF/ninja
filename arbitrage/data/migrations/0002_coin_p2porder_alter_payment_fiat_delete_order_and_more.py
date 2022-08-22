# Generated by Django 4.1 on 2022-08-22 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='P2POrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('author', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=4)),
                ('coin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.coin')),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='fiat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.fiat'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.AddField(
            model_name='p2porder',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.payment'),
        ),
    ]
