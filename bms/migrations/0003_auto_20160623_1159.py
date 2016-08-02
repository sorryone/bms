# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0002_auto_20160622_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='qrimage_url',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='code',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
