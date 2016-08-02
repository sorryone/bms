# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0003_auto_20160623_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consume',
            name='wechat',
        ),
        migrations.AddField(
            model_name='consume',
            name='bank_type',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='consume',
            name='fee_type',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='consume',
            name='out_trade_no',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='consume',
            name='trade_type',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='consume',
            name='transaction_id',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='body',
            field=models.CharField(default=b'', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='detail',
            field=models.CharField(default=b'', max_length=8192, null=True),
        ),
        migrations.AddField(
            model_name='players',
            name='subscribe',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
