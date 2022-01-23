# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum


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
