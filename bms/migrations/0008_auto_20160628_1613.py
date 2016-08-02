# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0007_checkpoint_stage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playergamedata',
            name='player',
            field=models.OneToOneField(related_name='playerdata', to='bms.Players'),
        ),
    ]
