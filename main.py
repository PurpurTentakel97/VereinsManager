# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
# Python 3.10

from config import config_sheet
from sqlite import database, global_database_handler
from logic.handler.pdf_handler import global_pdf_handler
from logic.handler import global_handler
from logic import validation

from logic.handler import window_handler


def _test() -> None:
    pass


# main
if __name__ == "__main__":
    config_sheet.create_config()
    database.crate_database()
    validation.create_validation()
    global_database_handler.create_global_handler()
    global_pdf_handler.create_pdf_handler()
    window_handler.on_start()
    global_handler.delete_inactive_data()
    _test()
