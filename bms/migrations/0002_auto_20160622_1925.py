# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='mac',
            field=models.CharField(max_length=32, unique=True, null=True),
        ),
    ]
