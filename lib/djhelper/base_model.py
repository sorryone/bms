# -*- coding: utf-8 -*-
import copy
import json
import datetime
from django.forms.fields import Field
from django_filters import Filter

from django.db import models
from django.db.models.manager import Manager
from django.db.models import Q
__author__ = 'liling'


class AdvanceQueryset(models.query.QuerySet):
    """支持全文搜索的queryset
    """
    def __init__(self, model, *argv, **kwargs):
        self.search_fields = []              # 需要搜索的字段
        self.filter_like_fields = []         # 匹配包含关键字的字段
        self.filter_equal_fields = []        # 需完全匹配的字段
        self.period_fields = []              # 按时间段查询字段
        self.search_time_fields = []         # 需要搜索的时间字段

        super(AdvanceQueryset, self).__init__(model, *argv, **kwargs)
        for k in ["filter_like_fields",
                  "filter_equal_fields",
                  "search_time_fields",
                  "period_fields"]:
            setattr(self, k, getattr(model, k, []))
        search_fields = copy.copy(getattr(model, "search_fields", None))
        all_fields = self._get_model_fields(model)
        if search_fields:
            for field_name in search_fields:
                if field_name in all_fields and\
                        type(all_fields[field_name]) in (
                            models.TimeField, models.DateField,
                            models.DateTimeField,
                        ):
                    self.search_time_fields.append(field_name)
                else:
                    self.search_fields.append(field_name)

    @classmethod
    def _get_model_fields(cls, model):
        """获取一个model的全部字段信息
        """
        # self._get_model_fields(self.model.potential.field.related_model)['chosen_time']
        return dict([(f.name, f) for f in model._meta.fields])

    def search(self, keywords):
        """全文搜索
        """
        if not isinstance(keywords, (list, tuple)):
            raise Exception("search() argument must be `list` or `tuple`")
        search_query = self
        for keyword in keywords:
            if not keyword:
                continue
            filters = Q()
            for field in self.search_fields:
                filters |= Q(**{"%s__icontains" % field: keyword})
            for field in self.search_time_fields:
                filters |= Q(**{"%s__contains" % field: keyword})
            search_query = search_query.filter(filters)
        return search_query.distinct()

    def filter_fuzzy(self, **kwargs):
        """并列条件查询
        """
        filter_query = self
        filter_fields = self.filter_like_fields + self.filter_equal_fields
        if not filter_fields:
            raise Exception(
                '`filter_like_fields` and `filter_equal_fields` are empty.')
        for field, value in kwargs.iteritems():
            if field in filter_fields:
                if isinstance(value, (tuple, list)):
                    filters = Q()
                    for item in value:
                        if field in self.filter_equal_fields:
                            filters |= Q(**{field: item})
                        else:
                            filters |= Q(**{"%s__icontains" % field: item})
                    filter_query = filter_query.filter(filters)
                else:
                    if field in self.filter_equal_fields:
                        filter_query = filter_query.filter(**{field: value})
                    else:
                        filter_query = filter_query.filter(**{
                                        "%s__icontains" % field: value})
            elif field in self.period_fields:
                if not isinstance(value, (list, tuple)):
                    raise Exception(
                        "Time period field must be `tuple` or `list`.")
                start, end = value
                if isinstance(start, (int, float, str)):
                    start = datetime.datetime.fromtimestamp(start)
                if isinstance(end, (int, float, str)):
                    end = datetime.datetime.fromtimestamp(end)
                filters = Q(**{"%s__isnull" % field: False,
                            "%s__gte" % field: start, "%s__lt" % field: end})
                filter_query = filter_query.filter(filters)

        return filter_query


class AdvanceManager(Manager):
    def get_queryset(self):
        return AdvanceQueryset(self.model, using=self._db)

    def search(self, *argv, **kwargs):
        return self.all().search(*argv, **kwargs)

    def filter_fuzzy(self, *argv, **kwargs):
        return self.all().filter_fuzzy(*argv, **kwargs)


class JsonField(Field):
    def to_python(self, value):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            pass

        if isinstance(value, int):
            return (int(value),)
        elif isinstance(value, str):
            return (str(value),)
        elif isinstance(value, list):
            return value


class JsonFilter(Filter):
    field_class = JsonField
