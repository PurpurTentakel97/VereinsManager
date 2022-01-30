# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

types = [
    "instruments",
    "positions",
    "membership_type",
    "phone_number",
    "e_mail"
]


class SQLite_Table(Enum):
    MEMBERS = "members"
