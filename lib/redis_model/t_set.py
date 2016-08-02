# -*- coding: utf-8 -*-
import redis
from base_model import RedisBase, RedisError

class _SetModel(RedisBase):
    """
    A redis-set model class.
    """
    data_type = "set"

    def __init__(self, pkey, *args, **kwargv):
        super(_SetModel, self).__init__(pkey, *args, **kwargv)

    def members(self):
        """
        获取完整的set对象
        @return:
            set
        """
        return self.get_client().smembers(self.storage_key) or set()

    def members_list(self):
        """
        返回全部成员的列表
        @return:
            list
        """
        return list(self.get_client().smembers(self.storage_key))

    def add(self, *members):
        """
        向set对象添加新的成员
        @args:
            *member - 要添加的成员
        @return:
            int  - 实际添加的成员数量
        """
        return self.get_client().sadd(self.storage_key, *members)

    def length(self):
        """
        返回指定key的set对象长度
        @return:
            int
        """
        return self.get_client().scard(self.storage_key)

    def has_member(self, member):
        """
        当前集合中是否包含 member
        @args:
            member
        @return:
            bool
        """
        return self.get_client().sismember(self.storage_key, member)

    def remove(self, member):
        """
        从当前set中删除指定的成员。
        @args:
            member
        @return:
            bool - 成功或失败
        """
        return self.get_client().srem(self.storage_key, member)

    def random_member(self):
        """
        从当前set中随机返回一个成员
        @args:
        @return:
        """
        return self.get_client().srandmember(self.storage_key)

    def random_members(self, amount):
        """
        从当前集合中随机返回N个成员，如果指定的数量大于整个集合的长度，则返回所有的成员
        @args:
            amount - 要获取的成员数量
        @return:
            set - 成员集合
        """
        if amount >= self.length():
            return self.members()       # 乱序？
        _member_set = set()
        while len(_member_set) < amount:
            _member_set.add(self.random_member())
        return _member_set

    def move(self, member, target_pkey):
        """
        将成员member从当前对象set移动到指定pkey的set中。
        @args:
            member -
            target_pkey - 目标set的pkey
        @return:
            bool - 成功或失败
        """
        target_storage_key = self.__class__.get_storage_key(target_pkey)
        return self.get_client().smove(self.storage_key, target_storage_key, member)

    def pop_random_member(self):
        """
        从当前set中随机删除一个成员，并返回该成员。
        @args:
        @return:
        """
        return self.get_client().spop(self.storage_key)

    # TODO: 用时需改造
    #def inter(self, rset_obj, *args):
    #    """
    #    返回当前set对象和指定的若干set对象的交集
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        set
    #    """
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sinter(self.storage_key, rset_obj.storage_key, *tuple(skeys))

    #def interstore(self, store_pkey, rset_obj, *args):
    #    """
    #    找出当前set对象和指定的若干set对象的交集，并将差集存储到指定键下。
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        int    - 存储的差集成员数
    #    """
    #    store_storage_key = self.__class__.get_storage_key(store_pkey)
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sinterstore(store_storage_key, self.storage_key, rset_obj.storage_key, *tuple(skeys))

    #def union(self, rset_obj, *args):
    #    """
    #    返回当前set对象和指定的若干set对象的并集
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        set
    #    """
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sunion(self.storage_key, rset_obj.storage_key, *tuple(skeys))

    #def unionstore(self, store_pkey, rset_obj, *args):
    #    """
    #    找出当前set对象和指定的若干set对象的并集，并将差集存储到指定键下。
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        int    - 存储的并集成员数
    #    """
    #    store_storage_key = self.__class__.get_storage_key(store_pkey)
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sunionstore(store_storage_key, self.storage_key, rset_obj.storage_key, *tuple(skeys))

    #def diff(self, rset_obj, *args):
    #    """
    #    返回当前set对象和指定的若干set对象的差集
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        set
    #    """
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sdiff(self.storage_key, rset_obj.storage_key, *tuple(skeys))

    #def diffstore(self, store_pkey, rset_obj, *args):
    #    """
    #    找出当前set对象和指定的若干set对象的差集，并将差集存储到指定键下。
    #    @args:
    #        rset_obj - _SetModel 类型的对象
    #    @return:
    #        int    - 存储的差集成员数
    #    """
    #    store_storage_key = self.__class__.get_storage_key(store_pkey)
    #    skeys = [o.storage_key for o in args]
    #    return self.get_client().sdiffstore(store_storage_key, self.storage_key, rset_obj.storage_key, *tuple(skeys))





