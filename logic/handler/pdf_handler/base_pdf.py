# Purpur Tentakel
# 06.03.2022
# VereinsManager / Base PDF

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph

from datetime import datetime
import os

from config import config_sheet as c
import debug

debug_str: str = "BasePDF"

base_pdf: "BasePDF"


class BasePDF:
    def __init__(self) -> None:
        self.dir_name: str = str()
        self.file_name: str = str()
        self.style_sheet: StyleSheet1 = StyleSheet1()

    def transform_path(self, path: str) -> None:
        now = datetime.now()
        if path:
            self.dir_name, file_name = os.path.split(path)
            parts = file_name.split(".")
            file_type = parts[-1]
            name: str = str()
            for _ in parts[:-1]:
                name += _
            self.file_name = f"{name}_{now.strftime(c.config.date_format['path'])}.{file_type}"
        else:
            self.dir_name = f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.dirs['member']}/\
                {c.config.dirs['export']}"
            self.file_name = f"Mitglieder_{now.strftime(c.config.date_format['path'])}.pdf"

    def create_dir(self) -> None:
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

    def paragraph(self, value) -> Paragraph:
        if isinstance(value, list):
            return Paragraph(str(value[0]) + ": " + str("---" if not value[1] else value[1]),
                             self.style_sheet["BodyText"])
        else:
            return Paragraph(str("---" if not value else value), self.style_sheet["BodyText"])

    @staticmethod
    def set_last_export_path(path: str) -> None:
        c.config.last_export_path = path


def create_base_pdf() -> None:
    global base_pdf
    base_pdf = BasePDF
