import sql_query
from collections import OrderedDict

order = ['SELECT', 'FROM', 'INNER JOIN', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT']


class BaseModel:
    component = ''
    fields = []
    pk = ''
    fk = ((None, ''),)

    def __init__(self):
        self.operators = OrderedDict({'SELECT': '',
                                      'FROM': '',
                                      'INNER JOIN': '',
                                      'WHERE': '',
                                      'GROUP BY': '',
                                      'HAVING': '',
                                      'ORDER BY': '',
                                      'LIMIT': '',
                                      })
        self.select_fields = []
        self.filters = []
        self.limit_value = 0
        self.join_on = {}
        self.order_field = ''

    def build_sql(self):
        fields = tuple(self.select_fields) if self.select_fields else (self.fields,)
        self.operators["SELECT"] = sql_query.Select(fields).get_sql()
        self.operators["FROM"] = sql_query.From(self.component).get_sql()
        if self.filters:
            self.filters[0].update({"IsDelMark": False})
            self.operators["WHERE"] = sql_query.Where(tuple(self.filters)).get_sql()
        if self.limit_value:
            self.operators["LIMIT"] = sql_query.Limit(self.limit_value).get_sql()
        if self.join_on:
            self.operators["INNER JOIN"] = sql_query.InnerJoin(self.join_on).get_sql()
        if self.order_field:
            self.operators["ORDER BY"] = sql_query.OrderBy(self.order_field).get_sql()

    def get_sql(self):
        self.build_sql()
        sql = ''
        # for item in self.operators:
        for item in order:
            if self.operators[item] != '':
                sql += self.operators[item]
        return sql

    def __repr__(self):
        return self.get_sql()

    def _select(self, fields=None, clear=False):
        fields = fields if fields else self.fields
        if clear:
            self.select_fields = []
        self.select_fields.append(fields)

    def _filter(self, filters, clear=False):
        if clear:
            self.filters = []
        if filters:
            self.filters.append(filters)

    def _limit(self, limit):
        self.limit_value = limit

    def get(self, pk):
        # fields = only if only else self.fields

        if type(pk) is dict:
            filters = pk  # | filters if filters else pk
        else:
            filters = {self.pk: pk}  # | filters if filters else {self.pk: pk}

        # self._select()

        self._filter(filters)
        self._limit(1)

        return self

    def only(self, *only_fields):
        if not isinstance(only_fields[0], (list, tuple)):
            only_fields = (only_fields,)

        for fields in only_fields:
            index = only_fields.index(fields)
            try:
                self.select_fields[index] = fields
            except IndexError:
                self.select_fields.append(fields)
        return self

    def filter(self, filters):
        if isinstance(filters, dict):
            filters = (filters,)

        for filt in filters:
            index = filters.index(filt)
            try:
                # self.filters[index] = self.filters[index] | filt  # for python >= 3.9
                self.filters[index].update(filt)
            except IndexError:
                self.filters.append(filt)
        return self

    def list(self):

        return self

    def limit(self, limit):
        self._limit(limit)

        return self

    def join(self, join_fields=None):
        if join_fields:
            if not isinstance(join_fields, (list, tuple)):
                join_fields = (join_fields,)

            join_models = []
            for obj in self.fk:
                if obj[1] in join_fields:
                    join_models.append(obj)
        else:
            join_models = self.fk

        join_on = {}
        fields_join = [tuple(self.fields)]
        for obj in join_models:
            model, field_join = obj
            join_on[model.component] = (field_join, model.pk)
            fields_join.append(tuple(model.fields))

        self.select_fields += fields_join
        self.join_on = join_on

        return self

    def order_by(self, order_field):
        self.order_field = order_field

        return self

    def first(self, limit=1):
        self._limit(limit)
        self.order_by("CreatedDate")

        return self

    def last(self, limit=1):
        self._limit(limit)
        self.order_by("-CreatedDate")

        return self
