# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum
import json
import debug

debug_str: str = "Config"

config: "Config"


class Config:
    def __init__(self) -> None:
        self.config: dict = dict()

        self.date_format: dict = dict()
        self.raw_type_id: dict = dict()
        self.special_user: dict = dict()

        self.save_dir: str = "saves"
        self.organisation_dir: str = "default_organisation"
        self.export_dir: str = "export"

        self.database_name: str = f"default_database.vm"

        self.load_config()

    def load_config(self) -> None:
        with open("config/config.json") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: dict = json_data["date_formats"]
        self.raw_type_id: dict = json_data["raw_type_id"]
        self.special_user: dict = json_data["special_user"]


def create_config():
    global config
    config = Config()
