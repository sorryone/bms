# -*- coding: utf-8 -*-
"""阿里大鱼SDK
"""
__author__ = "liling"

try:
    import simplejson as json
except ImportError:
    import json
import urlparse
import top.api
from top.api.base import TopException


class Alidayu(object):

    EXTEND = "extend"
    SMS_TYPE = "sms_type"
    SMS_FREE_SIGN_NAME = "sms_free_sign_name"
    SMS_PARAMS = "sms_params"
    SMS_TEMPLATE_CODE = "sms_template_code"
    REC_NUMS = "rec_nums"

    def __init__(self, app_key, app_secret, api_url):
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_url = api_url
        self.api_host = urlparse.urlparse(api_url).hostname

        self.extend = None
        self.sms_type = "normal"
        self.sms_free_sign_name = None
        self.sms_params = self.sms_param = None
        self.sms_template_code = None
        self.rec_nums = self.rec_num = None
        self.error = None

    def setopt(self, opt_name, opt_value):
        setattr(self, opt_name, opt_value)
        if opt_name == self.REC_NUMS:
            self.rec_num = ",".join(opt_value)
        if opt_name == self.SMS_PARAMS:
            self.sms_param = json.dumps(opt_value)

    def send(self):
        req = top.api.AlibabaAliqinFcSmsNumSendRequest(self.api_host)
        req.set_app_info(top.appinfo(self.app_key,self.app_secret))
        req.extend = self.extend
        req.sms_type = self.sms_type
        req.sms_free_sign_name = self.sms_free_sign_name
        req.sms_param = self.sms_param
        req.sms_template_code = self.sms_template_code
        req.rec_num = self.rec_num
        try:
            res = req.getResponse()
        except TopException, e:
            self.error = e
            return False
        return True

