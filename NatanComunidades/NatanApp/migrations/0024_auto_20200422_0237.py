# Generated by Django 2.2.10 on 2020-04-22 02:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('NatanApp', '0023_auto_20200422_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 4, 22, 2, 37, 1, 888136, tzinfo=utc)),
        ),
    ]