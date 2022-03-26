# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
# Python 3.10

from config import config_sheet
from sqlite import database, global_handler as g_h
from logic.handler.pdf_handler import global_pdf_handler as g_p_h
from logic import validation

from logic.handler import window_handler


def _test() -> None:
    pass


# main
if __name__ == "__main__":
    config_sheet.create_config()
    database.crate_database()
    validation.create_validation()
    g_h.create_global_handler()
    g_p_h.create_pdf_handler()
    window_handler.on_start()
    _test()
