# -*- coding: utf-8 -*-
from base_model import RedisBase, RedisError
import cPickle as pickle

class _HashModel(RedisBase):
    """
    A redis-hash model class.
    需要子类定义 fields 变量，来指定字段类型。
    """
    data_type = "hash"

    def __init__(self, pkey, *args, **kwargv):
        super(_HashModel, self).__init__(pkey, *args, **kwargv)

    def has_key(self, key):
        """
        判断hash对象中是否包含指定的key。
        @args:
            key  - str
        @return:
            bool
        """
        return self.get_client().hexists(self.storage_key, key)

    def get_value(self, key, default = None):
        """
        从hash对象中获取指定key的值。
        @args:
            key  - str
        @return:
            str  - if given key not exists, return None
        """
        value = self.get_client().hget(self.storage_key, key)
        if value is None:
            value = default
        return value
        #_value = self.get_client().hget(self.storage_key, key)
        #return self.loads_field(key, _value)

    def get_values(self, key_list):
        """
        返回指定列表中所有key对应的值。如果key不存在，返回列表中对应的值为None。
        @args:
            key_list  - list
        @return:
            list
        """
        if not key_list:
            return []
        return self.get_client().hmget(self.storage_key, key_list)
        #_value_list = self.get_client().hmget(self.storage_key, key_list)
        #_loads_value_list = []
        #for i in range(len(key_list)):
        #    _loads_value_list.append(self.loads_field(key_list[i], _value_list[i]))
        #return _loads_value_list

    def set_value(self, key, value):
        """
        设定给定key对应的值。
        @args:
            key  - str
        @return:
            str
        """
        #_value = self.dumps_field(key, value)
        return self.get_client().hset(self.storage_key, key, value)

    def set_values(self, mapping):
        """
        按照指定的字典中所有的键值更新hash对象。
        @args:
            mapping  - dict
        @return:
            bool
        """
        #mapping = dict(mapping)
        #for k,v in mapping.items():
        #    mapping[k] = self.dumps_field(k, v)
        return self.get_client().hmset(self.storage_key, mapping)

    def pop(self, *keys):
        """
        从hash对象中删除指定key的键值。
        @args:
            keys  - list
        @return:
            bool
        """
        return self.get_client().hdel(self.storage_key, *keys)

    def get_all(self):
        """
        获取完整的hash对象
        @return:
            dict
        """
        return self.get_client().hgetall(self.storage_key)
        #data_all = self.get_client().hgetall(self.storage_key)
        #for k,v in data_all.items():
        #    data_all[k] = self.loads_field(k, v)
        #return data_all

    def incr(self, key, amount = 1):
        """
        将amount的数字加到指定key的字段值上。指定字段类型必须为整数。
        @args:
            key     - str
            amount  - int
        @return
            int     - 该字段增加数值后的值
        """
        return self.get_client().hincrby(self.storage_key, key, amount)

    def get_keys(self):
        """
        返回hash对象中所有的key。
        @return:
            list
        """
        return self.get_client().hkeys(self.storage_key)

    def values(self):
        """
        返回hash对象中全部的字段值。
        注意：返回列表中所有值均没有序列化，只适合不需要序列化的数据。
        @return:
            list
        """
        return self.get_client().hvals(self.storage_key)

    def set_new(self, key, value):
        """为hash对象增加一个字段key，并设置值为value。 如果key已经存在，执行会失败。
        @args:
            key   - str
            value - str
        @return:
            bool
        """
        #_value = self.dumps(key, value)
        return self.get_client().hsetnx(self.storage_key, key, value)

    def length(self):
        """返回hash对象的长度（字段数）。
        @return:
            int
        """
        return self.get_client().hlen(self.storage_key)








    #def dumps_field(self, key, value):
    #    """
    #    按需要序列化一个字段的数据。
    #    """
    #    if hasattr(self, "fields"):
    #        field_type = self.fields.get(key)
    #        if field_type == "strnotNone":
    #            value = None if value == "None" else value
    #        elif not field_type in ["str", "int", "float", "long"]:
    #            value = pickle.dumps(value)
    #    return value

    #def loads_field(self, key, value):
    #    """
    #    按需要反序列化一个字段的数据。
    #    """
    #    if hasattr(self, "fields"):
    #        field_type = self.fields.get(key)
    #        if field_type in ["int", "float", "long"]:
    #            value = eval("%s('%s')" % (field_type, value))
    #        elif field_type == "strnotNone":
    #            value = None if value == "None" else value
    #        elif not field_type.startswith("str"):
    #            value = pickle.loads(value)
    #    return value




