# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

import config_sheet
from sqlite import database



# main
if __name__ == "__main__":
    database.crate_database()
    config_sheet.create_config()
    #main_handler.create_database_classes()
    #main_handler.create_all_tables()
    #base_window.create_application()
    #main_window.main_window_ = main_window.MainWindow()
    #base_window.run_application()
