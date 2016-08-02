# -*- coding: utf-8 -*-
from django.db import models
from bms.models.Game import Game

__author__ = 'maxijie'


class Players(models.Model):
    city = models.CharField(max_length=128, null=True)
    country = models.CharField(max_length=128, null=True)
    province = models.CharField(max_length=128, null=True)
    sex = models.CharField(max_length=16, null=True)
    name = models.CharField(max_length=255)
    avatar_file = models.CharField(max_length=256)
    wechat = models.CharField(max_length=32)
    subscribe = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


class PlayerGameData(models.Model):
    player = models.OneToOneField(Players, related_name='playerdata')
    game = models.ForeignKey(Game, related_name='playerdata')
    star = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
