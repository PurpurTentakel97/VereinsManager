# Purpur Tentakel
# 20.03.2022
# VereinsManager / Password Validation

from logic import validation as v, window_handler
from config import error_code as e, config_sheet as c
from sqlite import select_handler as s_h
from helper import hasher
import debug

debug_str: str = "Password Validation"


def check_password(ID: int, password: str) -> str | bool:
    try:
        v.validation.must_positive_int(int_=ID)
        v.validation.must_str(str_=password)
    except (e.NoInt, e.NoPositiveInt, e.NoStr) as error:
        debug.error(item=debug_str, keyword="check_password", message=f"Error = {error.message}")
        return error.message

    hashed, valid = s_h.select_handler.get_hashed_password_by_ID(ID=ID)
    if not valid:
        return hashed

    result: bool = hasher.compare_password(password=password, hashed=hashed)
    if result:
        c.config.set_user(ID=ID)
        window_handler.create_main_window()
        return result
    else:
        return result
