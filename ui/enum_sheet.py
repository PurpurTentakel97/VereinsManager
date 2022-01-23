# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

member_ship_type: list[str] = list()

position_types: list[str] = list()

uniform_types: list[str] = list()

performance_types: list[str] = list()

instrument_types: list[str] = list()

locations: dict[str, str] = dict()

special_user: dict[str,str] = dict()

members: list[dict] = list()


class EditLineType(Enum):
    FIRST_NAME = 0
    LAST_NAME = 1

    STREET = 2
    HOUSE_NUMBER = 3
    ZIP_CODE = 4
    CITY = 5

    PHONE_NUMBER = 6
    MAIL_ADDRESS = 7


class DateType(Enum):
    B_DAY = 0
    ENTRY = 1
