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

    B_DAY_DAY = 7
    B_DAY_YEAR = 6
    B_DAY_MONTH = 8

    ENTRY_DAY_DAY = 9
    ENTRY_DAY_MONTH = 10
    ENTRY_DAY_YEAR = 11

    PHONE_NUMBER = 12
    MAIL_ADDRESS = 13
