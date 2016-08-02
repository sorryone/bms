# -*- coding: utf-8 -*-
import uuid
import hashlib
import urllib2
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.hashers import make_password as django_make_password
from bms.models.Users import Users
from django.db import IntegrityError
from lib.djhelper.encrypt import AuthCode
from django.conf import settings


class UserLogin(object):
    def __init__(self, mobile, password, user_info={}):
        self.mobile = mobile
        self.password = password
        self.user_info = user_info

    def login(self):
        try:
            user = Users.objects.get(mobile=self.mobile)
        except Users.DoesNotExist:
            return False

        if django_check_password(self.password, user.password):
            return user
        else:
            return False

    def register(self):
        p_id = uuid.uuid1().get_hex()[0:20]
        username = "商户%s" % int(p_id[4:8], 16)
        project_type = self.user_info.get("project_type", "matchine")
        username = self.user_info.get("username", username)
        email = self.user_info.get("email", "")
        sex = self.user_info.get("sex", None)
        birthday = self.user_info.get("birthday", None)
        permission = self.user_info.get("permission", "business")
        id_card = self.user_info.get("id_card", None)
        if not self.password:
            self.password = self.mobile + "cat"

        show_pwd = self.password
        md5 = hashlib.md5()
        md5.update(self.password)
        salt = md5.hexdigest()
        password = django_make_password(self.password, salt)
        try:
            user = Users.objects.create(p_id=p_id, username=username,
                                        password=password,
                                        email=email, mobile=self.mobile,
                                        project_type=project_type,
                                        sex=sex, birthday=birthday,
                                        permission=permission,
                                        show_pwd=show_pwd, id_card=id_card)
        except IntegrityError as e:
            print e.message
            return False

        return user

    def modify_userinfo(self, p_id, data):
        try:
            user = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return False

        user.username = data.get("username")
        user.email = data.get("email")
        user.id_card = data.get("id_card")
        permission = data.get("permission")
        if permission:
            if user.permission != permission and permission != "admin":
                return False
            user.permission = permission

        password = data.get("password")
        if password:
            self._change_password(user)

        address = data.get("address")
        if address:
            user.business.address = address
            user.business.save()

        user.save()

    def set_user_permission(self, p_id, permission="business"):
        try:
            user = Users.Objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return False

        user.permission = permission
        user.save()

    def change_password(self, p_id, old_password):
        try:
            user = Users.objects.get(p_id=p_id)
        except Users.DoesNotExist:
            return False

        if not django_check_password(old_password, user.password):
            return False

        return self._change_password(user)

    def _change_password(self, user):
        md5 = hashlib.md5()
        md5.update(self.password)
        salt = md5.hexdigest()
        password = django_make_password(self.password, salt)

        user.password = password
        user.save()

        return user

    def encode_cookie(self, user):
        cookie_str = "pid^]+"+str(user.p_id)+"!;-"
        cookie_str = cookie_str+"mobile^]+"+str(user.mobile)+"!;-"
        cookie_str = cookie_str+"password^]+"+str(user.password)+"!;-"
        encoded_string = AuthCode.encode(cookie_str, settings.COOKIE_KEY)
        return encoded_string

    def _decode_hash(self, hash_str):
        hash_str = urllib2.unquote(hash_str)
        try:
            new_hash_str = AuthCode.decode(hash_str, settings.COOKIE_KEY)
        except:
            return False

        arr = new_hash_str.split("!;-")
        user_data = dict()
        for one in arr:
            result = one.split("^]+")
            if result[0]:
                user_data[result[0]] = result[1]

        return user_data

    def decode_hash(self, hash_str):
        user_data = self._decode_hash(hash_str)
        mobile = user_data.get('mobile')
        password = user_data.get("password")
        try:
            user = Users.objects.get(mobile=mobile)
        except Users.DoesNotExist:
            return False

        return password == user.password
