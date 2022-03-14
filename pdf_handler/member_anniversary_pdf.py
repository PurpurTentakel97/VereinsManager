# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Anniversary PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table

from datetime import datetime

import logic.anniversary_handler
from pdf_handler.base_pdf import BasePDF
from config import config_sheet as c

import debug

debug_str: str = "MemberAnniversaryPDF"

member_anniversary_pdf: "MemberAnniversaryPDF"


class MemberAnniversaryPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, year: int, active: bool = True) -> None or str:
        self.transform_path(path=path)
        self.create_dir()

        self.style_sheet = getSampleStyleSheet()
        doc = SimpleDocTemplate(f"{self.dir_name}/{self.file_name}", pagesize=A4, rightMargin=1.5 * cm,
                                leftMargin=1.5 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.5 * cm)

        if year:
            data = logic.anniversary_handler.get_anniversary_member_data(type_="other", active=active, year=year)
        else:
            data = logic.anniversary_handler.get_anniversary_member_data(type_="current", active=active)
        if isinstance(data, str):
            return data

        elements: list = [
            Paragraph("Geburtstage / Jubiläen", self.style_sheet["Title"])
        ]

        if not data:
            elements.append(Paragraph(
                f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                self.style_sheet["BodyText"]))
            elements.append(Paragraph(
                f"Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
            doc.build(elements)
            return

        keys: list = [
            "b_day",
            "entry_day",
        ]
        for key in keys:
            style_data: list = [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 2, colors.black),
                ("LINEAFTER", (0, 0), (0, -1), 3, colors.black),
                ("LINEBELOW", (0, 0), (-1, 0), 3, colors.black),
            ]

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
            elements.append(
                Paragraph(
                    f"Stand: {str(year)}" if year else f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                    self.style_sheet["BodyText"]))
            if not data[key]:
                elements.append(Paragraph("Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
                continue
            table_data: list = [
                headers,
            ]
            for index, entry in enumerate(data[key], start=1):
                row_data: list = [
                    str(index),
                    [Paragraph(f"{entry['firstname']} {entry['lastname']}")],
                    entry['date'],
                    str(entry['year']),
                ]
                table_data.append(row_data)
            table = Table(table_data, style=style_data, repeatRows=1)
            elements.append(table)
        doc.build(elements)


def create_member_anniversary_pdf() -> None:
    global member_anniversary_pdf
    member_anniversary_pdf = MemberAnniversaryPDF()
