# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import json
import traceback

from logic.handler.main_handler import path_handler
from config import config_sheet as c
from datetime import datetime

_error: list = list()


def debug(item, keyword, message) -> None:
    print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")


def info(item, keyword, error_) -> None:
    error_type_, error_value, error_traceback = error_
    error_traceback = traceback.extract_tb(error_traceback)
    print(f"+++++ INFO.LOG // {item} // {keyword} // Error: {error_type_} // {error_value} // {error_traceback} +++++")
    _add_error_to_list("info", item, keyword, str(error_type_), str(error_value), str(error_traceback))


def error(item, keyword, error_) -> None:
    error_type_, error_value, error_traceback = error_
    error_traceback = traceback.extract_tb(error_traceback)
    print(f"+++++ ERROR.LOG // {item} // {keyword} // Error: {error_type_} // {error_value} // {error_traceback} +++++")
    _add_error_to_list("error", item, keyword, str(error_type_), str(error_value), str(error_traceback))


def _add_error_to_list(print_type, item, keyword, error_type, value, traceback) -> None:
    entry: dict = {
        "date": datetime.strftime(datetime.now(), c.config.date_format['long']),
        "type": "Error",
        "item": item,
        "keyword": keyword,
        print_type: {
            "type": error_type,
            "value": value,
            "traceback": traceback,
        },
    }
    _error.append(entry)


def export_error() -> None:
    if _error:
        path_handler.create_default_path(type_="error_log")
        print(f"<<< export_error start >>>\n{_error}\n<<< export_error end >>>")
        with open(
                f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.dirs['error']}/error_log_{datetime.strftime(datetime.now(), c.config.date_format['long_save'])}.json",
                "w", encoding='UTF-8') as file:
            json.dump(_error, file, ensure_ascii=False, indent=4)
