# Purpur Tentakel
# 21.01.2022
# VereinsManager / Window Handler

from ui import window_manager, base_window
from helpers import validation
from logic.main_handler import global_handler
from config import config_sheet as c, exception_sheet as e
from ui.windows import alert_window, user_verify_window, main_window, recover_window

debug_str: str = "Window Handler"


def on_start(skip: bool = False) -> None:
    window_manager.create_window_manager()
    base_window.create_application()
    if not skip:
        user_verify_window.create()
    else:
        main_window.create(default_user=False)
    base_window.run_application()


def create_main_window() -> None:
    default_user = _is_default_user()
    main_window.create(default_user)
    if not default_user:
        alert_window.create()
        if global_handler.is_delete_inactive_data():
            recover_window.create_recover_window(type_="member")
            recover_window.create_recover_window(type_="user")


def _is_default_user() -> bool:
    try:
        validation.must_default_user(c.config.user['ID'], True)
        return True
    except e.DefaultUserException:
        return False
