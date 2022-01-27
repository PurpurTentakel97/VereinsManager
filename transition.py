# Purpur Tentakel
# 21.01.2022
# VereinsManager / Transition
import main
from ui import base_window, main_window, enum_sheet
from enum import Enum


def create_application():
    base_window.create_application()


def run_application():
    base_window.run_application()


def create_main_window():
    main_window.create_main_window()


def set_window_massage(massage: str):
    print(massage)


def put_types_in_ui(types: dict):
    types: dict = types
    enum_sheet.membership_type = types["membership_type"]
    enum_sheet.position_types = types["position_type"]
    enum_sheet.uniform_types = types["uniform_type"]
    enum_sheet.performance_types = types["performance_type"]
    enum_sheet.instrument_types = types["instrument_type"]
    enum_sheet.phone_number_types = types["phone_number_type"]
    enum_sheet.mail_types = types["mail_type"]


def put_non_types_in_ui(non_types: dict):
    non_types: dict = non_types
    enum_sheet.locations = non_types["location"]
    enum_sheet.special_user = non_types["special_user"]


def save_data(data: list[dict], table):
    main.save_data(data=data, table=table)


def load_data(table) -> list:
    return main.load_data(table=table)