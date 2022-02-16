# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

import config_sheet
from sqlite import database, global_handler as g_h, select_handler as s_h

from ui import base_window, main_window


def _test() -> None:
    s_h.select_handler.get_raw_types()
    # s_h.select_handler.get_names_of_member()
    # s_h.select_handler.get_names_of_member(active=False)
    # s_h.select_handler.get_data_from_member_by_id(id_=1)
    # s_h.select_handler.get_data_from_member_by_id(id_=3, active=False)
    # s_h.select_handler.get_all_types()
    # s_h.select_handler.get_all_types(active=False)
    # s_h.select_handler.get_types_of_member()
    # s_h.select_handler.get_types_of_member(active=False)
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
