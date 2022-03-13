# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
# Python 3.10

from config import config_sheet
from sqlite import database, global_handler as g_h
from pdf_handler import global_pdf_handler as g_p_h
from logic import validation

from ui import base_window, main_window, window_manager


def _test() -> None:
    pass


# main
if __name__ == "__main__":
    config_sheet.create_config()
    database.crate_database()
    validation.create_validation()
    g_h.create_global_handler()
    g_p_h.create_pdf_handler()
    window_manager.create_window_manager()
    _test()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()
