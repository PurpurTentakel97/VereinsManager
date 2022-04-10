# Purpur Tentakel
# 10.04.2022
# VereinsManager / Test Validation Organisation

import pytest

from helper import validation as v
from config import exception_sheet as e


@pytest.mark.parametrize("data", [
    {
        'ID': None,
        'name': None,
        'street': None,
        'number': None,
        'zip_code': None,
        'city': None,
        'country': None,
        'bank_name': None,
        'bank_owner': None,
        'bank_IBAN': None,
        'bank_BIC': None,
        'contact_person': None,
        'web_link': None,
        'extra_text': None,
    }, {
        'ID': 1,
        'name': "test",
        'street': "test",
        'number': "test",
        'zip_code': "test",
        'city': "test",
        'country': "test",
        'bank_name': "test",
        'bank_owner': "test",
        'bank_IBAN': "test",
        'bank_BIC': "test",
        'contact_person': 1,
        'web_link': "test",
        'extra_text': "test",
    },
])
def test_add_update_organisation_pass(data):
    v.add_update_organisation(data=data)


@pytest.mark.parametrize(("data", "expected"), [
    ({
         'ID': None,
         'name': None,
         'street': None,
         'number': None,
         'zip_code': None,
         'city': None,
         'country': None,
         'bank_name': None,
         'bank_owner': None,
         'bank_IBAN': None,
         'bank_BIC': None,
         'contact_person': None,
         'web_link': None,
         'extra_text': None,
         '123': None,
     }, e.WrongLength), ({
                             'ID': None,
                             'name': None,
                             'street': None,
                             'number': None,
                             'zip_code': None,
                             'city': None,
                             'country': None,
                             'bank_name': None,
                             'bank_owner': None,
                             'bank_IBAN': None,
                             'bank_BIC': None,
                             'contact_person': None,
                             'web_link': None,
                         }, e.WrongLength),

])
def test_add_update_organisation_exception(data, expected):
    with pytest.raises(expected):
        v.add_update_organisation(data=data)
