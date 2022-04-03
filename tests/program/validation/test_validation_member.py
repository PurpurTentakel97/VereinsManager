# Purpur Tentakel
# 03.04.2022
# VereinsManager / Test Validation Member

import pytest

from logic import validation as v
from config import exception_sheet as e


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
def test_update_member_nexus_pass(data, type_):
    v.create_validation()
    v.validation.update_member_nexus(data, type_)


@pytest.mark.parametrize(("data", "type_", "expected"), [
    ([1, 2, 3, 4, 5], "type_", e.WrongLength),
    ([1, 2, 3], "type_", e.WrongLength),
    ([None, 2, None, "value"], "position", e.NoBool),
    ([None, 2, None, True], "phone", e.NoStr),
])
def test_update_member_nexus_exception(data, type_, expected):
    v.create_validation()
    with pytest.raises(expected):
        v.validation.update_member_nexus(data, type_)
