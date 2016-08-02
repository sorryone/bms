# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0006_auto_20160627_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='stage_id',
            field=models.IntegerField(null=True),
        ),
    ]
