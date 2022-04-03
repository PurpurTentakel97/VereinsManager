# Purpur Tentakel
# 20.03.2022
# VereinsManager / Password Validation

import math

from logic import validation as v
from logic.handler import window_handler, user_handler
from config import config_sheet as c, exception_sheet as e
from helper import hasher
import debug

debug_str: str = "Password Validation"


def must_password(password_1: str, password_2: str) -> None:
    if not isinstance(password_1, str) or len(password_1.strip()) == 0:
        raise e.NoPassword()

    if password_1 != password_2:
        raise e.DifferentPassword()

    if len(password_1) < 8:
        raise e.PasswordToShort()

    if " " in password_1:
        raise e.PasswordHasSpace()

    count = get_count_for_password(password_1)
    if count <= 0:
        raise e.VeryLowPassword()
    bits = math.log(count ** len(password_1), 2)

    if bits < 20:
        raise e.VeryLowPassword()
    elif bits < 40:
        raise e.LowPassword()


def get_count_for_password(password_1):
    digit: int = 0
    capital_letter: int = 0
    small_letter: int = 0
    special_character: int = 0
    count: int = 0
    characters: list = list()

    for character in password_1:
        if character.islower():
            small_letter = 26
        elif character.isupper():
            capital_letter = 26
        elif character.isdigit():
            digit = 10
        elif character.isprintable():
            special_character = 43
        if character in characters:
            count -= 1
        characters.append(character)

    count += (digit + capital_letter + small_letter + special_character)
    return count


def check_user_password(ID: int, password: str) -> [str | bool, bool]:
    try:
        v.must_positive_int(int_=ID)
        v.must_str(str_=password)

        hashed = user_handler.get_hashed_password_by_ID(ID=ID)

        result: bool = hasher.compare_password(password=password, hashed=hashed)
        if result:
            c.config.set_user(ID=ID)
            window_handler.create_main_window()
        return result, True
    except (e.InputError, e.OperationalError, e.PasswordError) as error:
        debug.debug(item=debug_str, keyword="check_password", message=f"Message = {error.message}")
        return error.message, False
