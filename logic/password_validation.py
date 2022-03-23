# Purpur Tentakel
# 20.03.2022
# VereinsManager / Password Validation

from logic import validation as v
from logic.handler import window_handler, user_handler
from config import config_sheet as c, exception_sheet as e
from helper import hasher
import debug

debug_str: str = "Password Validation"


def check_password(ID: int, password: str) -> [str | bool, bool]:
    try:
        v.validation.must_positive_int(int_=ID)
        v.validation.must_str(str_=password)

        hashed = user_handler.get_hashed_password_by_ID(ID=ID)

        result: bool = hasher.compare_password(password=password, hashed=hashed)
        if result:
            c.config.set_user(ID=ID)
            window_handler.create_main_window()
        return result, True
    except (e.InputError, e.OperationalError, e.PasswordError) as error:
        debug.debug(item=debug_str, keyword="check_password", message=f"Message = {error.message}")
        return error.message, False
