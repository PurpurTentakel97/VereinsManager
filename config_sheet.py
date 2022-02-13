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

        self.date_formats: dict = dict()
        self.type_table: dict = dict()
        self.log_table: dict = dict()

        self.member_table: dict = dict()
        self.member_phone_table: dict = dict()
        self.member_mail_table: dict = dict()
        self.member_position_table: dict = dict()

        self.load_config()

    def __str__(self) -> str:
        return "Config"

    def load_config(self) -> None:
        with open("config/sqlite_config.json") as json_file:
            json_data = json.load(json_file)

        self.config: dict = json_data
        debug.info(item=self, keyword="load config", message="config = " + str(self.config))

        self.date_formats: dict = json_data["date_formats"]
        debug.info(item=self, keyword="load config", message="date format = " + str(self.date_formats))
        self.log_table: dict = json_data["log"]
        debug.info(item=self, keyword="load config", message="log = " + str(self.log_table))
        self.type_table: dict = json_data["type_table"]
        debug.info(item=self, keyword="load config", message="type table = " + str(self.type_table))

        self.member_table: dict = json_data["member"]
        debug.info(item=self, keyword="load config", message="member  = " + str(self.member_table))
        self.member_phone_table: dict = json_data["member_phone"]
        debug.info(item=self, keyword="load config", message="member phone  = " + str(self.member_phone_table))
        self.member_mail_table: dict = json_data["member_mail"]
        debug.info(item=self, keyword="load config", message="member mail = " + str(self.member_mail_table))
        self.member_position_table: dict = json_data["member_position"]
        debug.info(item=self, keyword="load config",
                   message="member position = " + str(self.member_position_table))


def create_config():
    global config
    config = Config()
