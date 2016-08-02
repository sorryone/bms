# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0005_remove_consume_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='city',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='players',
            name='country',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='players',
            name='province',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='players',
            name='sex',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='players',
            name='avatar_file',
            field=models.CharField(max_length=256),
        ),
    ]
