# -*- coding: utf-8 -*-
from django.db import models
from bms.models.Machine import Machine
from bms.models.Business import Business
from bms.models.Players import Players
from bms.models.Space import Space
from bms.models.Game import Game

__author__ = 'maxijie'


class Consume(models.Model):
    # wechat trade_type
    trade_type = models.CharField(max_length=32, null=True)
    # wechat bank_type
    bank_type = models.CharField(max_length=32, null=True)
    # wechat fee_type
    fee_type = models.CharField(max_length=32, null=True)
    # 微信支付订单号 transaction_id
    transaction_id = models.CharField(max_length=128, null=True)
    # 商户订单号
    out_trade_no = models.CharField(max_length=128, null=True)
    game = models.ForeignKey(Game)
    machine = models.ForeignKey(Machine)
    business = models.ForeignKey(Business)
    space = models.ForeignKey(Space)
    player = models.ForeignKey(Players)
    # wechat total_fee
    amount = models.IntegerField(default=None)
    # time_end 支付完成时间
    amount_time = models.DateTimeField(auto_now=True)
