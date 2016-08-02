# -*- coding: utf-8 -*-
#import cPickle as pickle
from time import time as ts
from base_model import RedisBase

class _StringModel(RedisBase):
    """
    A redis-string model class.
    """
    data_type = "string"

    def __init__(self, pkey, *args, **kwargv):
        self._value = None
        self._timeout = None
        super(_StringModel, self).__init__(pkey, *args, **kwargv)

    def delete(self):
        self._value = None
        super(_StringModel, self).delete()

    def get_value(self):
        # 如果没有缓存值，或者设置的超时时间已过，强制从redis里重新取值
        if self._value is None or (self._timeout and self._timeout <= ts()):
            self._value = self.get_client().get(self.storage_key)
        _value_type = getattr(self.__class__, "value_type", None)
        if _value_type and _value_type in ["int", "float", "long"]:
            self._value = eval("%s('%s')" % (_value_type, self._value))
        return self._value

    def set_value(self, value):
        res = self.get_client().set(self.storage_key, value)
        self._value = value
        self._timeout = None
        return res

    def setex(self, value, time):
        """Set the value to ``value`` that expires in ``time`` seconds
        """
        res = self.get_client().setex(self.storage_key, value, time)
        if res:
            self._value = value
            self._timeout = ts() + time
        return res

    def setnx(self, value):
        """Set the value to ``value`` if key doesn't exist
        """
        res = self.get_client().setnx(self.storage_key, value)
        if res:
            self._value = value
            self._timeout = None
        return res

    def increase(self, amount = 1):
        self._value = self.get_client().incr(self.storage_key, amount)
        return self._value

    def decrease(self, amount = 1):
        self._value = self.get_client().incr(self.storage_key, -amount)
        return self._value

    @classmethod
    def mget(cls, keys):
        _storage_keys = [cls.get_storage_key(k) for k in keys]
        if _storage_keys == []:
            return []
        _values = cls.get_client().mget(_storage_keys)
        o_list = []
        for i in range(0, len(_storage_keys)):
            if _values[i] is None:
                o_list.append(None)
                continue
            o = cls(keys[i])
            o._value = _values[i]
            o_list.append(o)
        return o_list





