# Generated by Django 2.2 on 2020-05-12 13:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('NatanApp', '0032_auto_20200511_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 5, 12, 13, 41, 3, 326638, tzinfo=utc)),
        ),
    ]
