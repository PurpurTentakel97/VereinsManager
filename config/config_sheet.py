# Purpur Tentakel
# 21.01.2022
# VereinsManager / Config

import os
import json

from helpers import validation as v
from logic.sqlite import select_handler as s_h

debug_str: str = "Config"

config: "Config"


class DateFormat:
    def __init__(self, formats: dict):
        self.short: str = formats['short']
        self.short_save: str = formats['short_save']
        self.short_length: int = formats['short_length']
        self.long: str = formats['long']
        self.long_save: str = formats['long_save']
        self.long_length: int = formats['long_length']
        self.delete_years: int = formats['delete_years']


class RawTypeID:
    def __init__(self, ids: dict):
        self.membership: int = ids['membership']
        self.mail: int = ids['mail']
        self.phone: int = ids['phone']
        self.position: int = ids['position']
        self.country: int = ids['country']
        self.schedule_entry: int = ids['schedule_entry']


class Constant:
    def __init__(self, constant: dict):
        self.hash_rounds: int = constant['hash_rounds']
        self.icon_height_table: int = constant['icon_height_table']
        self.icon_max_width_table: int = constant['icon_max_width_table']
        self.icon_height_letter: int = constant['icon_height_letter']
        self.icon_max_width_letter: int = constant['icon_max_width_letter']


class Directory:
    def __init__(self, directory: dict):
        self.save: str = directory['save']
        self.organisation: str = directory['organisation']
        self.export: str = directory['export']
        self.error: str = directory['error']
        self.member: str = directory['member']
        self.member_list: str = directory['member_list']
        self.member_anniversary: str = directory['member_anniversary']
        self.member_card: str = directory['member_card']
        self.member_letter: str = directory['member_letter']
        self.member_log: str = directory['member_log']
        self.location: str = directory['location']
        self.config: str = directory['config']


class File:
    def __init__(self, file: dict):
        self.database: str = file['database']
        self.icon: str = file['icon']
        self.default_icon: str = file['default_icon']
        self.member_card_pdf: str = file['member_card_pdf']
        self.member_table_pdf: str = file['member_table_pdf']
        self.member_letter_active_pdf: str = file['member_letter_active_pdf']
        self.member_letter_membership_pdf: str = file['member_letter_membership_pdf']
        self.member_log_pdf: str = file['member_log_pdf']
        self.member_anniversary_pdf: str = file['member_anniversary_pdf']
        self.location_pdf: str = file['location_pdf']


class User:
    def __init__(self, user: dict):
        self.ID: int = user['ID']
        self.default_user_id: int = user['default_user_id']
        self.name: str = user['name']
        self.easter_egg: str = user['easter_egg']
        self.special: dict = user['special']


class Letter:
    def __init__(self, letter: dict):
        self.title: dict = letter['title']
        self.text: dict = letter['text']
        self.info: dict = letter['info']
        self.keys: dict = letter['keys']


class Config:

    def __init__(self) -> None:
        self.config: dict = dict()

        self.date_format: DateFormat
        self.raw_type_id: RawTypeID
        self.constant: Constant
        self.directory: Directory
        self.file: File
        self.user: User
        self.letter: Letter

        self.last_export_path: str = str()
        self._load_config()

    def get_icon_path(self) -> str:
        return os.path.join(os.getcwd(), self.dirs.save, self.dirs.organisation, self.files.icon)

    def get_default_icon_path(self) -> str:
        return os.path.join(os.getcwd(), self.dirs.config, self.files.default_icon)

    def set_user(self, ID: int) -> None:
        v.must_positive_int(int_=ID)
        data = s_h.select_handler.get_names_of_user(active=True)

        self.user.ID = ID
        for ID, firstname, lastname in data:
            if not ID == self.user.ID:
                continue
            self._set_user_name(firstname=firstname, lastname=lastname)
            self._set_easter_egg_from_user_name(firstname=firstname)
            break

    def _set_user_name(self, firstname: str, lastname: str) -> None:
        if firstname and lastname:
            self.user.name = firstname + " " + lastname
        elif firstname:
            self.user.name = firstname
        elif lastname:
            self.user.name = lastname

    def _set_easter_egg_from_user_name(self, firstname: str) -> None:
        if firstname:
            for item in self.user.special.items():
                if firstname.lower() in item:
                    self.user.easter_egg = item[1]
                    return
            self.user.easter_egg = str()

    def _load_config(self) -> None:
        with open(os.path.join(os.getcwd(), "config", "config.json"), encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data

        self.date_format: DateFormat = DateFormat(json_data["date_format"])
        self.raw_type_id: RawTypeID = RawTypeID(json_data["raw_type_id"])
        self.constant: Constant = Constant(json_data["constant"])
        self.dirs: Directory = Directory(json_data["dirs"])
        self.files: File = File(json_data["files"])
        self.user: User = User(json_data["user"])
        self.letters: Letter = Letter(json_data['letter'])


def create_config() -> None:
    global config
    config = Config()
