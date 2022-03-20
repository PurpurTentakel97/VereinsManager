# Purpur Tentakel
# 21.01.2022
# VereinsManager / Window Handler

from ui.windows import alert_window, base_window, window_manager, user_verify_window, main_window


def on_start() -> None:
    window_manager.create_window_manager()
    base_window.create_application()
    user_verify_window.create_user_verify_window()
    base_window.run_application()


def create_main_window() -> None:
    main_window.create_main_window()
    alert_window.create_alert_window()
