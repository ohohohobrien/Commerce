# Generated by Django 3.1.7 on 2021-03-18 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210318_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='time_posted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
