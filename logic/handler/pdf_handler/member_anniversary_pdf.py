# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Anniversary PDF

import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer

from logic.handler.data_handler import member_anniversary_data_handler
from logic.handler.pdf_handler.base_pdf import BasePDF, NumberedCanvas
from config import config_sheet as c, exception_sheet as e
import debug

debug_str: str = "MemberAnniversaryPDF"
member_anniversary_pdf: "MemberAnniversaryPDF"


class MemberAnniversaryPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, year: int, active: bool = True) -> [None | str, bool]:
        self._create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()
        data = self._get_data(year=year, active=active)

        elements: list = list()
        if self.is_icon():
            elements.append(self.get_icon())
        if year:
            elements.append(Paragraph(f"Stand: {year}", self.custom_styles["CustomBodyTextRight"]))
        else:
            elements.append(Paragraph(f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                      self.custom_styles["CustomBodyTextRight"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.5'] * cm))
        elements.extend(self._get_header())
        elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))

        if not data:
            self._no_data_return(elements=elements, doc=doc)
            return

        elements = self._get_table_elements(data, elements)
        elements = elements[:-1]
        try:
            doc.build(elements, canvasmaker=NumberedCanvas)
            self.set_last_export_path(path=f"{self.dir_name}\{self.file_name}")
            return None, True
        except PermissionError:
            debug.info(item=debug_str, keyword="create_pdf", error_=sys.exc_info())
            return e.PermissionException(self.file_name).message, False

    def _no_data_return(self, elements: list, doc: SimpleDocTemplate) -> None:
        elements.append(Paragraph(
            f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            self.style_sheet["BodyText"]))
        elements.append(Paragraph(
            f"Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
        doc.build(elements)

    def _create_basics(self, path: str) -> None:
        self.transform_path(path=path)
        self.create_dir()
        self.style_sheet = getSampleStyleSheet()

    def _get_table_elements(self, data: dict, elements: list) -> list:
        keys: list = [
            "b_day",
            "entry_day",
        ]
        for key in keys:
            style_data: list = self._get_style_data()

            headers, elements = self._get_table_headers(elements, key)

            if not data[key]:
                elements.append(Paragraph("Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
                elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))
                continue

            table_data: list = [
                headers,
            ]
            for index, entry in enumerate(data[key], start=1):
                table_data.append(self._get_row_data(entry, index))

            table = Table(table_data, style=style_data, repeatRows=1,
                          colWidths=[self._get_first_column_with(data[key]) * cm] + [None] * 3)
            elements.append(table)
            elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))
        return elements

    @staticmethod
    def _get_first_column_with(data) -> float:
        length = len(str(len(data)))
        default_width = 1
        character_width = 0.2
        return default_width + character_width * length

    def _get_table_headers(self, elements: list, key: str) -> tuple:
        headers: list = list()
        match key:
            case "b_day":
                elements.append(Paragraph("Geburtstage", self.style_sheet["Heading3"]))
                headers = [
                    "",
                    "Name",
                    "Geburtstag",
                    "Jahre",
                ]
            case "entry_day":
                elements.append(Paragraph("Jubiläen", self.style_sheet["Heading3"]))
                headers = [
                    "",
                    "Name",
                    "Jubiläum",
                    "Jahre",
                ]
        return headers, elements

    def _get_doc(self) -> SimpleDocTemplate:
        return SimpleDocTemplate(f"{self.dir_name}/{self.file_name}", pagesize=A4, rightMargin=1.5 * cm,
                                 leftMargin=1.5 * cm,
                                 topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    def _get_header(self) -> list:
        return [Paragraph("Geburtstage / Jubiläen", self.style_sheet["Title"])]

    @staticmethod
    def _get_data(year: int | None, active: bool) -> dict:
        if year:
            data, _ = member_anniversary_data_handler.get_anniversary_member_data(type_="other", active=active,
                                                                                  year=year)
        else:
            data, _ = member_anniversary_data_handler.get_anniversary_member_data(type_="current", active=active)

        return data

    @staticmethod
    def _get_style_data() -> list:
        return [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]

    @staticmethod
    def _get_row_data(entry: dict, index: int) -> list:
        return [
            str(index),
            [Paragraph(f"{entry['firstname']} {entry['lastname']}")],
            entry['date'],
            str(entry['year']),
        ]


def create_member_anniversary_pdf() -> None:
    global member_anniversary_pdf
    member_anniversary_pdf = MemberAnniversaryPDF()
