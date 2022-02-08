# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

date_format: str = '%Y-%m-%d'

all_types: dict = {
    "position": ("position_type", "Positions-Arten"),
    "membership": ("membership_type", "Mitglieds-Arten"),
    "phone_number": ("phone_number_type", "Telephon-Arten"),
    "mail": ("mail_type", "Mail-Arten")
}

member_types: list = [
    all_types["position"],
    all_types["membership"],
    all_types["phone_number"],
    all_types["mail"]
]





def get_single_type(table_type: "TableTypes") -> str:
    match table_type:
        case TableTypes.MEMBER_PHONE:
            data = all_types["phone_number"]
            return data[0]
        case TableTypes.MEMBER_MAIL:
            data = all_types["mail"]
            return data[0]
        case TableTypes.MEMBER_POSITION:
            data = all_types["position"]
            return data[0]


class TypeType(Enum):
    ALL = 0
    MEMBER = 1


class TableTypes(Enum):
    MEMBER = "member"
    MEMBER_PHONE = "member_phone"
    MEMBER_MAIL = "member_mail"
    MEMBER_POSITION = "member_position"
    LOG = "log"


class MemberTypes(Enum):
    ID = "ID"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    STREET = "street"
    NUMBER = "number"
    ZIP_CODE = "zip_code"
    CITY = "city"
    B_DAY_DATE = "birth_day_date"
    ENTRY_DATE = "entry_date"
    MEMBERSHIP_TYPE = "membership_type"
    SPECIAL_MEMBER = "special_member"
    COMMENT = "comment"
    ACTIVE_MEMBER = "active_member"


class MemberPhoneTypes(Enum):
    ID = "ID"
    MEMBER_ID = "member_id"
    TYPE_ID = "type_id"
    NUMBER = "number"


class MemberMailTypes(Enum):
    ID = "ID"
    MEMBER_ID = "member_id"
    TYPE_ID = "type_id"
    MAIL = "mail"


class MemberPositionTypes(Enum):
    ID = "ID"
    MEMBER_ID = "member_id"
    TYPE_ID = "type_id"


class LogTypes(Enum):
    ID = "ID"
    MEMBER_ID = "member_id"
    LOG_TYPE = "log_type"
    DATE = "date"
    OLD_DATA = "old_data"
    NEW_DATA = "new_data"
