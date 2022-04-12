# Purpur Tentakel
# 21.01.2022
# VereinsManager / Config

import json
import os
from helper import validation as v
from logic.sqlite import select_handler as s_h

debug_str: str = "Config"

config: "Config"


class Config:
    def __init__(self) -> None:
        self.config: dict = dict()

        self.date_format: dict = dict()
        self.raw_type_id: dict = dict()
        self.constant: dict = dict()
        self.dirs: dict = dict()
        self.files: dict = dict()
        self.user: dict = dict()
        self.spacer: dict = dict()
        self.letters: dict = dict()

        self.last_export_path: str = str()
        self._load_config()

    def _load_config(self) -> None:
        print(os.getcwd())
        with open(os.path.join(os.getcwd(), "config", "config.json"), encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: dict = json_data["date_format"]
        self.raw_type_id: dict = json_data["raw_type_id"]
        self.constant: dict = json_data["constant"]
        self.dirs: dict = json_data["dirs"]
        self.files: dict = json_data["files"]
        self.user: dict = json_data["user"]
        self.spacer: dict = json_data['spacer']
        self.letters: dict = json_data['letters']

    def set_user(self, ID: int) -> [str | None, bool]:
        v.must_positive_int(int_=ID)
        data = s_h.select_handler.get_names_of_user(active=True)

        self.user['ID'] = ID
        for ID, firstname, lastname in data:
            if not ID == self.user['ID']:
                continue
            self._set_user_name(firstname=firstname, lastname=lastname)
            self._set_easter_egg_from_user_name(firstname=firstname)
            break

    def _set_user_name(self, firstname: str, lastname: str) -> None:
        if firstname and lastname:
            self.user['name'] = firstname + " " + lastname
        elif firstname:
            self.user['name'] = firstname
        elif lastname:
            self.user['name'] = lastname

    def _set_easter_egg_from_user_name(self, firstname: str) -> None:
        if firstname:
            for item in self.user['special'].items():
                if firstname.lower() in item:
                    self.user['easter_egg'] = item[1]
                    return
            self.user['easter_egg'] = str()

    def get_icon_path(self) -> str:
        return os.path.join(os.getcwd(), self.dirs['save'], self.dirs['organisation'], self.files['icon'])

    def get_default_icon_path(self) -> str:
        return os.path.join(os.getcwd(), self.dirs['config'], self.files['default_icon'])


def create_config():
    global config
    config = Config()
