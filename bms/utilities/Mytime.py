# -*- coding: utf-8 -*-
import datetime


def get_today():
    return datetime.datetime.now().date()


def get_this_day():
    start = datetime.datetime.now().date()
    end = start + datetime.timedelta(days=1)
    return start, end
