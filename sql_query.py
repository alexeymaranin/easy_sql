
SYSTEM_FIELDS = ("Id", "CreatedDate", "UpdatedDate", "Data", "CreatorSubject", "ChangeAuthor", "IsDelMark")
FIELD_MODIFYER = "Data_"


class Select:
    def __init__(self, fields):
        if type(fields) is not tuple:
            self.fields = (fields,)  # tuple of tuples
        else:
            self.fields = fields  # tuple of tuples

    def get_fields(self):
        select_list = []
        for i in range(len(self.fields)):
            table_name = 'cmp' + str(i+1)
            for item in self.fields[i]:
                select_list.append((table_name, item))
        return select_list

    def make_select_sql_string(self):
        select_list = self.get_fields()
        sql_fields = 'SELECT '
        for item in select_list:
            field = FIELD_MODIFYER + item[1] if item[1] not in SYSTEM_FIELDS else item[1]
            sql_fields += '{}."{}" as "{}", '.format(item[0], field, item[1])

        sql_fields = sql_fields[:-2]

        return sql_fields

    def get_sql(self):
        return self.make_select_sql_string()


class From:
    def __init__(self, table):
        self.table = table

    def make_table_sql_string(self):
        sql_table = ' FROM "{}" as cmp1'.format(self.table)

        return sql_table

    def get_sql(self):
        return self.make_table_sql_string()


class Where:
    def __init__(self, filters):
        if type(filters) is not tuple:
            self.filters = (filters,)  # tuple of dicts
        else:
            self.filters = filters  # tuple of dicts

    def make_filter_sql_string(self):
        sql_filter = ' WHERE '
        for i in range(len(self.filters)):
            table_name = 'cmp' + str(i + 1)
            for item in self.filters[i]:
                filter_value, operator = self.get_item_and_operator(self.filters[i][item])
                item_parameter = self.convert_types_to_string(filter_value)
                item_field = FIELD_MODIFYER + item if item not in SYSTEM_FIELDS else item
                sql_filter += '''{}."{}" {} {} AND '''.format(table_name, item_field, operator, item_parameter)

        sql_filter = sql_filter[:-4]

        return sql_filter

    @staticmethod
    def convert_types_to_string(item):
        if type(item) is str:
            return """'{}'""".format(item)
        elif type(item) is int or type(item) is float:
            return '{}'.format(item)
        elif type(item) is bool:
            result = 'true' if item else 'false'
            return result
        elif item is None:
            return 'null'

    @staticmethod
    def get_negative_operator(item):
        if item is None:
            return 'IS NOT'
        elif str(item)[0] == '%' or str(item)[-1] == '%':
            return 'NOT LIKE'
        else:
            return '<>'

    @staticmethod
    def get_positive_operator(item):
        if item is None:
            return 'IS'
        elif str(item)[0] == '%' or str(item)[-1] == '%':
            return 'LIKE'
        else:
            return '='

    def get_item_and_operator(self, item):
        if type(item) is tuple:
            item = item[0]
            operator = self.get_negative_operator(item)
        else:
            operator = self.get_positive_operator(item)
        return item, operator

    def get_sql(self):
        return self.make_filter_sql_string()


class InnerJoin:
    def __init__(self, join_on):
        self.join_on = join_on  # dict where key is string, value is tuple

    def make_join_sql_string(self):
        sql_table = ''
        count = 2
        for join in self.join_on:
            main_field = FIELD_MODIFYER + self.join_on[join][0] if self.join_on[join][0] not in SYSTEM_FIELDS else self.join_on[join][0]
            join_field = FIELD_MODIFYER + self.join_on[join][1] if self.join_on[join][1] not in SYSTEM_FIELDS else self.join_on[join][1]
            sql_table += ' INNER JOIN "{}" as cmp{} ON cmp1."{}" = cmp{}."{}"'.format(join, count, main_field, count, join_field)
            count += 1
        return sql_table

    def get_sql(self):
        return self.make_join_sql_string()


class Limit:
    def __init__(self, limit):
        self.limit = limit

    def make_sql_string(self):
        sql = ' LIMIT {}'.format(self.limit)

        return sql

    def get_sql(self):
        return self.make_sql_string()


class OrderBy:
    def __init__(self, order_by):
        self.order_by = order_by

    def make_sql_string(self):
        if '-' in self.order_by:
            self.order_by = self.order_by.replace('-', '')
            ordering = 'DESC'
        else:
            ordering = 'ASC'

        self.order_by = FIELD_MODIFYER + self.order_by if self.order_by not in SYSTEM_FIELDS else self.order_by
        sql = ' ORDER BY "{}" {}'.format(self.order_by, ordering)

        return sql

    def get_sql(self):
        return self.make_sql_string()
