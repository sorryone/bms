# -*- coding: utf-8 -*-
from django.db import models
from bms.models.Business import Business

__author__ = 'maxijie'


class Space(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business)
    province = models.CharField(max_length=32)  # 省
    city = models.CharField(max_length=32)
    address = models.CharField(max_length=255)
    split_ratio = models.FloatField(null=True)
    split_ratio2 = models.FloatField(null=True)
    split_ratio3 = models.FloatField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
