# -*- coding: utf-8 -*-
import json
from django.db import models
from django import forms
from bms.models.Space import Space
from bms.models.Game import Game

__author__ = 'maxijie'


class Machine(models.Model):
    game = models.OneToOneField(Game)
    space = models.ForeignKey(Space)
    # num = models.AutoField()
    code = models.CharField(max_length=512, null=True)
    qrimage_url = models.CharField(max_length=128, null=True)
    sale = models.IntegerField(null=True)
    order_id = models.CharField(max_length=32, null=True, default="")
    mac = models.CharField(max_length=32, null=True, unique=True)
    device_info = models.TextField(u"设备信息", default="", null=True)
    configure_info = models.TextField(u"配置信息", default="", null=True)
    repair_info = models.TextField(u"维修备注", default="", null=True)
    factory_time = models.DateTimeField(null=True)  # 出厂时间
    order_time = models.DateTimeField(null=True)  # 订单生成时间
    repair_time = models.DateTimeField(null=True)  # 保修期
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Machine, self).__init__(*args, **kwargs)
        self._device_info = None
        self._configure_info = None
        self._repair_info = None

    @property
    def device_data(self):
        if self._device_info is None:
            temp = self.device_info
            if temp:
                if isinstance(temp, unicode):
                    temp = temp.encode("utf-8")
                self._device_info = json.loads(temp)
            else:
                self._device_info = {}

        return self._device_info

    @property
    def configure_data(self):
        if self._configure_info is None:
            temp = self.configure_info
            if temp:
                if isinstance(temp, unicode):
                    temp = temp.encode("utf-8")
                self._configure_info = json.loads(temp)
            else:
                self._configure_info = {}

        return self._configure_info

    @property
    def repair_data(self):
        if self._repair_info is None:
            temp = self.repair_info
            if temp:
                if isinstance(temp, unicode):
                    temp = temp.encode("utf-8")
                self._repair_info = json.loads(temp)
            else:
                self._repair_info = {}

        return self._repair_info

    def save(self, *args, **kwargv):
        if self._device_info is not None:
            self.device_info = json.dumps(self._device_info)

        if self._configure_info is not None:
            self.configure_info = json.dumps(self._configure_info)

        if self._repair_info is not None:
            self.repair_info = json.dumps(self._repair_info)

        super(Machine, self).save(*args, **kwargv)


class MachineForm(forms.Form):
    game_name = forms.CharField(label="游戏名字", max_length=32)
    mac = forms.CharField(label='mac', max_length=128)
    order_id = forms.CharField(label='订单号', max_length=128)
    device_info = forms.CharField(label='设备信息', max_length=1024, required=False)
    configure_info = forms.CharField(
        label='配置信息', max_length=1024, required=False)
    repair_info = forms.CharField(label='维修备注', max_length=1024, required=False)
    factory_time = forms.CharField(label='出厂时间', max_length=32)
    order_time = forms.CharField(label='订单生成时间', max_length=32)
    repair_time = forms.CharField(label='保修期', max_length=32)
    name = forms.CharField(label='场地名称', max_length=32)
    province = forms.CharField(label='省', max_length=8)
    city = forms.CharField(label='市', max_length=8)
    address = forms.CharField(label='具体位置', max_length=128)
    # split_ratio = forms.CharField(label='分成比例', max_length=32)
    # split_ratio2 = forms.CharField(label='分成比例2', max_length=32)
    # split_ratio3 = forms.CharField(label='分成比例3', max_length=32)
