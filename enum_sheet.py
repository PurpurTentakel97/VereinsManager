# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

_all_types: dict = {
    "position": ("position_type", "Positions-Arten"),
    "membership": ("membership_type", "Mitgliets-Arten"),
    "phone_number": ("phone_number_type", "Telephon-Arten"),
    "mail": ("mail_type", "Mail-Arten")
}

member_types: list = [
    _all_types["position"],
    _all_types["membership"],
    _all_types["phone_number"],
    _all_types["mail"]
]


def get_all_types() -> list:
    all_types: list = list()
    for type_ in _all_types.items():
        all_types.append(type_[1])
    return all_types


class TypeType(Enum):
    ALL = 0
    MEMBER = 1
