# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0009_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='factory_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='order_time',
            field=models.DateTimeField(null=True),
        ),
    ]
