# Purpur Tentakel
# 18.02.2022
# VereinsManager / Error Code

from enum import Enum


class ErrorCode(Enum):
    # Success
    OK_S = 0
    LOAD_S = 1
    ADD_S = 2
    UPDATE_S = 3
    ACTIVE_SET_S = 4
    DELETE_S = 5

    # Operational Error
    LOAD_E = 100
    ADD_E = 101
    UPDATE_E = 102
    ACTIVE_SET_E = 103
    DELETE_E = 104

    # Database
    F_KEY_E = 200

    # Input Error
    NO_INPUT = 300
    NO_ID = 301
    NO_CHANCE = 302
    ALREADY_EXISTS_E = 303
