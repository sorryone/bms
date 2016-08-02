# -*- coding: utf-8 -*-
from bms.models.Players import Players, PlayerGameData
from bms.models.Machine import Machine
from lib.platform.wechat_api import wechat


def get_or_create(wechat_data):
    openid = wechat_data.get("openid")
    machine_id = wechat_data.get("product_id")
    is_subscribe = wechat_data.get("is_subscribe")
    if is_subscribe:
        if is_subscribe == "Y":
            is_subscribe = True
        else:
            is_subscribe = False

    try:
        machine_obj = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return False

    try:
        player = Players.objects.get(wechat=openid)
        if is_subscribe:
            wechat_obj = wechat.client.user.get(openid)
            player.name = wechat_obj["nickname"]
            player.avatar_file = wechat_obj["headimgurl"]
            player.city = wechat_obj["city"]
            player.province = wechat_obj["province"]
            player.country = wechat_obj["country"]
            player.sex = wechat_obj["sex"]
            player.save()

    except Players.DoesNotExist:
        if not is_subscribe:
            return False
        wechat_obj = wechat.client.user.get(openid)
        player = Players.objects.create(
            wechat=openid,
            subscribe=is_subscribe,
            avatar_file=wechat_obj["headimgurl"],
            name=wechat_obj["nickname"],
            city=wechat_obj["city"],
            province=wechat_obj["province"],
            country=wechat_obj["country"],
            sex=wechat_obj["sex"]
            )

        pgd = PlayerGameData()
        pgd.player = player
        pgd.game = machine_obj.game
        pgd.score = 0
        pgd.star = 0
        pgd.save()

    data = {
        "attach": machine_id,
        "body": machine_obj.game.body or "BellcatGame",
        "detail": machine_obj.game.detail,
        "total_fee": machine_obj.game.sale,
        "product_id": machine_id
    }

    return data