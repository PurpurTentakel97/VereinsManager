# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
# Python 3.10

import sys

from config import config_sheet
from logic.sqlite import database, global_database_handler
from logic.pdf_handler import global_pdf_handler
from logic.main_handler import global_handler, window_handler

import debug

debug_str: str = "Main"

# main
if __name__ == "__main__":
    try:
        config_sheet.create_config()
        database.crate_database()
        global_database_handler.create_global_handler()
        global_pdf_handler.create_pdf_handler()
        window_handler.on_start()
        global_handler.delete_inactive_data()
        debug.export_error()
    except:
        debug.error(item=debug_str, keyword="main", error_=sys.exc_info())
        debug.export_error()
        exit()
