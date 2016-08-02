# -*- coding: utf-8 -*-
import redis
import cPickle as pickle
from t_string import _StringModel

class _KVModel(_StringModel):
    """
    将对象存储到StringModel里。
    需要子类实现以下变量：
        fields   -  字段及其类型
        key_name -  主键名
    """
    def __init__(self, pkey, *args, **kwargv):
        super(_KVModel, self).__init__(pkey, *args, **kwargv)

    @classmethod
    def get(cls, pkey):
        o = super(_KVModel, cls).get(pkey)
        if o is None:
            return None
        _data = eval(o.get_value())
        for field, ftype in cls.fields.items():
            if ftype == "adv":
                setattr(o, field, pickle.loads(_data.get(field, "N.")))  # "N." 会被反序列化为 None
            elif ftype in ["int", "float", "long"]:
                setattr(o, field, eval("%s(%s)"% (ftype, _data.get(field, 0))))
            else:
                setattr(o, field, _data.get(field))
        return o

    def put(self):
        """Save value to redis
        """
        _data = {}
        for field, ftype in self.fields.items():
            if ftype == "adv":
                _data[field] = pickle.dumps(getattr(self, field))
            else:
                _data[field] = getattr(self, field)
        self.set_value(repr(_data))

    def copy(self, new_pkey):
        """将一个对象的数据拷贝一份，生成新的对象返回
        """
        new_obj = self.__class__(new_pkey)
        for k, v in self.fields.items():
            if k == "pkey":
                setattr(new_obj, k, new_pkey)
            else:
                setattr(new_obj, k, getattr(self, k, None))
        #self.__class__(new_pkey).set_value(self.get_value())
        new_obj.put()
        #new_obj = self.__class__.get(new_pkey)
        #print new_obj.name
        return new_obj

    def putex(self, time):
        """Save value to redis and expires in ``time`` seconds
        """
        _data = {}
        for field, ftype in self.fields.items():
            if ftype == "adv":
                _data[field] = pickle.dumps(getattr(self, field))
            else:
                _data[field] = getattr(self, field)
        self.setex(repr(_data), time)

    def dumps(self):
        _data = {}
        for field in self.fields.keys():
            _data[field] = getattr(self, field)
        return _data

    @classmethod
    def mget(cls, keys):
        o_list = super(_KVModel, cls).mget(keys)
        for o in o_list:
            if o is None:
                continue
            _data = eval(o.get_value())
            for field, ftype in cls.fields.items():
                if ftype == "adv":
                    setattr(o, field, pickle.loads(_data.get(field, "N.")))  # "N." 会被反序列化为 None
                elif ftype in ["int", "float", "long"]:
                    setattr(o, field, eval("%s(%s)"% (ftype, _data.get(field, 0))))
                else:
                    setattr(o, field, _data.get(field))
        return o_list



