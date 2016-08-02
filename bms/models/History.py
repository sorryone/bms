# -*- coding: utf-8 -*-
from django.db import models

__author__ = 'maxijie'


class History(models.Model):
    order_id = models.CharField(max_length=32, null=True)
    mac_type = models.CharField(max_length=32)
    pid = models.IntegerField(null=True)
    state = models.CharField(max_length=32)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
