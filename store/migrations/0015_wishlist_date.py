# Generated by Django 3.2.11 on 2022-01-30 05:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20220130_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
