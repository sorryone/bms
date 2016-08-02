# -*- coding: utf-8 -*-
import re
__author__ = 'maxijie'


def check_user_name(s):
    p3 = re.compile("^0\d{2,3}[\d\+]{7,13}$|^1[34578][\d\+]"
                    "{9,12}$|^147\d{8}|[^\._-][\w\.+-]"
                    "+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+")
    email_or_mobile = p3.match(s)
    if email_or_mobile:
        return True
    else:
        return False


def check_mobile(s):
    p3 = re.compile("^[1][358][0-9]{9}$")
    mobile = p3.match(s)
    if mobile:
        return True
    else:
        return False


def check_password(s):
    p3 = re.compile("(?!^\\d+$)(?!^[a-zA-Z]+$)(?!^[_#@]+$).{8,}")
    password = p3.match(s)
    if password:
        return True
    else:
        return False
