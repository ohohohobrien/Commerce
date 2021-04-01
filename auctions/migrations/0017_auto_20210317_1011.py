# Generated by Django 3.1.7 on 2021-03-17 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210316_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='auction_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placed_bids', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placed_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]