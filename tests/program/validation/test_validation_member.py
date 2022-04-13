# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation Member

import pytest

from helper import validation as v
from config import exception_sheet as e
from tests import helper


@pytest.mark.parametrize("member", [
    {'first_name': 'Hans Peter',
     'last_name': 'Schmitz',
     'street': 'Straße',
     'number': '66785',
     'zip_code': '56754',
     'birth_date': -2207955600,
     'entry_date': -2207178000,
     'city': 'Köln',
     'country': 'Deutschland',
     'membership_type': 'Type_1',
     'special_member': True,
     'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.\n{"a" * 200}',
     'maps': 'www.bester_link.com'}
])
def test_update_member_pass(member):
    helper.generate_temp_database()
    helper.add_generic_type()
    helper.generate_select_handler()
    v.check_update_member(member)
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("member", "expected"), [
    ({'first_name': 'Hans Peter',
      'last_name': 'Schmitz',
      'street': 'Straße',
      'number': '66785',
      'zip_code': '56754',
      'birth_date': -2207955600,
      'entry_date': -2207178000,
      'city': 'Köln',
      'country': 'Deutschland',
      'membership_type': 'Type_1',
      'special_member': True,
      'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.\n{"a" * 2000}',
      'maps': 'www.bester_link.com'}, e.ToLong),
    ({'first_name': 'Hans Peter',
      'last_name': 'Schmitz',
      'street': 'Straße',
      'number': '66785',
      'zip_code': '56754',
      'birth_date': -2207955600,
      'entry_date': -2207178000,
      'city': 'Köln',
      'country': 'Deutschland',
      'membership_type': 'Type_2',
      'special_member': True,
      'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.',
      'maps': 'www.bester_link.com'}, e.NotFound),
    ({'first_name': 'Hans Peter',
      'last_name': 'Schmitz',
      'street': 'Straße',
      'number': '66785',
      'zip_code': '56754',
      'birth_date': -2207955600,
      'entry_date': -2207178000,
      'city': 'Köln',
      'country': 'Deutschland',
      'membership_type': '',
      'special_member': True,
      'comment_text': f'Ich bin der weltbeste Kommtentar und sehr lang.',
      'maps': 'www.bester_link.com'}, e.NoMembership)
])
def test_update_member_exception(member, expected):
    helper.generate_temp_database()
    helper.add_generic_type()
    helper.generate_select_handler()
    with pytest.raises(expected):
        v.check_update_member(member)
    helper.drop_select_handler()
    helper.delete_temp_database()


@pytest.mark.parametrize(("data", "type_"), [
    ([1, 2, "Type", "value"], "phone"),
    ([None, 2, None, "value"], "phone"),
    ([None, 2, None, "value"], "mail"),
    ([None, 2, None, True], "position"),
])
def test_update_member_nexus_pass(data, type_):
    v.check_update_member_nexus(data, type_)


@pytest.mark.parametrize(("data", "type_", "expected"), [
    ([1, 2, 3, 4, 5], "type_", e.WrongLength),
    ([1, 2, 3], "type_", e.WrongLength),
    ([None, 2, None, "value"], "position", e.NoBool),
    ([None, 2, None, True], "phone", e.NoStr),
])
def test_update_member_nexus_exception(data, type_, expected):
    with pytest.raises(expected):
        v.check_update_member_nexus(data, type_)
