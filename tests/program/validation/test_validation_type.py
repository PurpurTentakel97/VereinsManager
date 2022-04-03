# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation Type

import pytest

from logic import validation as v
from config import exception_sheet as e
from tests import helper


@pytest.mark.parametrize(("name", "raw_type_id"), [
    ("type_2", 1),
    ("TYPE_1", 2),
    ("Test_type                      ", 2),
])
def test_add_type_pass(name, raw_type_id):
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.add_type(type_name=name, raw_type_id=raw_type_id)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_add_type_exception():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    with pytest.raises(e.AlreadyExists):
        v.add_type(type_name="type_2", raw_type_id=2)
    helper.drop_select_handler()
    helper.delete_temp_database()


def test_update_type_pass():
    helper.generate_temp_database()
    helper.generate_select_handler()
    helper.add_generic_type()
    v.update_type(1, "test")
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
    with pytest.raises(expexted):
        v.update_type(ID, new_name)
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
