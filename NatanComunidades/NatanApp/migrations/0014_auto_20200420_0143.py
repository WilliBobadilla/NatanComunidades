# Generated by Django 2.2 on 2020-04-20 01:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('NatanApp', '0013_auto_20200419_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 4, 20, 1, 43, 5, 977835, tzinfo=utc)),
        ),
    ]