# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
# Python 3.10

from config import config_sheet
from sqlite import database, global_handler as g_h

from ui import base_window, main_window


def _test() -> None:
    pass


# main
if __name__ == "__main__":
    database.crate_database()
    config_sheet.create_config()
    g_h.create_global_handler()
    _test()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()
