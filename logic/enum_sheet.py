# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

weekDaysMapping = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


class DateType(Enum):
    DEAD_LINE = 0
    WORK_DATE = 1
    REMINDER_DATE = 2


class SQLite_Table(Enum):
    MEMBERS = "members"


class MemberEntries(Enum):
    ID = "id"

    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"

    STREET = "street"
    NUMBER = "number"
    ZIP_CODE = "zip_code"
    CITY = "city"

    BIRTH_DAY = "birth_day"
    ENTRY_DATE = "entry_date"

    PHONE_NUMBERS = "phone_numbers"
    MAIL_ADDRESSES = "mail_addresses"

    MEMBERSHIP_TYPE = "membership_type"
    SPECIAL_MEMBER = "special_member"
    POSITIONS = "positions"
    INSTRUMENTS = "instruments"

    COMMENT_TEXT = "comment_text"

    LOG = "log"
