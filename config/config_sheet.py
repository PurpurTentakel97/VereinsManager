# Purpur Tentakel
# 21.01.2022
# VereinsManager / Config

import json

from logic import validation as v
from sqlite import select_handler as s_h
import debug

debug_str: str = "Config"

config: "Config"


class Config:
    def __init__(self) -> None:
        self.config: dict = dict()

        # from config json
        self.date_format: dict = dict()
        self.raw_type_id: dict = dict()
        self.default_user_id: dict = dict()
        self.special_user: dict = dict()

        # hashes
        self.hash_round = 12

        # dirs
        self.save_dir: str = "saves"
        self.organisation_dir: str = "default_organisation"
        self.export_dir: str = "export"

        self.member_dir: str = "member"
        self.member_list: str = "member_list"
        self.member_anniversary: str = "member_anniversary"
        self.member_card: str = "member_card"
        self.member_letter: str = "member_letter"

        self.last_export_path: str = str()

        # file names
        self.database_name: str = f"default_database.vm"

        # user
        self.user_id: int = int()
        self.user_name: str = str()
        self.easter_egg: str = str()

        self._load_config()
        self._get_easter_egg_from_user_name()

    def set_user(self, ID: int) -> [str | None, bool]:
        v.validation.must_positive_int(int_=ID)
        data = s_h.select_handler.get_names_of_user(active=True)

        self.user_id = ID
        for ID, firstname, lastname in data:
            if not ID == self.user_id:
                continue
            self._set_user_name(firstname=firstname, lastname=lastname)
            break

        self._get_easter_egg_from_user_name()

    def _set_user_name(self, firstname: str, lastname: str) -> None:
        if firstname and lastname:
            self.user_name = firstname + " " + lastname
        elif firstname:
            self.user_name = firstname
        elif lastname:
            self.user_name = lastname

    def _load_config(self) -> None:
        with open("config/config.json", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: dict = json_data["date_format"]
        self.raw_type_id: dict = json_data["raw_type_id"]
        self.default_user_id: dict = json_data["default_user_id"]
        self.special_user: dict = json_data["special_user"]

    def _get_easter_egg_from_user_name(self) -> None:
        if self.user_name:
            for item in self.special_user.items():
                if self.user_name.lower() in item:
                    self.easter_egg = item[1]
                    return
            self.easter_egg = str()


def create_config():
    global config
    config = Config()
