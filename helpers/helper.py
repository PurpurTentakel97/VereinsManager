# Purpur Tentakel
# 18.04.2022
# VereinsManager / Helper

import datetime

None_str: str = "-----"


def get_accurate_years_from_date_to_now(date: datetime.datetime) -> int:
    now: datetime.datetime = datetime.datetime.now()
    years: int = get_years_from_date_to_now(date=date)

    if now.month < date.month:
        return years - 1
    if now.day < date.day:
        return years - 1
    return years


def get_years_from_date_to_now(date: datetime.datetime) -> int:
    now: datetime.datetime = datetime.datetime.now()
    years: int = now.year - date.year
    return years


def transform_timestamp_to_datetime(timestamp: int) -> datetime.datetime:
    if timestamp:
        return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)


def transform_int_to_bool(integer: int) -> bool:
    return integer == 1


def transform_bool_to_int(bool_: bool) -> int:
    if bool_:
        return 1
    return 0


def combine_strings(strings: tuple[str, ...]) -> str:
    combined: str = str()
    for string in strings:
        if not is_str(string=string):
            continue
        combined += string + " "

    combined = try_transform_to_None_string(string=combined)
    return combined.strip()


def combine_maps_string(street: str, number: str, zip_code: str, city: str) -> str:
    street_number: str = str()
    if street and number:
        street_number = street + "+" + number
    elif street:
        street_number = street

    zip_code_city: str = str()
    if zip_code and city:
        zip_code_city = zip_code + "+" + city
    elif zip_code:
        zip_code_city = zip_code
    elif city:
        zip_code_city = city

    if not zip_code_city and not street_number:
        return None_str
    return f"www.google.de/maps/place/{street_number},+{zip_code_city}".strip()


def try_transform_to_None_string(string: str) -> str:
    if not is_str(string=string):
        return None_str
    return string


def is_str(string: str) -> bool:
    if not isinstance(string, str):
        return False
    string = string.strip()
    if not string:
        return False
    return True
