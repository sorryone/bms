# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyer_name', models.CharField(default=b'', max_length=32)),
                ('buyer_mobile', models.CharField(max_length=16)),
                ('use_name', models.CharField(default=b'', max_length=32, null=True)),
                ('use_mobile', models.CharField(max_length=16)),
                ('address', models.CharField(default=b'', max_length=32, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.ForeignKey(related_name='businessdata', to='bms.Business')),
            ],
        ),
        migrations.CreateModel(
            name='CheckPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('score', models.IntegerField(null=True)),
                ('star', models.IntegerField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id', models.CharField(max_length=32)),
                ('wechat', models.CharField(max_length=32)),
                ('amount', models.IntegerField(default=None)),
                ('amount_time', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(to='bms.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sale', models.IntegerField(null=True)),
                ('configure_info', models.TextField(null=True, verbose_name='\u914d\u7f6e\u4fe1\u606f')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32, null=True)),
                ('sale', models.IntegerField(null=True)),
                ('order_id', models.CharField(default=b'', max_length=32, null=True)),
                ('mac', models.CharField(max_length=32, null=True)),
                ('device_info', models.TextField(default=b'', null=True, verbose_name='\u8bbe\u5907\u4fe1\u606f')),
                ('configure_info', models.TextField(default=b'', null=True, verbose_name='\u914d\u7f6e\u4fe1\u606f')),
                ('repair_info', models.TextField(default=b'', null=True, verbose_name='\u7ef4\u4fee\u5907\u6ce8')),
                ('factory_time', models.DateTimeField(auto_now=True, null=True)),
                ('order_time', models.DateTimeField(auto_now=True, null=True)),
                ('repair_time', models.DateTimeField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
                ('game', models.OneToOneField(to='bms.Game')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGameData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('star', models.IntegerField(null=True)),
                ('score', models.IntegerField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(related_name='playerdata', to='bms.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('avatar_file', models.CharField(max_length=128)),
                ('wechat', models.CharField(max_length=32)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=255)),
                ('split_ratio', models.FloatField(null=True)),
                ('split_ratio2', models.FloatField(null=True)),
                ('split_ratio3', models.FloatField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(to='bms.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p_id', models.CharField(default=b'', unique=True, max_length=32)),
                ('username', models.CharField(default=b'', max_length=255)),
                ('show_pwd', models.CharField(max_length=128, null=True)),
                ('password', models.CharField(max_length=128)),
                ('salt', models.CharField(max_length=16)),
                ('email', models.CharField(default=b'', max_length=255)),
                ('mobile', models.CharField(default=b'', max_length=16)),
                ('id_card', models.CharField(max_length=32, null=True)),
                ('permission', models.CharField(default=b'business', max_length=32)),
                ('avatar_file', models.CharField(max_length=128)),
                ('sex', models.IntegerField(default=None, null=True)),
                ('birthday', models.IntegerField(default=None, null=True)),
                ('project_type', models.CharField(max_length=15, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='playergamedata',
            name='player',
            field=models.ForeignKey(related_name='playerdata', to='bms.Players'),
        ),
        migrations.AddField(
            model_name='machine',
            name='space',
            field=models.ForeignKey(to='bms.Space'),
        ),
        migrations.AddField(
            model_name='consume',
            name='game',
            field=models.ForeignKey(to='bms.Game'),
        ),
        migrations.AddField(
            model_name='consume',
            name='machine',
            field=models.ForeignKey(to='bms.Machine'),
        ),
        migrations.AddField(
            model_name='consume',
            name='player',
            field=models.ForeignKey(to='bms.Players'),
        ),
        migrations.AddField(
            model_name='consume',
            name='space',
            field=models.ForeignKey(to='bms.Space'),
        ),
        migrations.AddField(
            model_name='checkpoint',
            name='players',
            field=models.ForeignKey(to='bms.Players'),
        ),
        migrations.AddField(
            model_name='businessgame',
            name='game',
            field=models.ForeignKey(related_name='businessdata', to='bms.Game'),
        ),
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.OneToOneField(to='bms.Users', to_field=b'p_id'),
        ),
    ]
