# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0010_auto_20160712_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkpoint',
            name='star',
        ),
        migrations.AddField(
            model_name='checkpoint',
            name='is_finish',
            field=models.IntegerField(null=True),
        ),
    ]
