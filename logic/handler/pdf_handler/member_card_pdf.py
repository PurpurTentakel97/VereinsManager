# Purpur Tentakel
# 26.03.2022
# VereinsManager / Member Card PDF
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph

from logic.handler.pdf_handler.base_pdf import BasePDF
from logic.handler.data_handler import member_card_data_handler
from logic import validation as v
from config import exception_sheet as e, config_sheet as c

import debug

debug_str: str = "MemberCardPDF"

member_card_pdf: "MemberCardPDF"


class MemberCardPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, active: bool, ID: int) -> [None | str, bool]:
        result = self._validate_data(path=path, active=active, ID=ID)
        if isinstance(result, str):
            return result, False

        self._create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()
        data = member_card_data_handler.get_card_member_data(active=active, ID=ID)

        elements: list = [
            Paragraph(data['member_data']['name'],
                      self.style_sheet["Title"])
        ]

        if not data:
            self._mo_data_return(doc=doc, elements=elements)
            return None, False
        elements.extend(self._get_card_data(data=data))
        doc.build(elements)
        self.set_last_export_path(path=f"{self.dir_name}\{self.file_name}")

    def _create_basics(self, path: str) -> None:
        self.transform_path(path=path)
        self.create_dir()
        self.style_sheet = getSampleStyleSheet()

    def _get_doc(self) -> SimpleDocTemplate:
        return SimpleDocTemplate(f"{self.dir_name}/{self.file_name}", pagesize=A4, rightMargin=1.5 * cm,
                                 leftMargin=1.5 * cm,
                                 topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    def _mo_data_return(self, doc: SimpleDocTemplate, elements: list) -> None:
        elements.append(Paragraph(
            f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            self.style_sheet["BodyText"]))
        elements.append(Paragraph(
            f"Keine Daten vorhanden", self.style_sheet["BodyText"]))
        doc.build(elements)

    def _get_card_data(self, data: dict) -> list:
        elements: list = list()
        elements.extend(self._get_member_entries(data=data['member_data']))
        elements.extend(self._get_nexus_entries(data=data['phone'], type_='phone'))
        elements.extend(self._get_nexus_entries(data=data['mail'], type_='mail'))
        elements.extend(self._get_position_entries(data=data['position']))
        elements.append(
            Paragraph(f"Kommentar:<br/>{data['member_data']['comment_text']}", self.style_sheet['BodyText']))
        return elements

    def _get_member_entries(self, data: dict) -> list:
        data['comment_text'] = data['comment_text'].replace('\n', '<br/>')
        elements: list = [
            Paragraph(f"Name: {data['name']}", self.style_sheet['Normal']),
            Paragraph(f"Adresse:", self.style_sheet['BodyText']),
            Paragraph(f"{data['street']}", self.style_sheet['Normal']),
            Paragraph(f"{data['zip_code']}", self.style_sheet['Normal']),
            Paragraph(f"{data['city']}", self.style_sheet['Normal']),
            Paragraph(f"{data['maps']}", self.style_sheet['Normal']),
            Paragraph(f"Geburtstag: {data['birth_date']}, {data['age']}", self.style_sheet['BodyText']),
            Paragraph(f"Eintritt: {data['entry_date']}, {data['years']}", self.style_sheet['Normal']),
            Paragraph(f"Mitgliedsart: {data['membership_type']}", self.style_sheet['Normal']),
            Paragraph(f"Ehrenmitglied: {'Ja' if data['special_member'] else 'Nein'}", self.style_sheet['Normal']),
        ]
        return elements

    def _get_nexus_entries(self, data: list, type_: str) -> list:
        elements: list = list()
        match type_:
            case "phone":
                elements.append(Paragraph("Telefon:", self.style_sheet['BodyText']))
            case "mail":
                elements.append(Paragraph("E-Mail:", self.style_sheet['BodyText']))
        for type_, value in data:
            elements.append(Paragraph(f"{type_}: {value}", self.style_sheet['Normal']))

        if len(elements) == 1:
            elements.append(Paragraph("Keine Einträge vorhanden", self.style_sheet['Normal']))

        return elements

    def _get_position_entries(self, data: list) -> list:
        elements: list = [
            Paragraph("Positionen:", self.style_sheet['BodyText'])
        ]
        for entry in data:
            elements.append(Paragraph(entry, self.style_sheet['Normal']))

        return elements

    @staticmethod
    def _validate_data(path: str, active: bool, ID: int) -> None | str:
        try:
            v.must_positive_int(int_=ID)
            v.must_bool(bool_=active)
            v.must_str(str_=path, length=None)
        except e.InputError as error:
            debug.error(item=debug_str, keyword="_validate_data", message=f"Error = {error.message}")
            return error.message


def create_member_card_pdf() -> None:
    global member_card_pdf
    member_card_pdf = MemberCardPDF()
