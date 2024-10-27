from base_models import BaseModel
import pytest


class Account(BaseModel):
    component = 'account_table'
    fields = ["Id", "Bonuses", "IsActual", "MainAccount", "PremiumAccount", "PromotionalAccount"]
    pk = "Id"


class Shares(BaseModel):
    component = 'shares_table'
    fields = ["Id", "SharesCount"]
    pk = "Id"


class User(BaseModel):
    component = 'user_table'
    fields = ["Id", "Name", "Email", "Account", "IsActive", "Inviter", "Age", "Shares"]
    pk = "Id"
    fk = ((Account, "Account"), (Shares, "Shares"))


@pytest.fixture()
def simple_user_get():
    user = User().get(5)
    return user


@pytest.fixture()
def custom_user_get():
    user = User().get({"Name": "Alex"})
    return user


@pytest.fixture()
def simple_user_filter():
    user = User().filter({"IsActive": True})
    return user


@pytest.fixture()
def full_user_filter():
    user = User().filter({"Id_IN": [1,2,3,4,5], "Email": "%gmail.com", "IsActive": True, "Inviter": (None,), "Age": 18})
    return user


@pytest.fixture()
def simple_user_join():
    user = User().join()
    return user


@pytest.fixture()
def filter_user_join():
    user = User().join().filter({"Name": "Alex"})
    return user


def test_get(simple_user_get, custom_user_get):
    result1 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."Id" = 5 AND cmp1."IsDelMark" = false  LIMIT 1'''
    print(simple_user_get.get_sql())
    assert simple_user_get.get_sql() == result1

    result2 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."Data_Name" = 'Alex' AND cmp1."IsDelMark" = false  LIMIT 1'''
    assert custom_user_get.get_sql() == result2


def test_filter(simple_user_filter, full_user_filter):
    result1 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."Data_IsActive" = true AND cmp1."IsDelMark" = false '''
    assert simple_user_filter.get_sql() == result1

    result2 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."Id" IN (1, 2, 3, 4, 5) AND cmp1."Data_Email" LIKE '%gmail.com' AND cmp1."Data_IsActive" = true AND cmp1."Data_Inviter" IS NOT null AND cmp1."Data_Age" = 18 AND cmp1."IsDelMark" = false '''
    assert full_user_filter.get_sql() == result2


def test_limit():
    result = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."IsDelMark" = false  LIMIT 5'''
    assert User().limit(5).get_sql() == result


def test_order_by():
    result1 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."IsDelMark" = false  ORDER BY "Data_Name" ASC'''
    assert User().order_by("Name").get_sql() == result1

    result2 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."IsDelMark" = false  ORDER BY "Data_Name" DESC'''
    assert User().order_by("-Name").get_sql() == result2


def test_first():
    result = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."IsDelMark" = false  ORDER BY "CreatedDate" ASC LIMIT 1'''
    assert User().first().get_sql() == result


def test_last():
    result = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares" FROM "user_table" as cmp1 WHERE cmp1."IsDelMark" = false  ORDER BY "CreatedDate" DESC LIMIT 1'''
    assert User().last().get_sql() == result


def test_join(simple_user_join, filter_user_join):
    result1 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert simple_user_join.get_sql() == result1

    result2 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert simple_user_join.only("Id", "Name").get_sql() == result2

    result3 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp2."Data_Bonuses" as "Bonuses", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert simple_user_join.only(("Id", "Name"), ("Bonuses",)).get_sql() == result3

    result4 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."Data_Name" = 'Alex' AND cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert filter_user_join.get_sql() == result4

    result5 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."Data_Name" = 'Alex' AND cmp1."IsDelMark" = false AND cmp2."Data_IsActual" = true AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert User().join().filter(({"Name": "Alex"}, {"IsActual": True})).get_sql() == result5

    result6 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp2."Data_Bonuses" as "Bonuses", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."Data_Name" = 'Alex' AND cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false '''
    assert filter_user_join.only(("Id", "Name"), ("Bonuses",)).get_sql() == result6

    result7 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false  LIMIT 5'''
    assert User().join().limit(5).get_sql() == result7

    result8 = '''SELECT cmp1."Id" as "Id", cmp1."Data_Name" as "Name", cmp1."Data_Email" as "Email", cmp1."Data_Account" as "Account", cmp1."Data_IsActive" as "IsActive", cmp1."Data_Inviter" as "Inviter", cmp1."Data_Age" as "Age", cmp1."Data_Shares" as "Shares", cmp2."Id" as "Id", cmp2."Data_Bonuses" as "Bonuses", cmp2."Data_IsActual" as "IsActual", cmp2."Data_MainAccount" as "MainAccount", cmp2."Data_PremiumAccount" as "PremiumAccount", cmp2."Data_PromotionalAccount" as "PromotionalAccount", cmp3."Id" as "Id", cmp3."Data_SharesCount" as "SharesCount" FROM "user_table" as cmp1 INNER JOIN "account_table" as cmp2 ON cmp1."Data_Account" = cmp2."Id" INNER JOIN "shares_table" as cmp3 ON cmp1."Data_Shares" = cmp3."Id" WHERE cmp1."IsDelMark" = false AND cmp2."IsDelMark" = false AND cmp3."IsDelMark" = false  ORDER BY "Data_Name" ASC'''
    assert User().join().order_by("Name").get_sql() == result8


