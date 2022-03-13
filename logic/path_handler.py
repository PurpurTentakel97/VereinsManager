# Purpur Tentakel
# 06.03.2022
# VereinsManager / Path Handler

import os

from config import config_sheet as c


def create_default_path(type_: str) -> None:
    path: str = ""
    match type_:
        case "export":
            path = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}"

    if path:
        if not os.path.exists(path):
            os.mkdir(path)
