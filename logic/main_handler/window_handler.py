# Purpur Tentakel
# 21.01.2022
# VereinsManager / Window Handler

from helper import validation
from config import config_sheet as c, exception_sheet as e
from ui.windows import alert_window, base_window, window_manager, user_verify_window, main_window
import debug

debug_str: str = "Window Handler"


def on_start() -> None:
    window_manager.create_window_manager()
    base_window.create_application()
    user_verify_window.create()
    base_window.run_application()


def create_main_window() -> None:
    default_user = _is_default_user()
    main_window.create(default_user)
    if not default_user:
        alert_window.create()


def _is_default_user() -> bool:
    try:
        validation.must_default_user(c.config.user['ID'], True)
        return True
    except e.DefaultUserException:
        return False
