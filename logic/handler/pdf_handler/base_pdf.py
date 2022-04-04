# Purpur Tentakel
# 06.03.2022
# VereinsManager / Base PDF

from PIL import Image as image
from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Image
from reportlab.lib.units import cm

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

    def get_icon(self) -> Image:
        width, height = self._get_icon_ratio()
        icon: Image = Image(c.config.get_icon_path(), width=width * cm, height=height * cm)
        icon.hAlign = 'RIGHT'
        return icon

    def _get_icon_ratio(self) -> tuple:
        image_ = image.open(f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.files['icon']}")
        width, height = image_.size
        if width == height:
            return c.config.constant['icon_height'], c.config.constant['icon_height']
        ratio = width / height
        width_ratio = c.config.constant['icon_height'] * ratio
        height_ratio = c.config.constant['icon_height']
        if width_ratio > c.config.constant['icon_max_width']:
            width_ratio, height_ratio = self._transform_max_width(ratio=ratio)
        return width_ratio, height_ratio

    @staticmethod
    def _transform_max_width(ratio: float) -> tuple:
        width = c.config.constant['icon_max_width']
        height = width / ratio
        return width, height

    @staticmethod
    def is_icon() -> bool:
        if os.path.exists(c.config.get_icon_path()):
            return True
        return False

    @staticmethod
    def set_last_export_path(path: str) -> None:
        c.config.last_export_path = path


def create_base_pdf() -> None:
    global base_pdf
    base_pdf = BasePDF
