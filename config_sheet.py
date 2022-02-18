# Purpur Tentakel
# 21.01.2022
# VereinsManager / ENUM

from enum import Enum
import json
import debug

config: "Config"

sqlit_path: str = "saves/text.vm"


class Config:
    def __init__(self) -> None:
        self.config: dict = dict()

        self.date_format: dict = dict()
        self.special_user: dict = dict()

        self.load_config()

    def __str__(self) -> str:
        return "Config"

    def load_config(self) -> None:
        with open("config/config.json") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: dict = json_data["date_formats"]
        self.special_user: dict = json_data["special_user"]


def create_config():
    global config
    config = Config()
