# -*- coding: utf-8 -*-
from lib.djhelper.api_view import api_view
from lib.platform.wechat_api import wechat as wechat_obj
from django.http import HttpResponse
from rest_framework.response import Response
from bms.logics import player as logics
from bms.logics import consume as consume_logics


@api_view(["GET", "POST"])
def wechat(request):
    if request.method == 'GET':
        try:
            print request.query_params
            signature = request.query_params.get("signature", "")
            timestamp = request.query_params.get("timestamp", "")
            nonce = request.query_params.get("nonce", "")
            echostr = request.query_params.get("echostr", "")
        except:
            return Response("error", status=400)

        print signature, timestamp, nonce
        rc = wechat_obj.check_wechat(signature, timestamp, nonce)
        if rc:
            return HttpResponse(echostr)

    try:
        xml = wechat_obj.check_message(request.body, request.query_params)
    except Exception, e:
        print request.body
        print e.message
    else:
        return HttpResponse(content=xml, content_type="application/xml")
    return HttpResponse("error")


# @api_view(["GET", "POST"])
def pay(request):
    if request.method == "POST":
        data = wechat_obj._xmltodict(request.body)
        result = {}
        d = logics.get_or_create(data)
        if d:
            rc = wechat_obj.create_order(d)
            if rc:
                result = {
                    "return_code": rc["return_code"],
                    "return_msg": rc["return_msg"],
                    "appid": rc["appid"],
                    "mch_id": rc["mch_id"],
                    "nonce_str": rc["nonce_str"],
                    "prepay_id": rc["prepay_id"],
                    "result_code": rc["result_code"],
                }

            if not result:
                result = {
                    "return_code": "SUCCESS",
                    "return_msg": "ok",
                    "result_code": "FAIL",
                    "err_code_des": "ServerError"
                }
        else:
            result = {
                "return_code": "SUCCESS",
                "return_msg": "ok",
                "result_code": "FAIL",
                "err_code_des": "请先关注公众号"
            }

        sign = wechat_obj._get_sign(result)
        result['sign'] = sign
        xml = wechat_obj._dicttoxml(result)
        return HttpResponse(content=xml, content_type="application/xml")
    return HttpResponse("pay")


# @api_view(["GET", "POST"])
def pay_callback(request):
    if request.method == "POST":
        data = wechat_obj._xmltodict(request.body)
        rc = consume_logics.create_consume(data)
        if rc:
            result = {
                "return_code": "SUCCESS",
                "return_msg": "OK"
            }
        else:
            result = {
                "return_code": "FAIL",
                "return_msg": "ServerError"
            }
        xml = wechat_obj._dicttoxml(result)
        return HttpResponse(content=xml, content_type="application/xml")
    return HttpResponse("pay_callback")
