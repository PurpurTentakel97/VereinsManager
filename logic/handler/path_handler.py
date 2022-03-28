# Purpur Tentakel
# 06.03.2022
# VereinsManager / Path Handler

import os

from config import config_sheet as c


def create_default_path(type_: str) -> None:
    path: str = ""
    match type_:
        case "member_list":
            path = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/{c.config.member_list}"
        case "member_anniversary":
            path = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/{c.config.member_anniversary}"
        case "member_card":
            path = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/{c.config.member_card}"
        case "member_letter":
            path = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/{c.config.member_letter}"

    if path:
        if not os.path.exists(path):
            os.makedirs(path)
