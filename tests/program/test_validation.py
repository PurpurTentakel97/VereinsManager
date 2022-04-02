# Purpur Tentakel
# 31.03.2022
# VereinsManager / Test Validation


import pytest
from tests import helper
import logic.validation as v
import config.exception_sheet as e


# global
# must string
@pytest.mark.parametrize("str_pass", [
    "abc",
    100 * " " + "a",
    50 * "a",
])
def test_must_str_pass(str_pass):
    v.create_validation()
    v.validation.must_str(str_pass)


def test_must_string_length_None():
    test_str = "a" * 100
    v.create_validation()
    v.validation.must_str(test_str, None)


@pytest.mark.parametrize(("str_exception", "expected"), [
    (5, e.NoStr),
    (-9, e.NoStr),
    (5.6, e.NoStr),
    (-9.6, e.NoStr),
    (str(), e.NoStr),
    (bool(), e.NoStr),
    (list(), e.NoStr),
    (tuple(), e.NoStr),
    (dict(), e.NoStr),
    ("a" * 51, e.ToLong),
    ("a" * 100, e.ToLong),
])
def test_must_string_exception(str_exception, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.must_str(str_exception)


# must dict with strings
@pytest.mark.parametrize(("keys_pass", "data_pass"), [
    (["1"], {"1": "1"}),
    (["1"], {"1": None}),
])
def test_must_stings_in_dict_pass(keys_pass, data_pass):
    v.create_validation()
    v.validation._must_multiple_str_in_dict(keys_pass, data_pass)


@pytest.mark.parametrize(("keys_exception", "data_exception", "expected"), [
    ([1], {"1": "1"}, KeyError),
    ([1], 1, TypeError),
    (1, {"1": "1"}, TypeError),
])
def test_must_stings_in_dict_exception(keys_exception, data_exception, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation._must_multiple_str_in_dict(keys_exception, data_exception)


# must bool
def test_must_bool_pass():
    v.create_validation()
    v.validation.must_bool(bool())


@pytest.mark.parametrize("bool_exception", [
    str(),
    int(),
    float(),
    list(),
    tuple(),
    dict(),
])
def test_must_bool_exception(bool_exception):
    v.create_validation()
    with pytest.raises(e.NoBool):
        v.validation.must_bool(bool_exception)


# must positive int
@pytest.mark.parametrize("int_pass", [
    5,
    helper.random_with_N_digits(5),
    helper.random_with_N_digits(15),
])
def test_must_positive_int_passed(int_pass):
    v.create_validation()
    v.validation.must_positive_int(int_=int_pass)


def test_must_positive_int_length_None():
    test_int = helper.random_with_N_digits(20)
    v.validation.must_positive_int(test_int, None)


@pytest.mark.parametrize(("int_exception", "expected"), [
    (5.6, e.NoInt),
    (-9.6, e.NoInt),
    (-9, e.NoPositiveInt),
    (0, e.NoPositiveInt),
    ("string", e.NoInt),
    (bool(), e.NoInt),
    (list(), e.NoInt),
    (tuple(), e.NoInt),
    (dict(), e.NoInt),
    (helper.random_with_N_digits(16), e.ToLong),
    (helper.random_with_N_digits(25), e.ToLong),
])
def test_must_positive_int_exception(int_exception, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.must_positive_int(int_exception)


# must int
@pytest.mark.parametrize("int_pass", [
    5,
    0,
    -6,
    helper.random_with_N_digits(5),
    helper.random_with_N_digits(15),
])
def test_must_int_passed(int_pass):
    v.create_validation()
    v.validation.must_int(int_=int_pass)


def test_must_int_length_None():
    test_int = helper.random_with_N_digits(20)
    v.validation.must_int(test_int, None)


@pytest.mark.parametrize(("int_exception", "expected"), [
    (5.6, e.NoInt),
    (-9.6, e.NoInt),
    ("string", e.NoInt),
    (bool(), e.NoInt),
    (list(), e.NoInt),
    (tuple(), e.NoInt),
    (dict(), e.NoInt),
    (helper.random_with_N_digits(16), e.ToLong),
    (helper.random_with_N_digits(25), e.ToLong),
])
def test_must_int_exception(int_exception, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.must_int(int_exception)


# must dict
def test_must_dict_pass():
    v.create_validation()
    v.validation.must_dict(dict())


@pytest.mark.parametrize("dict_exception", [
    str(),
    int(),
    float(),
    list(),
    tuple(),
    bool(),
])
def test_must_dict_exception(dict_exception):
    v.create_validation()
    with pytest.raises(e.NoDict):
        v.validation.must_dict(dict_exception)


# must list
def test_must_list_pass():
    v.create_validation()
    v.validation.must_list(list())


@pytest.mark.parametrize("dict_exception", [
    str(),
    int(),
    float(),
    tuple(),
    bool(),
    dict(),
])
def test_must_list_exception(dict_exception):
    with pytest.raises(e.NoList):
        v.validation.must_list(dict_exception)


# must length
@pytest.mark.parametrize(("length_pass", "data"), [
    (2, [1, 2]),
    (2, "12"),
    (2, (1, 2)),
    (2, {"1": 1, "2": 2}.items())
])
def test_must_length_pass(length_pass, data):
    v.create_validation()
    v.validation.must_length(length_pass, data)


@pytest.mark.parametrize(("length", "data", "expected"), [
    (2, [1], e.WrongLength),
    (2, [1, 2, 3], e.WrongLength),
    (2, bool(), TypeError),
    (2, float(), TypeError),
    (2, int(), TypeError),
])
def test_must_length_exception(length, data, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.must_length(length, data)


# must password
def test_must_password_pass():
    password = helper.generate_password()
    v.create_validation()
    v.validation.must_password(password, password)


@pytest.mark.parametrize(("password_1", "password_2", "expected"), [
    (int(), None, e.NoPassword),
    (float(), None, e.NoPassword),
    (list(), None, e.NoPassword),
    (tuple(), None, e.NoPassword),
    (dict(), None, e.NoPassword),
    (bool(), None, e.NoPassword),
    (None, None, e.NoPassword),
    (str(), None, e.NoPassword),
    ("123", "456", e.DifferentPassword),
    ("123", "123", e.PasswordToShort),
    ("1 23456789", "1 23456789", e.PasswordHasSpace),
    ("1111111111", "1111111111", e.VeryLowPassword),
    ("1234567890", "1234567890", e.LowPassword),
])
def test_must_password_exception(password_1, password_2, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.must_password(password_1, password_2)


# type
@pytest.mark.parametrize(("name", "raw_type_id"), [
    ("type_2", 1),
    ("TYPE_1", 2),
    ("Test_type                      ", 2),
])
def test_add_type_pass(name, raw_type_id):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    v.validation.add_type(type_name=name, raw_type_id=raw_type_id)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_add_type_exception():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    with pytest.raises(e.AlreadyExists):
        v.validation.add_type(type_name="type_2", raw_type_id=2)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_update_type_pass():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    v.validation.update_type(1, "test")
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("ID", "new_name", "expexted"), [
    (1, "type_1", e.NoChance),
    (1, "TYPE_1", e.NoChance),
    (1, "TYPE_1           ", e.NoChance),
    (10, "xxxx", e.NotFound),
])
def test_update_type_exception(ID, new_name, expexted):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    with pytest.raises(expexted):
        v.validation.update_type(ID, new_name)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_update_type_activity_pass():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    v.validation.update_type_activity(1, False)
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("ID", "active", "expexted"), [
    (1, True, e.NoChance),
    (10, False, e.NotFound),
])
def test_update_type_activity_exception(ID, active, expexted):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.create_validation()
    with pytest.raises(expexted):
        v.validation.update_type_activity(ID, active)
    helper.drop_select_handler()
    helper.delete_temp_database()


# member
@pytest.mark.parametrize("member", [
    {'first_name': 'Hans Peter',
     'last_name': 'Schmitz',
     'street': 'Straße',
     'number': '66785',
     'zip_code': '56754',
     'birth_date': -2207955600,
     'entry_date': -2207178000,
     'city': 'Köln',
     'membership_type': 'Aktiv',
     'special_member': True,
     'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.\n{"a" * 200}',
     'maps': 'www.bester_link.com'}
])
def test_update_member_pass(member):
    v.create_validation()
    v.validation.update_member(member)


@pytest.mark.parametrize(("member", "expected"), [
    ({'first_name': 'Hans Peter',
      'last_name': 'Schmitz',
      'street': 'Straße',
      'number': '66785',
      'zip_code': '56754',
      'birth_date': -2207955600,
      'entry_date': -2207178000,
      'city': 'Köln',
      'membership_type': 'Aktiv',
      'special_member': True,
      'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.\n{"a" * 2000}',
      'maps': 'www.bester_link.com'}, e.ToLong)
])
def test_update_member_exception(member, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.update_member(member)


@pytest.mark.parametrize(("data", "type_"), [
    ([1, 2, "Type", "value"], "phone"),
    ([None, 2, None, "value"], "phone"),
    ([None, 2, None, "value"], "mail"),
    ([None, 2, None, True], "position"),
])
def test_update_member_nexus_exception(data, type_):
    v.create_validation()
    v.validation.update_member_nexus(data, type_)


@pytest.mark.parametrize(("data", "type_", "expected"), [
    ([1, 2, 3, 4, 5], "type_", e.WrongLength),
    ([1, 2, 3], "type_", e.WrongLength),
    ([None, 2, None, "value"], "position", e.NoBool),
    ([None, 2, None, True], "phone", e.NoStr),
])
def test_update_member_nexus_pass(data, type_, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.update_member_nexus(data, type_)
