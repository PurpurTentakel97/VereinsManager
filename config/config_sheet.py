# Purpur Tentakel
# 21.01.2022
# VereinsManager / Config

import json
import debug

debug_str: str = "Config"

config: "Config"


class Config:
    def __init__(self) -> None:
        self.config: dict = dict()

        # from config json
        self.date_format: dict = dict()
        self.raw_type_id: dict = dict()
        self.special_user: dict = dict()

        # easter egg
        self.user_name: str = "artimus83"
        self.easter_egg: str = str()

        # dirs
        self.save_dir: str = "saves"
        self.organisation_dir: str = "default_organisation"
        self.export_dir: str = "export"
        self.member_dir: str = "member"

        # file names
        self.database_name: str = f"default_database.vm"

        self._load_config()
        self._get_easter_egg_from_user_name()

    def _load_config(self) -> None:
        with open("config/config.json", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: dict = json_data["date_formats"]
        self.raw_type_id: dict = json_data["raw_type_id"]
        self.special_user: dict = json_data["special_user"]

    def _get_easter_egg_from_user_name(self) -> None:
        if self.user_name:
            for item in self.special_user.items():
                if self.user_name in item:
                    self.easter_egg = item[1]
                    return


def create_config():
    global config
    config = Config()
