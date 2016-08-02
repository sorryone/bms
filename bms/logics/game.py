# -*- coding: utf-8 -*-
from bms.models.Business import Business
from bms.models.Game import Game


def create_game(data):
    # Game Model Info
    try:
        game = Game.objects.create(**data)
    except Game.DoesNotExist:
        return False

    return game


def game_list(p_id):
    try:
        business_obj = Business.objects.get(user_id=p_id)
    except Business.DoseNotExist:
        return False

    game_objs = business_obj.game.all()
    return game_objs
