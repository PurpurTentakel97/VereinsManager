# Purpur Tentakel
# 06.03.2022
# VereinsManager / Path Handler

import os

from config import config_sheet as c


def create_default_path(type_: str) -> None:
    path: str = _get_default_path(type_=type_)

    if path:
        if not os.path.exists(path):
            os.makedirs(path)


def _get_default_path(type_: str) -> str:
    path: str = ""
    match type_:
        case "member_list":
            path: str = os.path.join(
                os.getcwd(),
                c.config.dirs['save'],
                c.config.dirs['organisation'],
                c.config.dirs['export'],
                c.config.dirs['member'],
                c.config.dirs['member_list'],
            )
        case "member_anniversary":
            path: str = os.path.join(
                os.getcwd(),
                c.config.dirs['save'],
                c.config.dirs['organisation'],
                c.config.dirs['export'],
                c.config.dirs['member'],
                c.config.dirs['member_anniversary'],
            )
        case "member_card":
            path: str = os.path.join(
                os.getcwd(),
                c.config.dirs['save'],
                c.config.dirs['organisation'],
                c.config.dirs['export'],
                c.config.dirs['member'],
                c.config.dirs['member_card'],
            )
        case "member_letter":

            path: str = os.path.join(
                os.getcwd(),
                c.config.dirs['save'],
                c.config.dirs['organisation'],
                c.config.dirs['export'],
                c.config.dirs['member'],
                c.config.dirs['member_letter'],
            )
        case "error_log":
            path: str = os.path.join(
                os.getcwd(),
                c.config.dirs['save'],
                c.config.dirs['organisation'],
                c.config.dirs['error'],
            )

    return path
