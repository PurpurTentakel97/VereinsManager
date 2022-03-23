# Purpur Tentakel
# 20.03.2022
# VereinsManager / Password Validation

from logic import validation as v
from logic.handler import window_handler
from config import config_sheet as c
from sqlite import select_handler as s_h
from helper import hasher
import debug

debug_str: str = "Password Validation"


def check_password(ID: int, password: str) -> bool:
    v.validation.must_positive_int(int_=ID)
    v.validation.must_str(str_=password)

    hashed = s_h.select_handler.get_hashed_password_by_ID(ID=ID)

    result: bool = hasher.compare_password(password=password, hashed=hashed)
    if result:
        c.config.set_user(ID=ID)
        window_handler.create_main_window()
    return result
