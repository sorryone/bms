# -*- coding: utf-8 -*-
import datetime
from bms.utilities.Mytime import get_this_day
from django.db.models import Count
from bms.models.Space import Space
from bms.models.Machine import Machine
from bms.models.Users import Users
from bms.models.Game import Game


def get_all_machine(post_data, b_id=None):
    """
        获取所有商户的设备列表
    """
    filters = {}
    if post_data.get("name"):
        filters["space__name"] = post_data["name"]
    if post_data.get("city"):
        filters["space__city"] = post_data["city"]
    if post_data.get("mobile"):
        filters["space__business__user__mobile"] = post_data["mobile"]
    if post_data.get("game_name"):
        filters["game__name"] = \
            post_data["game_name"]

    if b_id:
        machine_objs = Machine.objects.filter(
            space__business_id=b_id, **filters)
    else:
        machine_objs = Machine.objects.filter(**filters)
    return _get_machine(machine_objs)


def get_machine(b_id, post_data):
    """
        获取某一个商户的设备列表
    """
    filters = {}
    if post_data.get("name"):
        filters["space__name"] = post_data["name"]
    if post_data.get("city"):
        filters["space__city"] = post_data["city"]
    if post_data.get("mobile"):
        filters["space__business__user__mobile"] = post_data["mobile"]
    if post_data.get("game_name"):
        filters["game__name"] = \
             post_data["game_name"]

    print "=======in"
    machine_objs = Machine.objects.filter(
        space__business_id=b_id, **filters)

    return _get_machine(machine_objs)


def _get_machine(machine_objs, today=False):
    if today:
        start_time, end_time = get_this_day()
    return_list = []
    for i in machine_objs:
        if today:
            consume_num = sum(i.consume_set.filter(
                machine__id=i.id,
                amount_time__gt=start_time,
                amount_time__lt=end_time).values_list(
                    "amount", flat=True))
        else:
            consume_num = sum(i.consume_set.filter(
                machine__id=i.id).values_list("amount", flat=True))

        temp = {
            "id": i.id,
            "name": i.space.name,
            "code": i.code,
            "mac": i.mac,
            "game_name": i.game.name,
            "address": i.space.address,
            "mobile": i.space.business.user.mobile,
            "repair_time": i.repair_time,
            "consume_num": round(consume_num/100.0, 2),
        }
        return_list.append(temp)
    return return_list


def modify_machine_info(m_id, data):
    machine_params = {
        "mac": data.get("mac"),
        "order_id": data.get("order_id"),
        "device_info": data.get("device_info", {}),
        "configure_info": data.get("configure_info", {}),
        "repair_info": data.get("repair_info", {}),
        "factory_time": data.get("factory_time", None),
        "order_time": data.get("order_time", None),
        "repair_time": data.get("repair_time", None)
    }

    space_params = {
        "name": data.get("name"),
        "province": data.get("province"),
        "city": data.get("city"),
        "address": data.get("address"),
        "split_ratio": data.get("split_ratio", 0),
        "split_ratio2": data.get("split_ratio2", 0),
        "split_ratio3": data.get("split_ratio3", 0)
    }

    try:
        m_obj = Machine.objects.get(id=m_id)
    except Machine.DoesNotExist:
        return False
    else:
        m_obj.order_id = machine_params["order_id"]
        m_obj.device_info = machine_params["device_info"]
        m_obj.configure_info = machine_params["configure_info"]
        m_obj.repair_info = machine_params["repair_info"]
        if machine_params["factory_time"]:
            m_obj.factory_time = datetime.datetime.strptime(
                machine_params["factory_time"], "%Y-%m-%d")

        if machine_params["order_time"]:
            m_obj.order_time = datetime.datetime.strptime(
                machine_params["order_time"], "%Y-%m-%d")

        if machine_params["repair_time"]:
            m_obj.repair_time = datetime.datetime.strptime(
                machine_params["repair_time"], "%Y-%m-%d")

        m_obj.save()

    try:
        s_obj = Space.objects.get(id=m_obj.space_id)
    except Space.DoesNotExist:
        return False
    else:
        s_obj.province = space_params["province"]
        s_obj.name = space_params["name"]
        s_obj.city = space_params["city"]
        s_obj.address = space_params["address"]
        s_obj.save()

    return True


def get_machine_info(m_id):
    try:
        machine_obj = Machine.objects.get(id=m_id)
    except Machine.DoesNotExist:
        return False

    temp = {
        "mobile": machine_obj.space.business.user.mobile,
        "game_name": machine_obj.game.name,
        "id": machine_obj.id,
        "order_id": machine_obj.order_id,
        "code": machine_obj.code,
        "mac": machine_obj.mac,
        "province": machine_obj.space.province,
        "city": machine_obj.space.city,
        "address": machine_obj.space.address,
        "name": machine_obj.space.name,
        "order_id": machine_obj.order_id,
        "device_info": machine_obj.device_info,
        "configure_info": machine_obj.configure_info,
        "repair_info": machine_obj.repair_info,
        "factory_time": machine_obj.factory_time,
        "order_time": machine_obj.order_time,
        "repair_time": machine_obj.repair_time
    }
    return temp


def get_game_names():
    game = Game.objects.values("name")
    game_exclude = game.exclude(name__isnull=True).exclude(name="")
    game_names = game_exclude.annotate(
        dcount=Count('name')).values_list("name", flat=True)
    return game_names


def get_users_mobiles():
    bus = Users.objects.filter(permission="business").values("mobile")
    bus_exclude = bus.exclude(mobile__isnull=True).exclude(mobile="")
    mobiles = bus_exclude.annotate(
        dcount=Count('mobile')).values_list("mobile", flat=True)

    return mobiles


def get_machine_citys():
    spc = Space.objects.values('city')
    spc_exclude = spc.exclude(city__isnull=True).exclude(city="")
    city_list = spc_exclude.annotate(
        dcount=Count('city')).values_list("city", flat=True)

    return city_list


def get_space_names():
    spc = Space.objects.values('name')
    spc_exclude = spc.exclude(name__isnull=True).exclude(name="")
    name_list = spc_exclude.annotate(
        dcount=Count('name')).values_list("name", flat=True)

    return name_list
