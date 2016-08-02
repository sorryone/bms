# -*- coding: utf-8 -*-
import json
from rest_framework import status
from django.http import HttpResponse


class AuthMiddleware(object):
    def process_request(self, request):
        IGNORE_METHOD = ("login", "pay", "wechat", "pay_callback", "game")
        CHECK_PATH = ("bms",)
        try:
            method_name = request.path.split('/')[2]
            path_name = request.path.split('/')[1]
        except Exception, e:
            print '>>> auth middleware exception:', e
            return

        if path_name not in CHECK_PATH:
            return

        if method_name in IGNORE_METHOD:
            print "INGORE_method_name=", method_name
            return

        from bms.logics.users import UserLogin
        logic = UserLogin("", "")
        bms_cookie = request.COOKIES.get("bms__cookie")
        if bms_cookie:
            user_data = logic._decode_hash(bms_cookie)
            p_id = user_data.get("pid")
            request.p_id = p_id
        else:
            result_data = {
                "msg": "http 401",
            }
            return HttpResponse(json.dumps(result_data),
                                status=status.HTTP_401_UNAUTHORIZED,
                                content_type='application/json')
