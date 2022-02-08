# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

from sqlite import global_handler as main_handler

from ui import base_window, main_window


# main
if __name__ == "__main__":
    main_handler.create_database_classes()
    main_handler.create_all_tables()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()
