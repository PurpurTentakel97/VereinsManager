# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

from os import path, mkdir
import json

from logic import transition


def _get_ui_types() -> dict:
    if not path.exists("types"):
        mkdir("types")
    with open("types/type.json", "r", encoding="utf=8") as f:
        data = json.load(f)
        return data


def _get_ui_non_types() -> dict:
    if not path.exists("types"):
        mkdir("types")
    with open("types/non_type.json", "r", encoding="utf=8") as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    transition.put_types_in_ui(types=_get_ui_types())
    transition.put_non_types_in_ui(non_types=_get_ui_non_types())
    transition.create_application()
    transition.create_main_window()
    transition.run_application()
