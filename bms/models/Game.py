# -*- coding: utf-8 -*-
import json
from django.db import models

__author__ = 'maxijie'


class Game(models.Model):
    name = models.CharField(max_length=32)
    sale = models.IntegerField(null=True)
    body = models.CharField(max_length=256, null=True, default="")
    detail = models.CharField(max_length=8192, null=True, default="")
    configure_info = models.TextField(u"配置信息", null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self._configure_info = None

    @property
    def configure_data(self):
        if self._configure_info is not None:
            temp = self.configure_info
            if temp:
                if isinstance(temp, unicode):
                    temp = temp.decode("utf-8")
                self._configure_info = json.loads(temp)
            else:
                self._configure_info = {}

        return self._configure_info

    def save(self, *args, **kwargv):
        if self._configure_info is not None:
            self.configure_info = json.dumps(self._configure_info)

        super(Game, self).save(*args, **kwargv)
