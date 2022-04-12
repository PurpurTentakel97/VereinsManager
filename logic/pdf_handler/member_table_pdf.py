# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Table PDF

import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from logic.data_handler import member_table_data_handler
from logic.pdf_handler.base_pdf import BasePDF, NumberedCanvas
from logic.main_handler import organisation_handler
from logic.sqlite import select_handler as s_h
from config import config_sheet as c, exception_sheet as e
import debug

debug_str: str = "MemberTablePDF"

member_table_pdf: "MemberTablePDF"


class MemberTablePDF(BasePDF):
    def __init__(self) -> None:
        super().__init__()

    def create_pdf(self, path: str, active: bool) -> [str | None, bool]:
        self._create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()
        data = self._get_data(active)
        type_ids = self._get_type_ids()

        elements: list = list()

        elements.extend(self._get_header())

        if not data:
            self._no_data_return(doc, elements)
            return

        elements.extend(self._get_table_data(data, type_ids))
        elements = elements[:-1]
        try:
            doc.build(elements, canvasmaker=NumberedCanvas)
            self.set_last_export_path(path=f"{self.dir_name}\{self.file_name}")
            return None, True
        except PermissionError:
            debug.info(item=debug_str, keyword=f"create_pdf", error_=sys.exc_info())
            return e.PermissionException(self.file_name).message, False

    def _create_basics(self, path: str) -> None:
        self.transform_path(path=path)
        self.create_dir()
        self.style_sheet = getSampleStyleSheet()

    def _get_doc(self) -> SimpleDocTemplate:
        return SimpleDocTemplate(f"{self.dir_name}/{self.file_name}", pagesize=A4, rightMargin=1.5 * cm,
                                 leftMargin=1.5 * cm,
                                 topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    def _no_data_return(self, doc: SimpleDocTemplate, elements: list):
        elements.append(Paragraph(
            f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            self.style_sheet["BodyText"]))
        elements.append(Paragraph(
            f"Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
        doc.build(elements)

    def _get_table_data(self, data: dict, type_ids: list) -> list:
        elements: list = list()
        for type_id, type_ in type_ids:
            all_members: list = data[type_id]
            elements.append(Paragraph(f"{type_}", self.style_sheet["Heading3"]))
            elements.append(Spacer(width=0, height=c.config.spacer['0.1'] * cm))
            if not all_members:
                elements.append(Paragraph(
                    f"Keine Mitglieder vorhanden.",
                    self.style_sheet["BodyText"]))
                elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))
                continue

            table_data: list = self._get_default_table_data()
            style_data: list = self._get_default_style_data()
            table, style = self._get_single_table_data(all_members)
            table_data.extend(table)
            style_data.extend(style)
            first_column_width: float = self._get_first_column_with(data=table)

            table = Table(table_data, style=style_data, repeatRows=1,
                          colWidths=[first_column_width * cm] + [None])
            elements.append(table)
            elements.append(Spacer(width=0, height=c.config.spacer['0.1'] * cm))
            elements.append(Paragraph("(E) = Ehrenmitglied"))
            elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))
        return elements

    def _get_single_table_data(self, all_members: list) -> tuple:
        table_data: list = list()
        style_data: list = list()
        for index, member in enumerate(all_members, start=1):
            member_data = member["member"]
            phone_data = member["phone"]
            mail_data = member["mail"]
            row_data: list = [
                str(index) if not member_data["special_member"] else f"{str(index)} (E)",
                [Paragraph(
                    f"{member_data['first_name']} {member_data['last_name']}<br/>{member_data['street']}<br/>{member_data['zip_code']} {member_data['city']}<br/>{member_data['country']}")],
                [Paragraph(f"Alter {member_data['age']}<br/>{member_data['b_date']}"), Spacer(0, 0.3*cm),
                 Paragraph(f"Alter {member_data['membership_years']}<br/>{member_data['entry_date']}")],
                [self.paragraph(x) for x in phone_data],
                [self.paragraph(x) for x in mail_data],
            ]
            table_data.append(row_data)

            if member_data["special_member"]:
                style_data.append(("BACKGROUND", (0, index), (0, index), colors.lightgrey))
            if member_data["age"] is not None and (
                    int(member_data["age"]) % 10 == 0 or int(member_data["age"]) == 18):
                style_data.append(("BACKGROUND", (2, index), (2, index), colors.lightgrey))
            if member_data["membership_years"] is not None and int(member_data["membership_years"]) % 5 == 0:
                style_data.append(("BACKGROUND", (2, index), (2, index), colors.lightgrey))
        return table_data, style_data

    def _get_header(self) -> list:
        elements: list = list()
        if self.is_icon():
            elements.append(self.get_icon(type_="table"))
        elements.append(Paragraph(f"Stand:{datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                  self.custom_styles["CustomBodyTextRight"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.5'] * cm))

        organisation_data, _ = organisation_handler.get_organisation_data()
        if organisation_data['name']:
            elements.append(Paragraph(organisation_data['name'], self.style_sheet["Title"]))
        elements.append(Paragraph("Mitglieder", self.style_sheet["Title"]))
        elements.append(Spacer(width=0, height=c.config.spacer['1'] * cm))
        return elements

    @staticmethod
    def _get_first_column_with(data) -> float:
        length = len(str(len(data)))
        default_width = 1
        character_width = 0.2
        return default_width + character_width * length

    @staticmethod
    def _get_data(active: bool) -> dict:
        data, _ = member_table_data_handler.get_member_table_data(active=active)
        return data

    @staticmethod
    def _get_type_ids() -> list:
        type_ids = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"], active=True)
        return [[x[0], x[1]] for x in type_ids]

    @staticmethod
    def _get_default_table_data() -> list:
        return [[
            "",
            "Name / Adresse",
            "Alter / Eintritt",
            "Telefon",
            "Mail",
        ]]

    @staticmethod
    def _get_default_style_data() -> list:
        return [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]


def create_member_table_pdf() -> None:
    global member_table_pdf
    member_table_pdf = MemberTablePDF()
