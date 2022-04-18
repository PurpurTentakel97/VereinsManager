# Purpur Tentakel
# 31.03.2022
# VereinsManager / Test Validation


import pytest
from tests import helper
import helpers.validation as v
import config.exception_sheet as e


# must string
@pytest.mark.parametrize("str_pass", [
    "abc",
    100 * " " + "a",
    50 * "a",
])
def test_must_str_pass(str_pass):
    v.must_str(str_pass)


def test_must_string_length_None():
    test_str = "a" * 100
    v.must_str(test_str, None)


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
    with pytest.raises(expected):
        v.must_str(str_exception)


# must membership type
@pytest.mark.parametrize("membership_type", [
    "Type_1",
])
def test_must_membership_type_pass(membership_type):
    helper.generate_temp_database()
    helper.add_generic_type()
    helper.generate_select_handler()
    v.must_membership_type(membership_type)
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("membership_type", "expected"), [
    ("Type_2", e.NotFound),
    ("", e.NoMembership),
    (5, e.NoMembership),
    (-9, e.NoMembership),
    (5.6, e.NoMembership),
    (-9.6, e.NoMembership),
    (str(), e.NoMembership),
    (bool(), e.NoMembership),
    (list(), e.NoMembership),
    (tuple(), e.NoMembership),
    (dict(), e.NoMembership),
])
def test_must_membership_type_pass(membership_type,expected):
    helper.generate_temp_database()
    helper.add_generic_type()
    helper.generate_select_handler()
    with pytest.raises(expected):
        v.must_membership_type(membership_type)
    helper.drop_select_handler()
    helper.delete_temp_database()


# must dict with strings
@pytest.mark.parametrize(("keys_pass", "data_pass"), [
    (["1"], {"1": "1"}),
    (["1"], {"1": None}),
])
def test_must_stings_in_dict_pass(keys_pass, data_pass):
    v._must_multiple_str_in_dict(keys_pass, data_pass)


@pytest.mark.parametrize(("keys_exception", "data_exception", "expected"), [
    ([1], {"1": "1"}, KeyError),
    ([1], 1, TypeError),
    (1, {"1": "1"}, TypeError),
])
def test_must_stings_in_dict_exception(keys_exception, data_exception, expected):
    with pytest.raises(expected):
        v._must_multiple_str_in_dict(keys_exception, data_exception)


# must bool
def test_must_bool_pass():
    v.must_bool(bool())


@pytest.mark.parametrize("bool_exception", [
    str(),
    int(),
    float(),
    list(),
    tuple(),
    dict(),
])
def test_must_bool_exception(bool_exception):
    with pytest.raises(e.NoBool):
        v.must_bool(bool_exception)


# must positive int
@pytest.mark.parametrize("int_pass", [
    5,
    helper.random_with_N_digits(5),
    helper.random_with_N_digits(15),
])
def test_must_positive_int_passed(int_pass):
    v.must_positive_int(int_=int_pass)


def test_must_positive_int_length_None():
    test_int = helper.random_with_N_digits(20)
    v.must_positive_int(test_int, None)


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
    with pytest.raises(expected):
        v.must_positive_int(int_exception)


# must int
@pytest.mark.parametrize("int_pass", [
    5,
    0,
    -6,
    helper.random_with_N_digits(5),
    helper.random_with_N_digits(15),
])
def test_must_int_passed(int_pass):
    v.must_int(int_=int_pass)


def test_must_int_length_None():
    test_int = helper.random_with_N_digits(20)
    v.must_int(test_int, None)


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
    with pytest.raises(expected):
        v.must_int(int_exception)


# must dict
def test_must_dict_pass():
    v.must_dict(dict())


@pytest.mark.parametrize("dict_exception", [
    str(),
    int(),
    float(),
    list(),
    tuple(),
    bool(),
])
def test_must_dict_exception(dict_exception):
    with pytest.raises(e.NoDict):
        v.must_dict(dict_exception)


# must list
def test_must_list_pass():
    v.must_list(list())


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
        v.must_list(dict_exception)


# must length
@pytest.mark.parametrize(("length_pass", "data"), [
    (2, [1, 2]),
    (2, "12"),
    (2, (1, 2)),
    (2, {"1": 1, "2": 2}.items())
])
def test_must_length_pass(length_pass, data):
    v.must_length(length_pass, data)


@pytest.mark.parametrize(("length", "data", "expected"), [
    (2, [1], e.WrongLength),
    (2, [1, 2, 3], e.WrongLength),
    (2, bool(), TypeError),
    (2, float(), TypeError),
    (2, int(), TypeError),
])
def test_must_length_exception(length, data, expected):
    with pytest.raises(expected):
        v.must_length(length, data)
