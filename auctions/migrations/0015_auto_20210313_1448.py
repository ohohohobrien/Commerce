# Generated by Django 3.1.7 on 2021-03-13 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20210311_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='auction_listings', to='auctions.Categories'),
        ),
    ]