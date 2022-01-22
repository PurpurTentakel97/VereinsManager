# Purpur Tentakel
# 21.01.2022
# VereinsManager / Transition

from ui import base_window, main_window


def create_application():
    base_window.create_application()


def run_application():
    base_window.run_application()


def create_main_window():
    main_window.create_main_window()


def set_window_massage(massage: str):
    print(massage)
