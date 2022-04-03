# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation Password
import pytest
from logic import password_validation as p_v
from config import exception_sheet as e, config_sheet as c
from tests import helper


def test_must_password_pass():
    password = helper.generate_password()
    p_v.must_password(password, password)


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
    with pytest.raises(expected):
        p_v.must_password(password_1, password_2)


@pytest.mark.parametrize(("ID", "password", "expected_password", "expected_function"), [
    (1, "default", True, True),
    (1, "1", False, True),
    (2, "1", False, False),
])
def test_check_user_password_pass(ID, password, expected_password, expected_function):
    helper.generate_temp_database()
    helper.generate_select_handler()
    result = p_v.check_user_password(ID, password, False)
    assert result[0] == expected_password
    assert result[1] == expected_function
    assert (ID == c.config.user_id) == expected_password
    helper.drop_select_handler()
    helper.delete_temp_database()
