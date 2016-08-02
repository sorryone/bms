# -*- coding: utf-8 -*-
import redis
import random
import lib.redis_model

# redis 连接对象
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def flush_client(host, port=REDIS_PORT, db=REDIS_DB):
    global REDIS_HOST, REDIS_PORT, REDIS_DB
    REDIS_HOST = host
    REDIS_PORT = port
    REDIS_DB = db

STORAGE_PREFIX = 'bms'


class RedisBase(object):
    """A base class for redis-models.
    """
    @classmethod
    def get_client(cls):
        return get_redis_client()

    def __init__(self, pkey):
        """
        需要子类定义的类成员：
            data_type              - 子类操作的redis数据类型: string, list,
            set, sorted_set, hash
        """
        cls_name = self.__class__.__name__
        if cls_name in lib.redis_model.__all__:
            raise NotImplementedError
        self.storage_key = self.__class__.get_storage_key(pkey)
        self.pkey = pkey

    @classmethod
    def _storage_key_prefix(cls):
        """获取redis存储KEY的前缀
        """
        _storage_prefix = STORAGE_PREFIX
        return _storage_prefix + "|" + cls.__name__ + '|'

    @classmethod
    def get_storage_key(cls, pkey):
        """redis的KEY值
        """
        # _storage_key = _storage_prefix + "|" +
        #                cls.__module__ + "." + cls.__name__ + '|' + str(pkey)
        _storage_key = cls._storage_key_prefix() + str(pkey)
        return _storage_key

    @classmethod
    def get(cls, pkey):
        """
        Get a redis-model object.
        @args:
            key: redis key.
        @return:
            if key exist, return an object, otherwise return None.
        """
        _storage_key = cls.get_storage_key(pkey)
        if cls.get_client().type(_storage_key) != cls.data_type:
            return None

        o = cls(pkey)
        return o

    @classmethod
    def exists(cls, pkey):
        """Check whether ``pkey`` has exists.
        """
        _storage_key = cls.get_storage_key(pkey)
        return cls.get_client().exists(_storage_key)

    def expire(self, time):
        """Set an expire flag on this key for ``time`` seconds
        """
        return self.get_client().expire(self.storage_key, time)

    def delete(self):
        """Delete a redis record.
        @args:
        @return:
            if record exist, delete it then return True, otherwise return False.
        """
        return self.get_client().delete(self.storage_key)

    @classmethod
    def keys(cls, pkey_pattern="*"):
        re_keywords = ['[', ']', ]      # 特殊字符
        for kw in re_keywords:
            pkey_pattern = pkey_pattern.replace(kw, "\\%s" % kw)
        _storage_key_pattern = cls.get_storage_key(pkey_pattern)
        _keys = cls.get_client().keys(_storage_key_pattern)
        return [k[len(cls._storage_key_prefix()):] for k in _keys]

    @classmethod
    def search(cls, pkey_pattern="*", amount=None, exclude_patterns=None):
        """按pkey搜索，返回对象列表
        @args:
            pkey_pattern        - 搜索结果的pkey通配符
            amount              - 需要的结果总数
            exclude_patterns    - 需要忽略的pkey通配符列表
        """
        storage_keys = list(set(cls.keys(pkey_pattern)))
        storage_keys = filter(lambda x: x, storage_keys)
        if not storage_keys:
            return []
        if exclude_patterns:
            for pattern in exclude_patterns:
                exclude_keys = list(set(cls.keys(pattern)))
                storage_keys = filter(
                    lambda x: x not in exclude_keys, storage_keys)
        if storage_keys and isinstance(amount, int):
            storage_keys = random.sample(
                storage_keys, min(len(storage_keys), amount))
        o_list = cls.mget(storage_keys)
        return o_list

    @classmethod
    def mget(cls, pkeys):
        return [cls(pkey) for pkey in pkeys]


class RedisError(Exception):
    def __init__(self, code, value=None):
        self.code = code
        self.value = value

    def __str__(self):
        return repr(self.value)
