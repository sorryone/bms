# -*- coding: utf-8 -*-
import json
from lib.djhelper.api_view import api_render, api_view, api_result
from bms.logics import game as logics
from bms.models.Users import Users
from bms.logics import consume as game_logics


@api_render
def create_game(request):
    if request.method == "POST":
        try:
            p_id = request.POST.get("p_id")
        except:
            return request, "cpts/business_info.html", {}

        try:
            u = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return request, "cpts/business_info.html", {}

        if u.permission == "business":
            data = logics.get_business_info(p_id)
        else:
            data = logics.get_all_business()

        if not data:
            return request, "cpts/business_info.html", {}

        return request, "cpts/business_info.html", {"data": data}


@api_view(["GET"])
@api_result
def test(request):
    if request.method == "GET":
        return 0, "ok"


@api_view(["GET"])
@api_result
def get_rank(request):
    if request.method == "GET":
        try:
            game_type = int(request.query_params.get("game_type"))
            pid = int(request.query_params.get('pid'))
        except:
            return 1, "参数错误"

        data = game_logics.get_rank_top(game_type, pid)
        if not data:
            return 2, "数据错误"

        return 0, data


@api_view(['GET'])
@api_result
def get_game_list(request):
    if request.method == "GET":
        try:
            mac = request.query_params.get("mac")
            game_type = int(request.query_params.get("game_type"))
        except:
            return 1, "参数错误"

        data = game_logics.get_consume_to_redis(mac, game_type)
        if data is False:
            return 2, "数据错误"
        return 0, data


@api_view(["GET"])
@api_result
def start_game(request):
    if request.method == "GET":
        try:
            pid = int(request.query_params.get("pid"))
            machine_id = int(request.query_params.get("machine_id"))
            game_type = int(request.query_params.get("game_type"))
        except:
            return 1, "参数错误"

        data = game_logics.start_game(pid, machine_id, game_type)
        if not data:
            return 2, "数据错误"
        return 0, data


@api_view(["POST"])
@api_result
def end_game(request):
    if request.method == "POST":
        try:
            params = json.loads(request.body)
            hid = int(params.get("hid"))
            pid = int(params.get("pid"))
            machine_id = int(params.get("machine_id"))
            game_type = int(params.get("game_type"))
            score = int(params.get("score"))
            stage_id = int(params.get("stage_id"))
            is_finish = int(params.get("is_finish"))
        except Exception, e:
            print e.message
            return 1, "参数错误"

        data = game_logics.end_game(
            hid, pid, machine_id, game_type, score, is_finish, stage_id)
        if not data:
            return 2, "数据错误"

        return 0, data


@api_view(["GET"])
@api_result
def get_qrcode(request):
    if request.method == "GET":
        try:
            macs = request.query_params.get("mac")
            macs = macs.split(",")
            game_type = int(request.query_params.get("game_type"))
        except:
            return 1, "参数错误"

        data = game_logics.get_qrcode(game_type, macs)
        if not data:
            return 2, "数据错误"

        return 0, data
