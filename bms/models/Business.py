# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from bms.models.Users import Users
from bms.models.Game import Game

__author__ = 'maxijie'


class Business(models.Model):
    user = models.OneToOneField(Users, to_field="p_id")
    buyer_name = models.CharField(max_length=32, default="")
    buyer_mobile = models.CharField(max_length=16)
    use_name = models.CharField(max_length=32, default="", null=True)
    use_mobile = models.CharField(max_length=16)
    address = models.CharField(max_length=32, default="", null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


class BusinessGame(models.Model):
    business = models.ForeignKey(Business, related_name='businessdata')
    game = models.ForeignKey(Game, related_name='businessdata')


class BusinessForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', max_length=32)
    email = forms.CharField(label='邮箱', max_length=100)
    permission = forms.CharField(label='权限', max_length=32)
    id_card = forms.CharField(label='身份证', max_length=64, required=False)
    address = forms.CharField(label='地址', max_length=255, required=False)
    mobile = forms.CharField(label='商户手机号', max_length=32)
    # use_name = forms.CharField(label='使用人姓名', max_length=32)
    # use_mobile = forms.CharField(label='使用人手机号', max_length=32)


class BusinessModifyForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    email = forms.CharField(label='邮箱', max_length=100)
    id_card = forms.CharField(label='身份证', max_length=64)
    address = forms.CharField(label='地址', max_length=255)
