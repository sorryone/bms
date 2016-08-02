# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0011_auto_20160712_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='is_finish',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
