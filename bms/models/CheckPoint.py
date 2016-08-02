# -*- coding: utf-8 -*-
from django.db import models
from bms.models.Players import Players

__author__ = 'maxijie'


class CheckPoint(models.Model):
    players = models.ForeignKey(Players)
    stage_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    score = models.IntegerField(null=True)  # 本关最高积分
    is_finish = models.IntegerField(null=True, default=0)  # 是否过关
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
