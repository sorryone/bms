# -*- coding: utf-8 -*-
from lib.djhelper.api_view import api_render
from bms.logics import business as business_logics
from bms.logics import machine as machine_logics
from bms.models.Users import Users
from bms.models.Machine import MachineForm


@api_render
def machine_list(request):
    if request.method == "POST":
        post_data = request.POST
        print post_data
    else:
        post_data = {}

    try:
        p_id = request.p_id
        u = Users.objects.get(p_id=p_id)
    except:
        return request, "cpts/error.html", {"msg": "No User"}

    if u.permission == "business":
        data = machine_logics.get_machine(u.business.id, post_data)
        mobiles = [u.mobile]
    else:
        b_id = request.GET.get("b_id")
        data = machine_logics.get_all_machine(post_data, b_id)
        mobiles = machine_logics.get_users_mobiles()

    names = machine_logics.get_space_names()
    citys = machine_logics.get_machine_citys()
    game_names = machine_logics.get_game_names()

    if data:
        return request, "cpts/device_list.html", {
            "msg": "ok", "data": data, "citys": citys, "names": names,
            "mobiles": mobiles, "game_names": game_names}

    return request, "cpts/device_list.html", {
        "msg": "ok", "citys": citys, "names": names,
        "mobiles": mobiles, "game_names": game_names}


@api_render
def create_machine(request):
    if request.method == "POST":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
            print request.POST
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "NO USERS"}
        else:
            if u.permission != "admin":
                return request, "cpts/error.html", {"msg": "请联系管理员"}

        mf = MachineForm(request.POST)
        if not mf.is_valid():
            return request, "cpts/error.html", {"msg": "录入数据错误"}

        try:
            mobile = request.POST.get("mobile")
            user = Users.objects.get(mobile=mobile)
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "商户不存在 %s" % mobile}

        game_names = machine_logics.get_game_names()
        m_id = business_logics.create_machine(mf.cleaned_data, user)
        if m_id:
            data = machine_logics.get_machine_info(m_id)
            return request, "cpts/device_info.html", {
                     "data": data, "game_names": game_names}
        return request, "cpts/error.html", {}

    if request.method == "GET":
        try:
            m_id = request.GET.get("m_id")
        except:
            return request, "cpts/error.html", {"msg": "设备id为空"}
        else:
            try:
                p_id = request.p_id
                u = Users.objects.get(p_id=p_id)
            except Users.DoesNotExist:
                return request, "cpts/error.html", {"msg": "NO USERS"}
            else:
                if u.permission != "admin":
                    return request, "cpts/error.html", {"msg": "请联系管理员"}
            game_names = machine_logics.get_game_names()
            if not m_id:
                mobiles = machine_logics.get_users_mobiles()
                return request, "cpts/device_info_create.html", {
                                "mobiles": mobiles, "game_names": game_names}

        data = machine_logics.get_machine_info(m_id)
        if data:
            return request, "cpts/device_info.html", {
                "data": data, "game_names": game_names}
        return request, "cpts/error.html", {"msg": "No Data"}


@api_render
def modify_machine(request):
    if request.method == "POST":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "No USER"}
        else:
            if u.permission != "admin":
                return request, "cpts/error.html", {"msg": "请联系管理员"}

        mf = MachineForm(request.POST)
        if mf.is_valid():
            m_id = request.POST.get("m_id")
            rc = machine_logics.modify_machine_info(m_id, mf.cleaned_data)
            if not rc:
                request, "cpts/error.html", {"msg": "修改失败"}
            data = machine_logics.get_machine_info(m_id)
            game_names = machine_logics.get_game_names()
            if data:
                mobiles = machine_logics.get_users_mobiles()
                return request, "cpts/device_info.html", {
                    "data": data, "mobile": mobiles, "game_names": game_names}
            return request, "cpts/error.html", {"msg": "No Data"}
