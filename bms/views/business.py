# -*- coding: utf-8 -*-
from lib.djhelper.api_view import api_render
from bms.logics import business as logics
from bms.models.Users import Users
from bms.models.Business import BusinessForm, BusinessModifyForm
from lib.djhelper.checkusername import check_mobile


@api_render
def business_list(request):
    if request.method == "GET":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "No User"}

        if u.permission == "business":
            data = logics.get_business(p_id)
        else:
            data = logics.get_all_business()

        if not data:
            return request, "cpts/business_list.html", {"msg": "No Data"}

        return request, "cpts/business_list.html", {"msg": "ok", "data": data}


@api_render
def create_business(request):
    if request.method == "POST":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
            print "post", request.POST
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "NO USERS"}
        else:
            if u.permission != "admin":
                return request, "cpts/error.html", {"msg": "请联系管理员"}

        bf = BusinessForm(request.POST)
        if bf.is_valid():
            mobile = bf.cleaned_data.get("mobile")
        else:
            return request, "cpts/error.html", {"msg": bf}

        if not check_mobile(mobile):
            return request, "cpts/error.html", {"msg": "检查手机号错误"}

        p_id = logics.create_business(bf.cleaned_data)
        if p_id:
            data = logics.get_business_info(p_id)
            return request, "cpts/business_info.html", {"data": data}

        return request, "cpts/error.html", {"msg": "创建用户/商户失败"}

    if request.method == "GET":
        try:
            p_id = request.GET.get("p_id")
        except:
            return request, "cpts/error.html", {"msg": "no p_id"}

        if not p_id:
            return request, "cpts/business_info_create.html", {}

        data = logics.get_business_info(p_id)
        if data:
            return request, "cpts/business_info.html", {"data": data}
        return request, "cpts/business_info.html", {}


@api_render
def modify_business(request):
    if request.method == "POST":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "NO USER"}
        else:
            if u.permission != "admin":
                return request, "cpts/error.html", {"msg": "请联系管理员修改"}

        bf = BusinessModifyForm(request.POST)
        if bf.is_valid():
            m_id = request.POST.get("m_id")
            rc = logics.modify_machine_info(m_id, bf.cleaned_data)
            if rc:
                return request, "cpts/error.html", {"msg": "修改失败"}

            data = logics.get_business_info(p_id)
            if data:
                return request, "cpts/business_info.html", {
                    "data": data, "msg": "修改成功"}

            else:
                return request, "cpts/business_info.html", {"msg": "修改失败"}

        return request, "cpts/error.html", {"msg": bf}
