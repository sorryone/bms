# -*- coding: utf-8 -*-
import time
from lib.redis_model import HashModel
from lib.redis_model import ListModel
from rest_framework.decorators import api_view as rest_api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


class MessageCache(HashModel):
    pass


class MessageQueue(ListModel):
    pass

IGNORE_METHOD = ()


def api_render(func):
    def decorator(*args, **kwargs):
        request, template, attr = func(*args, **kwargs)
        if not template:
            template = request.path
        p_id = getattr(request, "p_id", None)
        if p_id:
            attr["p_id"] = p_id
        return render(request, template, attr)
    return decorator


def api_result(func):
    def decorator(*args, **kwargs):
        rc, data = func(*args, **kwargs)
        if rc > 0:
            code = status.HTTP_400_BAD_REQUEST
            msg = data
        else:
            code = status.HTTP_200_OK
            msg = ""
        result = {"data": data, "rc": rc, "msg": msg, "servertime": time.time()}
        response = Response(data=result, status=code)
        return response
    return decorator


def api_view(http_method_names=None):
    def decorator(func):
        def handler(*args, **kwargs):
            rest_api = rest_api_view(http_method_names)
            rest_method = rest_api(func)
            response = rest_method(*args, **kwargs)
            if response.status_code != 200:
                return response

            request = args[0]
            path_name = request.path.split('/')[1]
            method_name = request.path.split('/')[2]
            if method_name in IGNORE_METHOD:
                return response

            if path_name == "xxx":
                pass
                # do something

            return response
        return handler
    return decorator
