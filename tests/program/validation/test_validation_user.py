# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation User

import pytest

from logic import validation as v
from config import exception_sheet as e
from tests import helper


@pytest.mark.parametrize("user", [
    {"firstname": "123",
     "lastname": "123",
     "street": "123",
     "number": "123",
     "city": "123",
     "phone": "123",
     "mail": "123",
     "position": "123",
     "zip_code": "123",
     "ID": 2,
     "password_1": "1234567890AB",
     "password_2": "1234567890AB",
     },
    {"firstname": None,
     "lastname": None,
     "street": None,
     "number": None,
     "city": None,
     "phone": None,
     "mail": None,
     "position": None,
     "zip_code": None,
     "ID": 2,
     "password_1": "1234567890AB",
     "password_2": "1234567890AB",
     },
    {"firstname": "123",
     "lastname": "123",
     "street": "123",
     "number": "123",
     "city": "123",
     "phone": "123",
     "mail": "123",
     "position": "123",
     "zip_code": "123",
     "ID": None,
     "password_1": "1234567890AB",
     "password_2": "1234567890AB",
     },
    {"firstname": "123",
     "lastname": "123",
     "street": "123",
     "number": "123",
     "city": "123",
     "phone": "123",
     "mail": "123",
     "position": "123",
     "zip_code": "123",
     "ID": 2,
     "password_1": None,
     "password_2": None,
     },
])
def test_save_update_user_pass(user):
    helper.add_user_ids_in_config()
    v.save_update_user(user)


@pytest.mark.parametrize(("user", "expected"), [
    ({"firstname": "123",
      "lastname": "123",
      "street": "123",
      "number": "123",
      "city": "123",
      "phone": "123",
      "mail": "123",
      "position": "123",
      "zip_code": "123",
      "ID": None,
      "password_1": None,
      "password_2": None,
      }, e.NoPassword),
    ({"firstname": "123",
      "lastname": "123",
      "street": "123",
      "number": "123",
      "city": "123",
      "phone": "123",
      "mail": "123",
      "position": "123",
      "zip_code": "123",
      "ID": 1,
      "password_1": None,
      "password_2": None,
      }, e.DefaultUserException),
    ({"firstname": "123",
      "lastname": "123",
      "street": "123",
      "number": "123",
      "city": "123",
      "phone": "123",
      "mail": "123",
      "position": "123",
      "zip_code": "123",
      "ID": 3,
      "password_1": None,
      "password_2": None,
      }, e.CurrentUserException),

])
def test_save_update_user_exception(user, expected):
    helper.add_user_ids_in_config()
    with pytest.raises(expected):
        v.save_update_user(user)


@pytest.mark.parametrize(("ID", "bool_"), [
    (2, True),
    (3, False),
])
def test_must_current_user_pass(ID, bool_):
    helper.add_user_ids_in_config()
    v.must_current_user(ID, bool_)


@pytest.mark.parametrize(("ID", "bool_", "expected"), [
    (3, True, e.CurrentUserException),
    (2, False, e.CurrentUserException),
])
def test_must_current_user_exception(ID, bool_, expected):
    helper.add_user_ids_in_config()
    with pytest.raises(expected):
        v.must_current_user(ID, bool_)


@pytest.mark.parametrize(("ID", "bool_"), [
    (1, True),
    (2, False),
])
def test_must_default_user_pass(ID, bool_):
    helper.add_user_ids_in_config()
    v.must_default_user(ID, bool_)


@pytest.mark.parametrize(("ID", "bool_", "expected"), [
    (2, True, e.DefaultUserException),
    (1, False, e.DefaultUserException),
])
def test_must_default_user_exception(ID, bool_, expected):
    helper.add_user_ids_in_config()
    with pytest.raises(expected):
        v.must_default_user(ID, bool_)
