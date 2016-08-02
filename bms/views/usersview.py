# -*- coding: utf-8 -*-
from lib.djhelper.api_view import api_render
from lib.djhelper.checkusername import check_mobile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from bms.models.Users import Users
from bms.logics.users import UserLogin
from bms.models.Users import UsersForm
from bms.logics import business as logics


@api_render
def index(request):
    if request.method == "GET":
        bms_cookie = request.COOKIES.get("bms__cookie")
        logic = UserLogin("", "")
        if bms_cookie and logic.decode_hash(bms_cookie):
            try:
                p_id = request.p_id
                u = Users.objects.get(p_id=p_id)
            except Users.DoesNotExist:
                return request, "cpts/error.html", {"msg": "No User"}

            data = {}
            if u.permission == "business":
                data_list = logics.get_all_consume_by_game(p_id)
                data = logics.get_all_consume_by_business(p_id, data_list)
            else:
                data_list = logics.get_all_consume_by_game()

            return request, "cpts/index.html", {
                "data": data, "data_list": data_list}

    return request, "cpts/login.html", {}


def login(request):
    if request.method == 'POST':
        uf = UsersForm(request.POST)
        if uf.is_valid():
            mobile = uf.cleaned_data.get("mobile")
            password = uf.cleaned_data.get("password")
            print "mobile====", mobile
            print "password====", password
        else:
            return render(request, "cpts/login.html",
                          {"msg": "Error: Mobile Or Password Error"})

        if not check_mobile(mobile):
            return render(request, "cpts/login.html",
                          {"msg": "Mobile Error"})

        logic = UserLogin(mobile, password)
        user = logic.login()
        if user:
            response = HttpResponseRedirect('/bms/index/')
            s = logic.encode_cookie(user)
            response.set_cookie("bms__cookie", s)
            return response

        return render(request, "cpts/login.html",
                      {"msg": "Error: Mobile Or Password Error"})
    else:
        return render(request, "cpts/login.html", {})


def logout(request):
    response = HttpResponseRedirect('/bms/login/')
    response.delete_cookie("bms__cookie")
    return response
