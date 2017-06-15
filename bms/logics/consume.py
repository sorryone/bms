# -*- coding: utf-8 -*-
import json
import uuid
import datetime
from django.conf import settings
from bms.models.Players import Players
from bms.models.Machine import Machine
from bms.models.Consume import Consume
from lib.redis_model import HashModel, SortedSetModel, ListModel
from bms.models.History import History
from bms.models.CheckPoint import CheckPoint
from bms.models.Game import Game


class OneRankSorted(SortedSetModel):
    pass


class RankSorted(SortedSetModel):
    pass


class ConsumeMac(HashModel):
    pass


class ConsumeList(ListModel):
    pass


class CouponList(ListModel):
    pass


def test():
    print "this is test"


def createCoupon(num, game_type):
    return_list = []
    cl = CouponList("CouponList_game_%s" % game_type)
    for i in range(num):
        a = uuid.uuid1().get_hex()
        x = uuid.UUID(a)
        s = str(x.int)[4: 20]
        cl.lpush(s)
        return_list.append(s)

    return return_list


def checkCoupon(s, game_type):
    cl = CouponList("CouponList_game_%s" % game_type)
    res = cl.remove(s)
    if res:
        return True
    else:
        return False


def remove_order_list():
    game_types = Game.objects.all().values_list("id", flat=True)
    machine_ids = Machine.objects.all().values_list("id", flat=True)
    for game_id in game_types:
        for m_id in machine_ids:
            r_name = "Mac_%s_%s" % (m_id, game_id)
            cm = ConsumeList(r_name)
            cm.delete()


def get_qrcode(game_type, macs):
    try:
        m = Machine.objects.get(mac__in=macs, game__id=game_type)
    except Machine.DoesNotExist:
        return False

    return {"base_code": settings.DINGDANGMAO_QRCODE,
            "code": m.code, "mac": m.mac}


def get_rank_top(game_type, pid):
    rank_name = "game_%s_rank" % game_type
    rs = RankSorted(rank_name)
    top_list = rs.range(0, 9, 1, 1)
    rank_num = rs.rev_rank(pid)
    if rank_num is not None:
        rank_num += 1
    else:
        rs.add(pid, 0)
        rank_num = rs.rev_rank(pid)
        rank_num += 1

    p_ids = []
    for i in top_list:
        if i[0] not in p_ids:
            p_ids.append(int(i[0]))

    p_ids.append(pid)
    p_objs = Players.objects.filter(id__in=p_ids)
    return_data = {
        "top_list": []
    }
    for index, i in enumerate(top_list):
        for p in p_objs:
            if int(i[0]) == p.id:
                return_data['top_list'].append({
                    "name": p.name,
                    "score": i[1],
                    "rank": index + 1
                })

    for p in p_objs:
        if pid == p.id:
            player_data = {}
            player_data["rank"] = rank_num
            player_data['name'] = p.name
            player_data['score'] = rs.score(pid) or 0
            return_data["player_data"] = player_data
            break

    return return_data


def get_one_rank(game_type):
    one_rank_name = "one_game_%s_rank" % game_type
    ors = OneRankSorted(one_rank_name)
    players_list = ors.range(0, 9, 1, 1)
    return_data = []
    for i in players_list:
        p = Players.objects.get(id=i[0])
        return_data.append({
            "pid": p.id,
            "name": p.name,
            "score": i[1],
            "avatar_file": p.avatar_file
        })

    return return_data


def start_game(order_id, machine_id, game_type):
    mac_name = "Mac_%s_%s" % (machine_id, game_type)
    cl = ConsumeList(mac_name)
    game_list = cl.range(0, -1)
    game_data = None
    for i in game_list:
        d = json.loads(i)
        if d.get("order_id", 0) == order_id:
            game_data = d
            break

    if not game_data:
        return False

    try:
        h, is_create = History.objects.get_or_create(order_id=order_id)
    except History.DoesNotExist:
        return False

    else:
        if h.state == "end":
            return False
        if is_create:
            h.state = "start"
            h.pid = game_data["pid"]
            h.mac_type = mac_name
            h.save()

    return True


def end_game(order_id, machine_id, game_type, score, is_finish, stage_id):
    mac_name = "Mac_%s_%s" % (machine_id, game_type)
    try:
        h = History.objects.get(order_id=order_id, mac_type=mac_name)
    except History.DoesNotExist:
        return False

    h.state = "end"
    h.save()

    try:
        p = Players.objects.get(id=h.pid)
    except Players.DoesNotExist:
        return False

    try:
        cp = p.checkpoint_set.get(stage_id=stage_id)
        is_create = False
    except CheckPoint.DoesNotExist:
        is_create = True
        cp = p.checkpoint_set.create(
            stage_id=stage_id, players=p,
            score=score, is_finish=is_finish)

    if is_create:
        add_score = score
    else:
        if score > cp.score:
            add_score = score - cp.score
            cp.score += add_score
        else:
            add_score = 0

        cp.is_finish = is_finish
        cp.save()

    one_rank_name = "one_game_%s_rank" % game_type
    ors = OneRankSorted(one_rank_name)
    ors.add_score_record(h.pid, score)

    rank_name = "game_%s_rank" % game_type
    rs = RankSorted(rank_name)
    rank_num = rs.rev_rank(h.pid)

    if rank_num is None:
        rs.add(p.id, score)
    else:
        rs.incrby(p.id, add_score)

    p.playerdata.score = sum(
        p.checkpoint_set.all().values_list("score", flat=True))
    p.playerdata.save()

    return True


def write_consume_to_redis(machine_obj, player_obj, cons_obj):
    if int(machine_obj.game.id) == 1:
        checkpoint = player_obj.checkpoint_set.filter(stage_id__lt=2*100000)
    else:
        checkpoint = player_obj.checkpoint_set.filter(stage_id__gt=2*100000)
    # checkpoint = player_obj.checkpoint_set.all()
    cp = {}
    for i in checkpoint:
        cp[i.stage_id] = {
            "score": i.score,
            "is_finish": i.is_finish,
        }
    temp = {
        "order_id": cons_obj.id,
        "machine_id": machine_obj.id,
        "name": player_obj.name,
        "avatar_file": player_obj.avatar_file,
        "pid": player_obj.id,
        "wechat": player_obj.wechat,
        "score": player_obj.playerdata.score,
        "checkpoint": cp
    }

    mac_name = "Mac_%s_%s" % (machine_obj.id, machine_obj.game.id)
    cl = ConsumeList(mac_name)
    # cl.set_value(cons_obj.id, json.dumps(temp))
    cl.rpush(json.dumps(temp))


def add_game_to_redis(machine_id, player_name):
    """
        TEST GAME
    """
    try:
        player_obj = Players.objects.get(name=player_name)
    except Players.DoesNotExist:
        return False

    try:
        machine_obj = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return False

    try:
        cons_obj = Consume.objects.all()[0]
    except Consume.DoesNotExist:
        return False

    write_consume_to_redis(machine_obj, player_obj, cons_obj)
    return True


def get_consume_to_redis(mac, game_type):
    try:
        m = Machine.objects.get(mac=mac, game__id=game_type)
    except Machine.DoesNotExist:
        return False

    mac_name = "Mac_%s_%s" % (m.id, m.game.id)
    cl = ConsumeList(mac_name)
    # ls = cl.get_all()
    ls = cl.range(0, -1)
    return_list = []
    for index, i in enumerate(ls):
        return_list.append(json.loads(i))

    return return_list


def create_consume(wechat_data):
    try:
        machine_obj = Machine.objects.get(id=wechat_data.get("attach"))
    except Machine.DoesNotExist:
        print "no machine_obj"
        return False

    try:
        player_obj = Players.objects.get(wechat=wechat_data.get("openid"))
    except Players.DoesNotExist:
        print "no players"
        return False

    end_time = wechat_data.get("time_end")
    amount_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M%S")
    data = {
        "trade_type": wechat_data.get("trade_type"),
        "bank_type": wechat_data.get("bank_type"),
        "fee_type": wechat_data.get("fee_type"),
        "transaction_id": wechat_data.get("transaction_id"),
        "out_trade_no": wechat_data.get("out_trade_no"),
        "game_id": machine_obj.game_id,
        "machine_id": machine_obj.id,
        "business_id": machine_obj.space.business_id,
        "space_id": machine_obj.space_id,
        "player_id": player_obj.id,
        "amount": wechat_data.get("total_fee"),
        "amount_time": amount_time
    }
    try:
        c = Consume.objects.filter(
            out_trade_no=data["out_trade_no"],
            transaction_id=data["transaction_id"]).exists()
    except Consume.DoesNotExist:
        return False
    else:
        if c:
            return True

    try:
        cons_obj = Consume.objects.create(**data)
    except Consume.DoesNotExist:
        return False

    write_consume_to_redis(machine_obj, player_obj, cons_obj)

    return True


def get_all_consume(p_id=None, m_id=None, data={}, page=0):
    filters = _set_filters(data)
    # page_length = 10
    # cur_index = page_length*(page)
    if p_id:
        cons_objs = Consume.objects.filter(
            business__user__p_id=p_id, **filters).order_by("-amount_time")
    elif m_id:
        cons_objs = Consume.objects.filter(
            machine_id=m_id, **filters).order_by("-amount_time")
    else:
        cons_objs = Consume.objects.filter(**filters).order_by("-amount_time")

    # max_count = cons_objs.count()
    # cons_objs = cons_objs[cur_index: cur_index + page_length]
    result_list = []
    for i in cons_objs:
        result_list.append(get_consume_info(i))

    return result_list


def get_consume(p_id, m_id=None, data={}, page=0):
    filters = _set_filters(data)
    # page_length = 10
    # cur_index = page_length*(page)
    if m_id:
        cons_objs = Consume.objects.filter(
            machine_id=m_id, **filters).order_by("-amount_time")
    else:
        cons_objs = Consume.objects.filter(
            business__user__p_id=p_id, **filters).order_by("-amount_time")

    # max_count = cons_objs.count()
    # cons_objs = cons_objs[cur_index: cur_index + page_length]

    result_list = []
    for i in cons_objs:
        result_list.append(get_consume_info(i))

    return result_list


def _set_filters(filters):
    result_f = {}
    start = datetime.datetime.now().date()
    end = start + datetime.timedelta(days=1)
    if "amount_time_start" in filters:
        result_f["amount_time__gt"] = filters['amount_time_start']
    else:
        result_f["amount_time__gt"] = start.strftime("%Y-%m-%d")

    if "amount_time_end" in filters:
        result_f["amount_time__lt"] = filters["amount_time_end"]
    else:
        result_f["amount_time__lt"] = end.strftime("%Y-%m-%d")

    if "game_name" in filters:
        result_f["game__name"] = filters["game_name"]

    return result_f


def get_consume_info(con_obj):
    result = {
        "amount_time": con_obj.amount_time,
        "id": con_obj.id,
        # "order_id": con_obj.order_id,
        "mobile": con_obj.business.buyer_mobile,
        "address": con_obj.space.address,
        "player_id": con_obj.player_id,
        "game_name": con_obj.game.name,
        "amount": round(con_obj.amount/100.0, 2),
        "mac": con_obj.machine.mac,
        "bank_type": con_obj.bank_type,
        "fee_type": con_obj.fee_type,
        "transaction_id": con_obj.transaction_id,
        "out_trade_no": con_obj.out_trade_no
    }

    return result
