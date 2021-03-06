# Generated by Django 3.1.7 on 2021-03-18 03:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auctionlisting_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_listings_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
