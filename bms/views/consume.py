# -*- coding: utf-8 -*-
from lib.djhelper.api_view import api_render
from bms.models.Users import Users
from bms.logics import consume as logics


@api_render
def consume_list(request):
    if request.method == "GET":
        try:
            p_id = request.p_id
            u = Users.objects.get(p_id=p_id)
            # page = request.GET.get("page", 0)
        except Users.DoesNotExist:
            return request, "cpts/error.html", {"msg": "No User"}

        if u.permission == "business":
            m_id = request.GET.get('m_id')
            data = logics.get_consume(p_id, m_id, request.GET)
        else:
            select_id = request.GET.get("p_id")
            m_id = request.GET.get("m_id")
            data = logics.get_all_consume(select_id, m_id, request.GET)

        if not data:
            return request, "cpts/cash.html", {}

        return request, "cpts/cash.html", {"data": data}
