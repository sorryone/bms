# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0004_auto_20160623_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consume',
            name='order_id',
        ),
    ]
