# -*- coding: utf-8 -*-
import qrcode
from django.conf import settings
from bms.utilities.Mytime import get_this_day
from django.db import IntegrityError
from bms.models.Machine import Machine
from bms.models.Business import Business, BusinessGame
from bms.models.Space import Space
from bms.models.Consume import Consume
from bms.logics.users import UserLogin
from bms.models.Users import Users
from bms.models.Game import Game
from lib.platform.wechat_api import wechat


def get_all_consume_by_game(p_id=None):
    """
        获取所有消费信息
    """
    game_objs = Game.objects.all()
    return_list = []
    start_time, end_time = get_this_day()
    for g_obj in game_objs:
        if p_id:
            consume_objs = Consume.objects.filter(business__user__p_id=p_id)
        else:
            consume_objs = Consume.objects.all()

        consume_num = sum(consume_objs.filter(game_id=g_obj.id).values_list(
            "amount", flat=True))

        today_consume_num = sum(consume_objs.filter(
            game_id=g_obj.id,
            amount_time__gt=start_time,
            amount_time__lt=end_time).values_list("amount", flat=True))

        temp = {
            "name": g_obj.name,
            "consume_num": round(consume_num/100.0, 2),
            "today_consume_num": round(today_consume_num/100.0, 2)
        }
        return_list.append(temp)

    return return_list


def get_all_consume_by_business(p_id, data_list):
    business_obj = Business.objects.get(user__p_id=p_id)
    space_ids = business_obj.space_set.values_list("id", flat=True)
    machine_num = Machine.objects.filter(space_id__in=space_ids).count()
    total_today_num = 0
    total_num = 0
    for d in data_list:
        total_today_num += d["today_consume_num"]
        total_num += d["consume_num"]

    return_data = {
        "p_id": p_id,
        "mobile": business_obj.user.mobile,
        "password": business_obj.user.show_pwd,
        "machine_num": machine_num,
        "total_today_num": total_today_num,
        "total_num": total_num,
        "address": business_obj.address
    }
    return return_data


def get_all_business(game_id=None):
    """
        获取商户信息列表
    """
    if game_id:
        # 获取指定游戏所有数据
        b_ids = BusinessGame.objects.filter(
            game_id=game_id,
            business__user__permission="business").values_list(
                "business_id", flat=True)

        business_objs = Business.objects.filter(id__in=b_ids)

    else:
        # 获取全部游戏数据
        business_objs = Business.objects.filter(
            user__permission="business")

    return_list = []
    start_time, end_time = get_this_day()

    for b in business_objs:
        temp = _get_info(b, start_time, end_time, game_id)
        return_list.append(temp)

    return return_list


def get_business(p_id, game_id=None):
    """
        获取单个商户信息
    """
    if game_id:
        try:
            bg = BusinessGame.objects.get(
                        business__user_id=p_id, game_id=game_id,
                        business__user__permission="business")
        except BusinessGame.DoesNotExsit:
            return False
        else:
            business_obj = bg.bussiness
    else:
        business_obj = Business.objects.get(
            user__permission="business", user_id=p_id)

    start_time, end_time = get_this_day()
    return [_get_info(business_obj, start_time, end_time, game_id)]


def _get_info(business, start_time, end_time, game_id=None):
    space_ids = business.space_set.values_list("id", flat=True)
    if game_id:
        game_ids = [game_id]
    else:
        ids = Consume.objects.filter(
            business_id=business.id).values_list("game_id", flat=True)
        game_ids = list(set(ids))
        # game_ids = business.businessdata.values_list('game_id', flat=True)

    machine_num = Machine.objects.filter(space_id__in=space_ids).count()
    consume_num = sum(Consume.objects.filter(
        business_id=business.id, amount_time__gt=start_time,
        game_id__in=game_ids, amount_time__lt=end_time).values_list(
            "amount", flat=True))

    temp = {
        "p_id": business.user_id,
        "b_id": business.id,
        "permission": business.user.permission,
        "mobile": business.user.mobile,
        "password": business.user.show_pwd,
        "address": business.address,
        "machine_num": machine_num,
        "consume_num": round(consume_num/100.0, 2),
        "game_id": game_id
    }

    return temp


def create_business(data):
    """
        注册账户 添加商户信息
    """
    # Users Model Info
    user_params = {
        "username": data.get("username", ""),
        "email": data.get("email", ""),
        "permission": data.get("permission", "business"),
        "id_card": data.get("id_card", ""),
    }

    mobile = data.get("mobile")
    password = data.get("password")
    logic = UserLogin(mobile, password, user_params)
    user = logic.register()
    if not user:
        return False

    if user.permission == "admin":
        return user.p_id

    # Business Model Info
    business_params = {
        "user_id": user.p_id,
        "buyer_name": data.get("username"),
        "buyer_mobile": data.get("mobile"),
        "use_name": data.get("use_name"),
        "use_mobile": data.get("mobile"),
        "address": data.get("address", "")
    }
    try:
        Business.objects.create(**business_params)
    except Business.DoesNotExist:
        return False

    return user.p_id


def get_business_info(p_id):
    try:
        user = Users.objects.get(p_id=p_id)
    except Users.DoesNotExist:
        return False

    if getattr(user, "business", None):
        address = user.business.address
    else:
        address = ""
    result = {
        "p_id": user.p_id,
        "permission": user.permission,
        "username": user.username or "",
        "email": user.email or "",
        "mobile": user.mobile or "",
        "password": user.show_pwd or "",
        "id_card": user.id_card or "",
        "address": address
    }

    return result


def modify_business_info(p_id, data):
    logic = UserLogin("", "")
    user_res = logic.modify_userinfo(p_id, data)
    if not user_res:
        return False
    return True


def create_machine(data, user):
    """
        为商户添加设备
        todo create code
    """
    # Machine Model Info
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

    # Space Model Info
    space_params = {
        "name": data.get("name"),
        "province": data.get("province"),
        "city": data.get("city"),
        "address": data.get("address"),
        "split_ratio": data.get("split_ratio", 0),
        "split_ratio2": data.get("split_ratio2", 0),
        "split_ratio3": data.get("split_ratio3", 0)
    }

    for k, v in space_params.iteritems():
        if v is None:
            print "=====>space_params %s is None<=========" % k
            raise
    try:
        game = Game.objects.get(name=data.get("game_name"))
    except Game.DoesNotExist:
        return False

    try:
        space_params["business_id"] = user.business.id
        s_obj = Space.objects.create(**space_params)
    except Space.DoesNotExist:
        return False

    try:
        machine_params["space_id"] = s_obj.id
        machine_params["game_id"] = game.id
        machine_obj = Machine.objects.create(**machine_params)
    except (Machine.DoesNotExist, IntegrityError):
        s_obj.delete()
        return False
    else:
        url, xlm = wechat.create_QRCode(machine_obj.id)
        machine_obj.code = url
        get_url = create_qrcode(url, machine_obj.id)
        machine_obj.qrimage_url = get_url
        machine_obj.save()

    return machine_obj.id


def create_qrcode(url, m_id):
    s = qrcode.make(url)
    qrname = "qrcode%s.png" % m_id
    save_url = settings.QRCODE_ROOT + qrname
    s.save(save_url)
    get_url = settings.QRCODE_URL + qrname
    return get_url
