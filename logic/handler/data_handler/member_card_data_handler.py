# Purpur Tentakel
# 26.03.2022
# VereinsManager / Member Card Data Handler

import datetime

from logic.handler.main_handler import member_handler
from sqlite import select_handler as s_h
from config import config_sheet as c
import debug

debug_str: str = "Member Card Data Handler"
none_str: str = "---"


def get_card_member_data(active: bool, ID: int) -> dict:
    data, _ = member_handler.get_member_data(ID=ID, active=active)
    data['member_data'] = _transform_member_data(data['member_data'])
    data['phone'] = _transform_nexus_data(data['phone'])
    data['mail'] = _transform_nexus_data(data['mail'])
    data['position'] = _transform_position_data(data['position'])
    return data


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
    for key in keys:
        data[key] = _transform_str(data[key])
    return data


def _transform_maps(data: dict) -> dict:
    if len(data['maps']) > 5:
        return data
    maps = f"""http://www.google.de/maps/place/{data['street']}+{data['number']},+{data['zip_code']}+{data['city']}"""
    data['maps'] = maps.replace(" ", "")
    return data


def _transform_street(data: dict) -> dict:
    street, number = data['street'], data['number']
    if street and number:
        address = f"{street} {number}"
    elif street:
        address = f"{street}"
    else:
        address = none_str

    del data['number']
    data['street'] = address
    return data


def _transform_name(data: dict) -> dict:
    firstname, lastname = data['first_name'], data['last_name']

    if firstname and lastname:
        name = f"{firstname} {lastname}"
    elif firstname:
        name = firstname
    elif lastname:
        name = lastname
    else:
        name = none_str

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
    if value is None:
        value = none_str
    type_id = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]
    return [type_id, value]


def _transform_position_data(data: dict) -> list:
    transformed: list = list()
    for entry in data:
        result = _transform_single_position(entry=entry)
        if result:
            transformed.append(result)
    if len(transformed) == 0:
        transformed.append(none_str)
    transformed.sort()
    return transformed


def _transform_single_position(entry: tuple) -> str:
    ID, type_id, active = entry
    if active:
        return s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]


def _transform_str(str_: str) -> str:
    if str_ is None:
        return none_str
    return str_


def _transform_bool(int_: int) -> bool:
    return int_ == 1


def _transform_date(timestamp: int) -> str:
    if timestamp == c.config.date_format['None_date']:
        return none_str
    return datetime.datetime.strftime(_transform_timestamp_to_date(timestamp), c.config.date_format['short'])


def _get_years_from_timestamp(timestamp: int) -> str:
    if timestamp == c.config.date_format['None_date']:
        return none_str

    now = datetime.datetime.now()
    date = _transform_timestamp_to_date(timestamp)
    years = now.year - date.year
    if now.month < date.month or (now.month == date.month and now.day < date.day):
        years -= 1
    return str(years)


def _transform_timestamp_to_date(timestamp: int) -> datetime.datetime:
    return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)
