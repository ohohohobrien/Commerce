# Generated by Django 3.1.7 on 2021-03-08 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210308_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.FloatField(),
        ),
    ]
