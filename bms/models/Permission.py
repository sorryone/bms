# -*- coding: utf-8 -*-
import json
from django.db import models
from bms.models.Users import Users

__author__ = 'maxijie'


class Permission(models.Model):
    user = models.OneToOneField(Users, to_field="p_id")
    name = models.CharField(max_length=16)
    permissions = models.TextField(u"权限(json)", null=True)

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)
        self._permissions = None

    @property
    def permissions_data(self):
        if self._permissions is None:
            temp = self.permissions
            if temp:
                if isinstance(temp, unicode):
                    temp = temp.encode("utf-8")
                self._permissions = json.loads(temp)
            else:
                self._permissions = {}
        return self._permissions

    def save(self, *args, **kwargv):
        if self._permissions is not None:
            self.permissions = json.dumps(self._permissions)
        super(Permission, self).save(*args, **kwargv)
