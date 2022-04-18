# Purpur Tentakel
# 26.03.2022
# VereinsManager / Member Card Data Handler

import datetime

from helpers import helper
from config import config_sheet as c
from logic.main_handler import member_handler
from logic.sqlite import select_handler as s_h

debug_str: str = "Member Card Data Handler"


def get_card_member_data(active: bool, ID: int) -> dict:
    data, _ = member_handler.get_member_data(ID=ID, active=active)
    data['member_data'] = _transform_member_data(data['member_data'])
    data['phone'] = _transform_nexus_data(data['phone'])
    data['mail'] = _transform_nexus_data(data['mail'])
    data['position'] = _transform_position_data(data['position'])
    return data


def _get_years_from_timestamp(timestamp: int) -> str:
    if timestamp == c.config.date_format['None_date']:
        return helper.None_str
    date = helper.transform_timestamp_to_datetime(timestamp)
    years: int = helper.get_accurate_years_from_date_to_now(date=date)
    return str(years)


def _transform_member_data(data: dict) -> dict:  # No need to transform membership_type
    data = _transform_member_strings(data=data)
    data = _transform_maps(data=data)
    data = _transform_street(data=data)
    data = _transform_name(data=data)
    data = _transform_member_dates(data=data)
    return data


def _transform_member_strings(data: dict) -> dict:
    keys: list = [
        'zip_code',
        'city',
        'maps',
        'comment_text',
    ]
    key: str
    for key in keys:
        data[key] = helper.try_transform_to_None_string(string=data[key])
    return data


def _transform_maps(data: dict) -> dict:
    maps: str = helper.combine_maps_string(street=data['street'], number=data['number'], zip_code=data['zip_code'],
                                           city=data['city'])
    data['maps'] = maps
    return data


def _transform_street(data: dict) -> dict:
    street: str = data['street']
    number: str = data['number']

    address: str = helper.combine_strings(strings=(street, number))

    del data['number']
    data['street'] = address
    return data


def _transform_name(data: dict) -> dict:
    firstname: str = data['first_name']
    lastname: str = data['last_name']

    name: str = helper.combine_strings(strings=(firstname, lastname))

    del data['last_name']
    del data['first_name']
    data['name'] = name

    return data


def _transform_member_dates(data: dict) -> dict:
    data['years'] = _get_years_from_timestamp(timestamp=data['entry_date'])
    data['entry_date'] = _transform_date(timestamp=data['entry_date'])
    data['age'] = _get_years_from_timestamp(timestamp=data['birth_date'])
    data['birth_date'] = _transform_date(timestamp=data['birth_date'])
    return data


def _transform_nexus_data(data: dict) -> list:
    transformed: list = list()
    for entry in data:
        transformed.append(_transform_single_nexus_data(entry=entry))
    transformed = sorted(transformed, key=lambda x: x[0])
    return transformed


def _transform_single_nexus_data(entry: tuple) -> list:
    ID, type_id, value = entry

    value: str = helper.try_transform_to_None_string(string=value)
    type_id: int = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]

    return [type_id, value]


def _transform_position_data(data: dict) -> list:
    transformed: list = list()
    for entry in data:
        entry: tuple
        result: str = _transform_single_position(entry=entry)
        if not result:
            continue
        transformed.append(result)
    if len(transformed) == 0:
        transformed.append(helper.None_str)
    transformed.sort()
    return transformed


def _transform_single_position(entry: tuple) -> str:
    ID, type_id, active = entry
    if active:
        return s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]


def _transform_date(timestamp: int) -> str:
    if timestamp == c.config.date_format['None_date']:
        return helper.None_str
    return datetime.datetime.strftime(helper.transform_timestamp_to_datetime(timestamp), c.config.date_format['short'])
