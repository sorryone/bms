# -*- coding: utf-8 -*-
from django.db import models
from django import forms

__author__ = 'maxijie'


class Users(models.Model):
    p_id = models.CharField(max_length=32, default="", unique=True)
    username = models.CharField(max_length=255, default="")
    show_pwd = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=128)
    salt = models.CharField(max_length=16)
    email = models.CharField(max_length=255, default="")
    mobile = models.CharField(max_length=16, default="")
    id_card = models.CharField(max_length=32, null=True)
    permission = models.CharField(max_length=32, default="business")
    avatar_file = models.CharField(max_length=128)
    sex = models.IntegerField(null=True, default=None)
    birthday = models.IntegerField(null=True, default=None)
    project_type = models.CharField(max_length=15, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


class UsersForm(forms.Form):
    mobile = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
