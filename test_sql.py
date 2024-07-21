import pytest
from sql_query import Select, From, Where, InnerJoin, Limit, OrderBy


@pytest.fixture
def sample_fields():
    fields1 = ("Id", "Email", "Department")
    fields2 = ("Id", "DepartmentName", "Project")
    fields3 = ("Id", "ProjectName", "Responsible")
    return fields1, fields2, fields3


def test_select(sample_fields):
    result1 = 'SELECT cmp1."Id" as "Id", cmp1."Data_Email" as "Email", cmp1."Data_Department" as "Department"'
    assert Select((sample_fields[0],)).get_sql() == result1

    result2 = ('SELECT cmp1."Id" as "Id", cmp1."Data_Email" as "Email", cmp1."Data_Department" as "Department", '
               'cmp2."Id" as "Id", cmp2."Data_DepartmentName" as "DepartmentName", cmp2."Data_Project" as "Project"')
    assert Select((sample_fields[0], sample_fields[1])).get_sql() == result2

    result3 = ('SELECT cmp1."Id" as "Id", cmp1."Data_Email" as "Email", cmp1."Data_Department" as "Department", '
               'cmp2."Id" as "Id", cmp2."Data_DepartmentName" as "DepartmentName", cmp2."Data_Project" as "Project", '
               'cmp3."Id" as "Id", cmp3."Data_ProjectName" as "ProjectName", cmp3."Data_Responsible" as "Responsible"')
    assert Select((sample_fields[0], sample_fields[1], sample_fields[2])).get_sql() == result3


@pytest.fixture
def sample_table():
    component = 'cee394d2-64fd-49d0-9221-1068ae010495'
    return component


def test_from(sample_table):
    result = ' FROM "cee394d2-64fd-49d0-9221-1068ae010495" as cmp1'
    assert From(sample_table).get_sql() == result


@pytest.fixture
def sample_filter():
    filter1 = {'Name': 'Alex', 'Id': 1, 'Department': None, 'LastName': (None,)}
    filter2 = {'DepartmentName': '%Special', 'Id': [5, 6, (7,)]}
    filter3 = {'Name': ('%Alex%',), 'Id_IN': (1, 2, 3), "Updated": True, "Vanished": False}
    return filter1, filter2, filter3


def test_where(sample_filter):
    result1 = """ WHERE cmp1."Data_Name" = 'Alex' AND cmp1."Id" = 1 AND cmp1."Data_Department" IS null AND cmp1."Data_LastName" IS NOT null """
    assert Where((sample_filter[0], )).get_sql() == result1

    result2 = """ WHERE cmp1."Data_Name" = 'Alex' AND cmp1."Id" = 1 AND cmp1."Data_Department" IS null AND cmp1."Data_LastName" IS NOT null AND cmp2."Data_DepartmentName" LIKE '%Special' AND cmp2."Id" = 5 AND cmp2."Id" = 6 AND cmp2."Id" <> 7 """
    assert Where((sample_filter[0], sample_filter[1])).get_sql() == result2

    result3 = """ WHERE cmp1."Data_Name" = 'Alex' AND cmp1."Id" = 1 AND cmp1."Data_Department" IS null AND cmp1."Data_LastName" IS NOT null AND cmp2."Data_DepartmentName" LIKE '%Special' AND cmp2."Id" = 5 AND cmp2."Id" = 6 AND cmp2."Id" <> 7 AND cmp3."Data_Name" NOT LIKE '%Alex%' AND cmp3."Id" IN (1, 2, 3) AND cmp3."Data_Updated" = true AND cmp3."Data_Vanished" = false """
    assert Where((sample_filter[0], sample_filter[1], sample_filter[2])).get_sql() == result3


@pytest.fixture
def sample_join():
    join = {'123123-456456-456-9221-100005': ('Department', 'Id'), '83e6ce3f-1211-4183-905c-29a3e1dcf468': ('Project', 'Id')}
    return join


def test_join(sample_join):
    result = (' INNER JOIN "123123-456456-456-9221-100005" as cmp2 ON cmp1."Data_Department" = cmp2."Id" INNER JOIN '
              '"83e6ce3f-1211-4183-905c-29a3e1dcf468" as cmp3 ON cmp1."Data_Project" = cmp3."Id"')
    assert InnerJoin(sample_join).get_sql() == result


def test_limit():
    result = ' LIMIT 5'
    assert Limit(5).get_sql() == result


def test_order_by():
    result1 = ' ORDER BY "Data_Name" ASC'
    result2 = ' ORDER BY "Id" DESC'
    assert OrderBy("Name").get_sql() == result1
    assert OrderBy("-Id").get_sql() == result2
