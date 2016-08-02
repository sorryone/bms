# -*- coding: utf-8 -*-
import redis
import hashlib
from base_model import RedisBase, RedisError

class _SortedSetModel(RedisBase):
    """
    A redis-sorted-set model class.
    """
    data_type = "zset"

    def __init__(self, pkey, *args, **kwargv):
        super(_SortedSetModel, self).__init__(pkey, *args, **kwargv)

    def add(self, member, score):
        """向set对象添加新的成员
        @args:
            member - 要添加的成员
        @return:
            BOOL  - 添加成功或失败
        """
        return self.get_client().zadd(self.storage_key, member, score)

    def add_score_record(self, member, score):
        """添加成员新的纪录，只有传入的 score 大于现存的score，才添加。
        """
        if self.get_client().zscore(self.storage_key, member) < score:
            return self.get_client().zadd(self.storage_key, member, score)
        return 0

    def range(self, start, end, desc = False, withscores = False, appose = False):
        """获取排序在start至end之间的所有成员（包含start和end位置的成员）。如果指定 withscores为True,则返回一个元祖的列表。
        @args:
            start      - int  起始序号
            end        - int  结束序号
            desc       - bool 是否倒序
            withscores - bool 是否同时返回score
            appose     - bool  是否支持并列
        @return:
            list
        """
        _lst = self.get_client().zrange(self.storage_key, start, end, desc, withscores)
        if _lst and appose:
            # 找到最后一个的分数
            if withscores:
                last_score = _lst[-1][1]
            else:
                last_score = self.get_client().zscore(self.storage_key, _lst[-1])
            # 找到相同分数的成员
            same_score_members = self.get_client().zrangebyscore(
                    self.storage_key, min = last_score, max = last_score,
                    withscores = withscores
            )
            if desc:
                same_score_members = same_score_members[::-1]
            _lst += same_score_members[same_score_members.index(_lst[-1])+1:]
        return _lst or []

    def revrange(self, start, end, withscores=False, appose = False):
        """
        整个集合按倒序排列后，返回start至end之间的所有成员（包含start和end位置的成员）。如果指定 withscores为True,则返回一个元祖的列表。
        @args:
            start      - int  起始序号
            end        - int  结束序号
            withscores - bool 是否同时返回score
            appose     - bool  是否支持并列
        @return:
            list
        """
        _lst = self.get_client().zrevrange(self.storage_key, start, end, withscores)
        if _lst and appose:
            # 找到最后一个的分数
            if withscores:
                last_score = _lst[-1][1]
            else:
                last_score = self.get_client().zscore(self.storage_key, _lst[-1])
            # 找到相同分数的成员
            same_score_members = self.get_client().zrevrangebyscore(
                    self.storage_key, min = last_score, max = last_score,
                    withscores = withscores
            )
            _lst += same_score_members[same_score_members.index(_lst[-1])+1:]
        return _lst or []

    def top(self, amount = 1, desc = False, withscores = False):
        """
        获取Top N的成员列表。
        @args:
            amount  - int 要获取的成员列表
        @return:
            list
        """
        if amount < 1:
            raise RedisError(1002)
        return self.get_client().zrange(self.storage_key, 0, amount-1, desc = desc, withscores = withscores)

    def range_by_score(self, min, max, start = None, num = None, withscores = False):
        """
        返回集合中score在指定区间的元素。如指定 start 和 num ，可以在指定区间内进行切片。
        @args:
            min             - int OR float OR double
            max             - int OR float OR double
            start           - 区间中切片开始的序号
            num             - 切片的元素个数
            withscores      - 是否一起返回score，如果为True，则返回的每个元素都是元祖
            #score_cast_func - 用来处理score的函数，默认为 float
        @return:
            list
        """
        return self.get_client().zrangebyscore(self.storage_key, min, max, start, num, withscores)

    def rev_range_by_score(self, max, min, start = None, num = None, withscores = False, score_cast_func = float):
        """
        整个集合倒序排列后，返回集合中score在指定区间的元素。如指定 start 和 num ，可以在指定区间内进行切片。
        @args:
            max             - int OR float OR double
            min             - int OR float OR double
            start           - 区间中切片开始的序号
            num             - 切片的元素个数
            withscores      - 是否一起返回score，如果为True，则返回的每个元素都是元祖
            score_cast_func - 用来处理score的函数，默认为 float
        @return:
            list
        """
        return self.get_client().zrevrangebyscore(self.storage_key, max, min, start, num, withscores, score_cast_func)

    def length(self):
        """
        返回集合的长度
        @return:
            long
        """
        return self.get_client().zcard(self.storage_key)

    def count(self, min, max):
        """
        返回指定score区间的元素个数。
        @args:
            min   - 指定的最小score
            max   - 指定的最大score
        @return:
            long
        """
        return self.get_client().zcount(self.storage_key, min, max)

    def incrby(self, member, amount = 1):
        """
        增加一个元素的score 值。
        @args:
            member  - 要增加score的成员。
            amount  - 增加的score数。
        @return:
            float   - 增加后的score值。
        """
        return self.get_client().zincrby(self.storage_key, member, amount)

    def rank(self, member, appose = False):
        """
        获取某元素在集合中的序号。
        @args:
            member  - str
            appose - bool  是否支持并列
        @return:
            int
        """
        if appose:
            score = self.get_client().zscore(self.storage_key, member)
            if score is None:
                return None
            # 找到相同分数的并列成员中的第一个
            same_score_member = self.get_client().zrangebyscore(
                    self.storage_key, min = score, max = score,
                    start = 0, num = 1
            )[0]
            return self.get_client().zrank(self.storage_key, same_score_member)
        else:
            return self.get_client().zrank(self.storage_key, member)

    def rev_rank(self, member, appose = False):
        """
        获取某元素在集合中倒序排列的序号。
        @args:
            member  - str
            appose - bool  是否支持并列
        @return:
            int
        """
        if appose:
            score = self.get_client().zscore(self.storage_key, member)
            if score is None:
                return None
            # 找到相同分数的并列成员中的第一个
            same_score_member = self.get_client().zrevrangebyscore(
                    self.storage_key, min = score, max = score,
                    start = 0, num = 1
            )[0]
            return self.get_client().zrevrank(self.storage_key, same_score_member)
        else:
            return self.get_client().zrevrank(self.storage_key, member)

    def remove(self, member):
        """
        删除一个成员。
        @args:
            members    - str
        """
        return self.get_client().zrem(self.storage_key, member)

    def score(self, member):
        """
        获取一个元素的 score .
        @args:
            member  - str
        @return:
            float
        """
        return self.get_client().zscore(self.storage_key, member)

    def remove_range_by_rank(self, min, max):
        """
        按序号删除某个区间的元素。
        @args:
            min   - int
            max   - int
        @return:
            long  - 实际删除的元素个数
        """
        return self.get_client().zremrangebyrank(self.storage_key, min, max)

    def remove_range_by_score(self, min_score, max_score):
        """
        按score删除某个区间的元素。
        @args:
            min_score  - float
            max_score  - float
        @return:
            long  - 实际删除的元素个数
        """
        return self.get_client().zremrangebyscore(self.storage_key, min_score, max_score)

    def interstore(self, pkeys, aggregate = "SUM"):
        """获取交集并存储到本对象内
        @args:
            pkeys           - 要求交集的pkey列表
            aggregate       - "SUM" or "MIN" or "MAX". 存储交集时生成score的方式。默认执行SUM操作
        @return:
            int    - 生成交集的成员个数
        """
        # 获取要取交集的实际存储key列表
        _storage_keys = [self.__class__.get_storage_key(pkey) for pkey in pkeys]
        dest_storage_key = self.storage_key
        return self.get_client().zinterstore(dest_storage_key, _storage_keys, aggregate)

    def unionstore(self, pkeys, aggregate = "SUM"):
        """获取并集并存储到本对象内
        @args:
            pkeys           - 要合并并集的pkey列表
            aggregate       - "SUM" or "MIN" or "MAX". 存储并集时生成score的方式。默认执行SUM操作
        @return:
            int    - 生成并集的成员个数
        """
        # 获取要取并集的实际存储key列表
        _storage_keys = [self.__class__.get_storage_key(pkey) for pkey in pkeys]
        dest_storage_key = self.storage_key
        return self.get_client().zunionstore(dest_storage_key, _storage_keys, aggregate)

    # TODO: 用时需改造
    #def interstore(self, rzset_obj_list, dest = None, use_cache = True, cache_seconds = 3, aggregate = "MIN", start = None, count = -1):
    #    """
    #    获取交集并存储到指定的key。
    #    @args:
    #        rzset_obj_list  - _SortedSetModel类型的变量列表
    #        dest            - str 求出交集后存储到的key，如不指定，会自动生成
    #        aggregate       - "SUM" or "MIN" or "MAX". 存储交集时生成score的方式。默认执行 MIN操作。
    #        use_cache       - 是否使用缓存，如为False，则强制重新生成集合
    #        cache_seconds   - 缓存保留的秒数，默认为5秒
    #        start           - 与count参数必须共同使用。如果为None，则返回值为交集中的元素个数，如指定数字，则表示返回元素的起始序号。
    #        count           - 与start参数必须共同使用。默认为-1，返回全部的元素
    #    @return:
    #        int    - 生成交集的成员个数
    #        或 set - 交集的元素集合
    #    """
    #    # 获取要取交集的实际存储key列表
    #    rzset_obj_list.append(self)
    #    storage_keys = [o.storage_key for o in rzset_obj_list]
    #    if dest is None:
    #        # 将全部存储key连接后取md5值
    #        m = hashlib.md5()
    #        m.update(".".join(storage_keys))
    #        dest = m.hexdigest() + ".inter"
    #    _storage_key = self.__class__.get_storage_key(dest)
    #    if use_cache and self.get_client().exists(_storage_key):
    #        # 如果结果已经存在，则不用重新生成
    #        if not isinstance(start, int):
    #            return self.get_client().zcard(_storage_key)
    #    else:
    #        inter_length = self.get_client().zinterstore(_storage_key, storage_keys, aggregate)
    #        self.get_client().expire(_storage_key, cache_seconds)
    #    if isinstance(start, int):
    #        count = count if count == -1 else start + count
    #        return self.get_client().zrange(_storage_key, start, count)
    #    return inter_length


    #def union(self, rzset_obj_list, aggregate = "MIN", start = 0, count = 10):
    #    """
    #    获取并集
    #    @args:
    #        rzset_obj_list  - _SortedSetModel类型的变量列表
    #        aggregate       - "SUM" or "MIN" or "MAX". 存储并集时生成score的方式。默认执行 MIN操作。
    #    @return:
    #        int    - 生成并集的成员个数
    #    """
    #    # 获取要取并集的实际存储key列表
    #    rzset_obj_list.append(self)
    #    storage_keys = [o.storage_key for o in rzset_obj_list]
    #    if dest is None:
    #        # 将全部存储key连接后取md5值
    #        m = hashlib.md5()
    #        m.update(".".join(storage_keys))
    #        dest = m.hexdigest() + ".union"
    #    _storage_key = self.__class__.get_storage_key(dest)
    #    if self.get_client().exists(_storage_key):
    #        # 如果结果已经存在，则不用重新生成
    #        union_length = self.get_client().zcard(_storage_key)
    #    else:
    #        union_length = self.get_client().zunionstore(_storage_key, storage_keys, aggregate)
    #    self.get_client().expire(_storage_key, 3)  # 设置3秒后删除并集
    #    if isinstance(start, int):
    #        return self.get_client().zrange(_storage_key, start, start + count)
    #    return union_length
    #    #return self.unionstore(rzset_obj_list = rzset_obj_list, aggregate = aggregate, start = start, count = count)

    #def unionstore(self, rzset_obj_list, dest = None, use_cache = True, cache_seconds = 3, aggregate = "MIN", start = None, count = -1):
    #    """
    #    获取并集并存储到指定的key。
    #    @args:
    #        rzset_obj_list  - _SortedSetModel类型的变量列表
    #        dest            - str 求出并集后存储到的key，如不指定，会自动生成
    #        aggregate       - "SUM" or "MIN" or "MAX". 存储并集时生成score的方式。默认执行 MIN操作。
    #        use_cache       - 是否使用缓存，如为False，则强制重新生成集合
    #        cache_seconds   - 缓存保留的秒数，默认为5秒
    #        start           - 与count参数必须共同使用。如果为None，则返回值为并集中的元素个数，如指定数字，则表示返回元素的起始序号。
    #        count           - 与start参数必须共同使用。默认为-1，返回全部的元素
    #    @return:
    #        int    - 生成并集的成员个数
    #        或 set - 并集的元素集合
    #    """
    #    # 获取要取并集的实际存储key列表
    #    rzset_obj_list.append(self)
    #    storage_keys = [o.storage_key for o in rzset_obj_list]
    #    if dest is None:
    #        # 将全部存储key连接后取md5值
    #        m = hashlib.md5()
    #        m.update(".".join(storage_keys))
    #        dest = m.hexdigest() + ".union"
    #    _storage_key = self.__class__.get_storage_key(dest)
    #    if use_cache and self.get_client().exists(_storage_key):
    #        # 如果结果已经存在，则不用重新生成
    #        if not isinstance(start, int):
    #            return self.get_client().zcard(_storage_key)
    #    else:
    #        union_length = self.get_client().zunionstore(_storage_key, storage_keys, aggregate)
    #        self.get_client().expire(_storage_key, cache_seconds)
    #    if isinstance(start, int):
    #        count = count if count == -1 else start + count
    #        return self.get_client().zrange(_storage_key, start, count)
    #    return union_length

    






