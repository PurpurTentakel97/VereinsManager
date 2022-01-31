# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum

types = [
    ("positions", "Positionsarten"),
    ("membership_type", "Mitglietsarten"),
    ("phone_number", "Telefonarten"),
    ("e_mail", "Mailarten")
]


class SQLite_Table(Enum):
    MEMBERS = "members"
