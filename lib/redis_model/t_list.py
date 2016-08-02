# -*- coding: utf-8 -*-
import redis
from base_model import RedisBase, RedisError

class _ListModel(RedisBase):
    """A redis-list model class.
    """
    data_type = "list"

    WHERE_BEFORE = "BEFORE"
    WHERE_AFTER = "AFTER"

    def __init__(self, pkey, *args, **kwargv):
        super(_ListModel, self).__init__(pkey, *args, **kwargv)

    def insert(self, where, ref_value, value):
        """向列表插入数据
        @args:
            where       - WHERE_BEFORE, WHERE_AFTER
            ref_value  -
            value      -
        @return:
            int     -  length of the list
        """
        return self.get_client().linsert(self.storage_key, where, ref_value, value)

    def set_i(self, index, value):
        """修改某个位置的元素值
        @args:
            index       -
            value       -
        @return:
            bool
        """
        return self.get_client().lset(self.storage_key, index, value)

    def remove(self, value, num = 0):
        """删除某个元素
        @args:
            value       -
            num         - 如果为0，则从列表中全部查找该值删除，如果>0则从左边删除指定数量，如果<0则从右边删除指定的数量
        @return:
            int     - 删除的元素个数
        """
        return self.get_client().lrem(self.storage_key, value, num)

    def length(self):
        """返回列表长度
        """
        return self.get_client().llen(self.storage_key)

    def range(self, start, end):
        """返回指定范围的元素
        @args:
            start           -
            end             -
        @return:
            int
        """
        return self.get_client().lrange(self.storage_key, start, end)

    def top(self, num):
        """获取前面若干数量的元素
        @args:
            num     - 数量
        """
        if num == 0:
            return []
        return self.get_client().lrange(self.storage_key, 0, (num - 1))

    def lpop(self):
        """删除列表的第一个元素
        @return:
            str     - 被删除的元素
        """
        return self.get_client().lpop(self.storage_key)

    def rpop(self):
        """删除列表的最后一个元素
        @return:
            str     - 被删除的元素
        """
        return self.get_client().rpop(self.storage_key)

    def lpush(self, *values):
        """将values里的值依次添加到列表起始
        @return:
            int     - 列表的新长度
        """
        return self.get_client().lpush(self.storage_key, *values)

    def lpushx(self, value):
        """将value添加到列表起始，如果列表不存在，则不做任何操作
        @return:
            int     - 列表的新长度
        """
        return self.get_client().lpushx(self.storage_key, value)

    def rpush(self, *values):
        """将values里的值依次添加到列表末尾
        @return:
            int     - 列表的新长度
        """
        return self.get_client().rpush(self.storage_key, *values)

    def rpushx(self, value):
        """将value添加到列表末尾，如果列表不存在，则不做任何操作
        @return:
            int     - 列表的新长度
        """
        return self.get_client().rpushx(self.storage_key, value)

    def rpoplpush(self, src, dst):
        """从src 列表中删除最后一个元素，并将这个元素添加到 dst 列表的起始
        @return:
            str     - 移动的元素
        """
        src_storage_key = self.__class__.get_storage_key(src)
        dst_storage_key = self.__class__.get_storage_key(dst)
        return self.get_client().rpoplpush(self.storage_key, src_storage_key, dst_storage_key)

    def index(self, index):
        """获取某个排名的元素
        @args:
            index       - 排名
        @return:
            str
        """
        return self.get_client().lindex(self.storage_key, index)

    def trim(self, start, end):
        """只保留列表中排名在start和end之间的元素，其他的删除
        @return:
            bool
        """
        return self.get_client().ltrim(self.storage_key, start, end)


    #['blpop', 'brpop', 'brpoplpush', ]







