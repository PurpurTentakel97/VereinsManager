# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation Type

import pytest

from helper import validation as v
from config import exception_sheet as e
from tests import helper


@pytest.mark.parametrize(("name", "raw_type_id", "extra_value"), [
    ("type_2", 1, "string"),
    ("TYPE_1", 2, None),
    ("Test_type                      ", 2, None),
])
def test_add_type_pass(name, raw_type_id, extra_value):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.add_type(type_name=name, raw_type_id=raw_type_id, extra_value=extra_value)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_add_type_exception():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    with pytest.raises(e.AlreadyExists):
        v.add_type(type_name="type_2", raw_type_id=2, extra_value="string")
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize("extra_value", [
    None,
    "string"
])
def test_update_type_pass(extra_value):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.update_type(1, "test", extra_value)
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("ID", "new_name", "extra_value", "expexted"), [
    (1, "type_1", "None", e.NoChance),
    (1, "TYPE_1", "None", e.NoChance),
    (1, "TYPE_1           ", "None", e.NoChance),
    (10, "xxxx", None, e.NotFound),
    (10, "TYPE_1", 1, e.NoStr),
])
def test_update_type_exception(ID, new_name, extra_value, expexted):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    with pytest.raises(expexted):
        v.update_type(ID, new_name, extra_value)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_update_type_activity_pass():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.update_type_activity(1, False)
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
    with pytest.raises(expexted):
        v.update_type_activity(ID, active)
    helper.drop_select_handler()
    helper.delete_temp_database()
