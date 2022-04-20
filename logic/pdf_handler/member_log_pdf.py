# Purpur Tentakel
# 13.04.2022
# VereinsManager / Log Handler

from _datetime import datetime

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.units import cm

from helpers import helper
from logic.pdf_handler.base_pdf import BasePDF
from logic.data_handler import member_log_data_handler
from logic.main_handler import organisation_handler, member_handler
from config import config_sheet as c
import debug

debug_str: str = "Log Handler"

member_log_pdf: "MemberLogPDF"


class MemberLogPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, ID: int, active: bool) -> tuple[None | str, bool]:
        self.create_basics(path=path)
        doc: SimpleDocTemplate = self._get_doc()
        data: list = self._get_data(target_id=ID)

        elements: list = list()

        elements.extend(self._get_header(ID=ID, active=active))

        if not data:
            return self._no_data_return(doc=doc, elements=elements)

        elements.extend(self._get_table(data=data))

        return self._export(doc=doc, elements=elements)

    @staticmethod
    def _get_data(target_id: int) -> list:
        data = member_log_data_handler.get_log_member_data(target_id=target_id)
        return data

    def _get_header(self, ID: int, active: bool) -> list:
        elements: list = list()
        if self._is_icon():
            elements.append(self._get_icon('table'))
        elements.append(Paragraph(f"Stand:{datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                  self.custom_styles["CustomBodyTextRight"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.5'] * cm))

        organisation_data, _ = organisation_handler.get_organisation_data()
        if organisation_data['name']:
            elements.append(Paragraph(organisation_data['name'], self.style_sheet["Title"]))
        elements.append(Paragraph(self._get_member_name(ID=ID, active=active), self.style_sheet["Title"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.3'] * cm))
        return elements

    @staticmethod
    def _get_member_name(ID: int, active: bool) -> str:
        member_data, _ = member_handler.get_member_data(ID=ID, active=active)
        member_data: dict = member_data['member_data']

        name = helper.combine_strings(strings=(member_data['first_name'], member_data['last_name']))
        return name

    def _get_table(self, data: list) -> list:
        table_data: list = self._get_table_data(data=data)
        style_data: list = self._get_default_style_data()

        table: Table = Table(table_data, style=style_data, repeatRows=1)
        return [
            Paragraph("Log", self.custom_styles['CustomCenterHeading3']),
            Spacer(width=0, height=c.config.spacer['0.1'] * cm),
            table,
        ]

    def _get_table_data(self, data: list) -> list:
        table_data: list = self._get_default_table_data()

        for row_id, entry in enumerate(data, start=1):
            keys: tuple = (
                "log_date",
                "display_name",
                "old_data",
                "new_data",
            )
            row: list = [str(row_id)]
            for key in keys:
                row.append(entry[key])
            table_data.append(row)

        return table_data

    @staticmethod
    def _get_default_table_data() -> list:
        return [[
            "",
            "Datum",
            "Art",
            "Alte Daten",
            "Neue Daten",
        ]]

    @staticmethod
    def _get_default_style_data() -> list:
        return [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]

    def _no_data_return(self, doc: SimpleDocTemplate, elements: list) -> tuple[str | None, bool]:
        elements.append(Paragraph("Keine Daten vorhanden", self.style_sheet['BodyText']))
        return self._export(doc=doc, elements=elements)


def create() -> None:
    global member_log_pdf
    member_log_pdf = MemberLogPDF()
