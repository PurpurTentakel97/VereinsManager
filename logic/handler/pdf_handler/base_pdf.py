# Purpur Tentakel
# 06.03.2022
# VereinsManager / Base PDF
import sys

from PIL import Image as image, UnidentifiedImageError
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Image
from reportlab.lib.units import cm

from datetime import datetime
import os

from config import config_sheet as c, exception_sheet as e
import debug

debug_str: str = "BasePDF"

base_pdf: "BasePDF"


class BasePDF:
    def __init__(self) -> None:
        self.dir_name: str = str()
        self.file_name: str = str()
        self.styles = getSampleStyleSheet()
        self.custom_styles: dict = dict()
        self._add_styles()

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
                             self.styles["BodyText"])
        else:
            return Paragraph(str("---" if not value else value), self.styles["BodyText"])

    def get_icon(self, type_: str) -> Image:
        try:
            width, height = self._get_icon_ratio(type_=type_)
            icon: Image = Image(c.config.get_icon_path(), width=width * cm, height=height * cm)
            icon.hAlign = 'RIGHT'
            return icon
        except e.CaseException:
            debug.info(item=debug_str, keyword="get_icon", error_=sys.exc_info())

    def _get_icon_ratio(self, type_: str) -> tuple:
        image_ = image.open(f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.files['icon']}")
        width, height = image_.size
        return self._transform_width_height(type_=type_, width=width, height=height)

    def _add_styles(self) -> None:
        self.custom_styles['CustomTitle'] = (ParagraphStyle(name='CustomTitle', parent=self.styles['Title'],
                                                            fontSize=35))
        self.custom_styles['CustomHeading'] = (ParagraphStyle(name='CustomHeading', parent=self.styles['Heading1'],
                                                              fontSize=20))
        self.custom_styles['CustomBodyTextRight'] = (ParagraphStyle(name='CustomBodyTextRight',
                                                                    parent=self.styles['BodyText'], fontSize=10,
                                                                    alignment=TA_RIGHT))

    @staticmethod
    def _transform_width_height(type_: str, width: int, height: int) -> tuple:
        match type_:
            case "letter":
                icon_height = c.config.constant['icon_height_letter']
                icon_max_width = c.config.constant['icon_max_width_letter']
            case "table":
                icon_height = c.config.constant['icon_height_table']
                icon_max_width = c.config.constant['icon_max_width_table']
            case _:
                raise e.CaseException(type_)

        if width == height:
            return icon_height, icon_height

        ratio = width / height
        width_ratio = icon_height * ratio
        height_ratio = icon_height

        if width_ratio < icon_max_width:
            return width_ratio, height_ratio

        width_ratio = icon_max_width
        height_ratio = width_ratio / ratio
        return width_ratio, height_ratio

    @staticmethod
    def is_icon() -> bool:
        if os.path.exists(c.config.get_icon_path()):
            try:
                _ = image.open(f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.files['icon']}")
                return True
            except UnidentifiedImageError:
                debug.info(item=debug_str, keyword="is_icon", error_=sys.exc_info())
        return False

    @staticmethod
    def set_last_export_path(path: str) -> None:
        c.config.last_export_path = path


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(20 * cm, 2 * cm,
                             "Seite %d von %d" % (self._pageNumber, page_count))


def create_base_pdf() -> None:
    global base_pdf
    base_pdf = BasePDF
