# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

import config_sheet
from sqlite import database, select_handler, global_handler

from ui import base_window, main_window

# main
if __name__ == "__main__":
    database.crate_database()
    config_sheet.create_config()
    global_handler.create_global_handler()
    select_handler.select_handler.get_names_of_member()
    select_handler.select_handler.get_names_of_member(active=False)
    select_handler.select_handler.get_data_from_member_by_id(id_=1)
    select_handler.select_handler.get_data_from_member_by_id(id_=3, active=False)
    select_handler.select_handler.get_all_types()
    select_handler.select_handler.get_all_types(active=False)
    select_handler.select_handler.get_types_of_member()
    select_handler.select_handler.get_types_of_member(active=False)
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()
