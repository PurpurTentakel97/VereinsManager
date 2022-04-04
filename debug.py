# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import json

from logic.handler import path_handler
from config import config_sheet as c
from datetime import datetime

is_debug: bool = True
is_debug_item: bool = False
debug_item: str = "MEMBERS WINDOW"
is_debug_keyword: bool = False
debug_keyword: str = "Phonenumbers"

is_info: bool = True
is_info_item: bool = False
info_item: str = "MEMBERS WINDOW"
is_info_keyword: bool = False
info_keyword: str = "Phonenumbers"

_error: list = list()


def debug(item, keyword, message) -> None:
    if is_debug:
        if is_debug_item and item == debug_item:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")
        elif is_debug_keyword and keyword == debug_keyword:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")
        elif not is_debug_keyword and not is_debug_item:
            print(f"+++++ Debug.LOG // {item} // {keyword} // {message} +++++")


def info(item, keyword, message) -> None:
    if is_info:
        if is_info_item and item == info_item:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")
        elif is_info_keyword and keyword == info_keyword:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")
        elif not is_info_keyword and not is_info_item:
            print(f"+++++ Info.LOG // {item} // {keyword} // {message} +++++")


def error(item, keyword, message) -> None:
    error: str = f"+++++ ERROR.LOG // {item} // {keyword} // {message} +++++"
    print(error)
    _add_error_to_list(item, keyword, message)


def _add_error_to_list(item, keyword, message) -> None:
    entry: dict = {
        "date": datetime.strftime(datetime.now(), c.config.date_format['long']),
        "type": "Error",
        "item": item,
        "keyword": keyword,
        "message": message,
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
