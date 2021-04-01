# Generated by Django 3.1.7 on 2021-03-11 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210310_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='cauction_listings', to='auctions.Comments'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aauction_listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.ManyToManyField(blank=True, related_name='zauction_listings', to='auctions.Bids'),
        ),
    ]
