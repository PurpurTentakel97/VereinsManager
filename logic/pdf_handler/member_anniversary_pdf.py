# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Anniversary PDF

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table

from datetime import datetime

from logic.handler import member_anniversary_data_handler
from logic.pdf_handler.base_pdf import BasePDF
from config import config_sheet as c
import debug

debug_str: str = "MemberAnniversaryPDF"

member_anniversary_pdf: "MemberAnniversaryPDF"


class MemberAnniversaryPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, year: int, active: bool = True) -> None:
        self._create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()
        data = self._get_data(year=year, active=active)

        elements: list = [
            Paragraph("Geburtstage / Jubiläen", self.style_sheet["Title"])
        ]

        if not data:
            self._no_data_return(elements=elements, doc=doc)
            return

        keys: list = [
            "b_day",
            "entry_day",
        ]

        elements = self._get_table_elements(data, elements, keys, year)
        doc.build(elements)
        self._set_last_export_path(path=f"{self.dir_name}\{self.file_name}")

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

    def _get_table_elements(self, data: dict, elements: list, keys: list, year: int) -> list:
        for key in keys:
            style_data: list = self._get_style_data()

            headers, elements = self._get_table_headers(elements, key)
            table_data: list = [
                headers,
            ]

            elements.append(
                Paragraph(
                    f"Stand: {str(year)}" if year else f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                    self.style_sheet["BodyText"]))

            if not data[key]:
                elements.append(Paragraph("Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
                continue

            for index, entry in enumerate(data[key], start=1):
                table_data.append(self._get_row_data(entry, index))

            table = Table(table_data, style=style_data, repeatRows=1)
            elements.append(table)
        return elements

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
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ("LINEAFTER", (0, 0), (0, -1), 3, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 3, colors.black),
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
