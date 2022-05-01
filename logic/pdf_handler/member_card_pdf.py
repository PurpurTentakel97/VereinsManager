# Purpur Tentakel
# 26.03.2022
# VereinsManager / Member Card PDF

import sys
from datetime import datetime

from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table

from helpers import validation
from logic.main_handler import organisation_handler
from logic.data_handler import member_card_data_handler
from config import exception_sheet as e, config_sheet as c
from logic.pdf_handler.base_pdf import BasePDF

import debug

row_height: float = 0.4 * cm
column_width: float = 2.9 * cm
empty: str = "  "

debug_str: str = "MemberCardPDF"

member_card_pdf: "MemberCardPDF"


class MemberCardPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, active: bool, ID: int) -> tuple[None | str, bool]:
        result = self._check_data(path=path, active=active, ID=ID)
        if isinstance(result, str):
            return result, False

        self.create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()
        data, valid = member_card_data_handler.get_card_member_data(active=active, ID=ID)
        if not valid:
            return data, valid
        self._set_column_width(data=data)

        elements: list = list()
        header, valid = self._get_header(data=data)
        if not valid:
            return header, valid
        elements.extend(header)

        if not data:
            return self._mo_data_return(doc=doc, elements=elements)

        elements.extend(self._get_card_data(data=data))

        return self._export(doc=doc, elements=elements)

    @staticmethod
    def _get_longest_value(data: dict) -> int:
        longest: int = 0
        keys: list = [
            "mail",
            "phone",
        ]
        for key in keys:
            for value_, _ in data[key]:
                length = len(value_)
                if length > longest:
                    longest = length

        return longest

    def _get_card_data(self, data: dict) -> list:
        elements: list = list()
        elements.extend(self._get_member_entries(input_=data['member_data']))
        elements.extend(self._get_nexus_entries(input_=data['phone'], type_='phone'))
        elements.extend(self._get_nexus_entries(input_=data['mail'], type_='mail'))
        elements.extend(self._get_position_entries(input_=data['position']))
        elements.extend(self._get_single_table(data=("<b>Kommentar:</b>", f"{data['member_data']['comment_text']}"),
                                               comment_break_count=True))
        return elements

    def _get_member_entries(self, input_: dict) -> list:
        input_['comment_text'] = input_['comment_text'].replace('\n', '<br/>')
        elements: list = list()
        data: tuple = (
            "<b>Adresse:</b>",
            f"{input_['name']}",
            f"{input_['street']}",
            f"{input_['zip_code']} {input_['city']}",
            f"{input_['country']}",
            f"{input_['maps']}",
        )
        elements.extend(self._get_single_table(data=data))

        data: tuple = (
            ["<b>Geburtstag:</b>", f"{input_['birth_date']}, {input_['age']}"],
            ["<b>Eintritt:</b>", f"{input_['entry_date']}, {input_['years']}"],
            ["<b>Mitgliedsart:</b>", f"{input_['membership_type']}"],
            ["<b>Beitrag:</b>", f"{input_['membership_type_extra_value']}"],
            ["<b>Ehrenmitglied:</b>", f"{'Ja' if input_['special_member'] else 'Nein'}"],
        )
        elements.extend(self._get_double_table(data=data))

        return elements

    def _get_nexus_entries(self, input_: list, type_: str) -> list:
        data: list = list()
        match type_:
            case "phone":
                data.append(["<b>Telefon:</b>", empty])
            case "mail":
                data.append(["<b>E-Mail:</b>", empty])

        for type_, value in input_:
            data.append([f"{type_}:", f"{value}"])

        if len(data) == 1:
            data.append(["Keine Angaben vorhanden", empty])

        return self._get_double_table(data=tuple(data))

    def _get_position_entries(self, input_: list) -> list:
        data: list = [
            "<b>Positionen:</b>",
        ]

        for entry in input_:
            data.append(entry)

        return self._get_single_table(data=tuple(data))

    def _get_single_table(self, data: tuple, comment_break_count: bool = False) -> list:
        table_data: list = list()
        for _1 in data:
            table_data.append([self._paragraph(_1)])

        if comment_break_count:
            row_count = self._get_comment_break_count(comment=data[1])
            return [
                Table(table_data, rowHeights=[row_height] + [row_height * row_count]),
                Spacer(0, c.config.spacer['0.5'] * cm),
            ]

        return [
            Table(table_data, rowHeights=[row_height] * len(data)),
            Spacer(0, c.config.spacer['0.5'] * cm),
        ]

    @staticmethod
    def _get_comment_break_count(comment: str) -> float:
        count: int = 0
        for character in comment:
            if character == "<":
                count += 1
        return (count + 1) * 1.12

    def _get_double_table(self, data: tuple) -> list:
        table_data: list = list()
        for _1, _2 in data:
            table_data.append([self._paragraph(_1), self._paragraph(_2)])
        return [
            Table(table_data, colWidths=[column_width] + [None], rowHeights=[row_height] * len(data)),
            Spacer(0, c.config.spacer['0.5'] * cm),
        ]

    def _get_header(self, data: dict) -> tuple[list | str, bool]:
        elements: list = list()

        if self._is_icon():
            elements.append(self._get_icon(type_="table"))
        elements.append(Paragraph(f"Stand:{datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                  self.custom_styles["CustomBodyTextRight"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.5'] * cm))

        organisation_data, valid = organisation_handler.get_organisation_data()
        if not valid:
            return organisation_data, valid

        if organisation_data['name']:
            elements.append(Paragraph(organisation_data['name'], self.style_sheet["Title"]))
        elements.append(Paragraph(data['member_data']['name'], self.style_sheet["Title"]))
        elements.append(Spacer(width=0, height=c.config.spacer['0.5'] * cm))

        return elements, True

    def _set_column_width(self, data: dict) -> None:
        global column_width
        column_width = 2.9 * cm
        length = self._get_longest_value(data=data)
        new_column_width: float = 0.22 * length * cm
        if new_column_width > column_width:
            column_width = new_column_width

    @staticmethod
    def _check_data(path: str, active: bool, ID: int) -> None | str:
        try:
            validation.must_positive_int(int_=ID)
            validation.must_bool(bool_=active)
            validation.must_str(str_=path, length=None)
        except e.InputError as error:
            debug.info(item=debug_str, keyword="_validate_data", error_=sys.exc_info())
            return error.message

    def _mo_data_return(self, doc: SimpleDocTemplate, elements: list) -> tuple[str | None, bool]:
        elements.append(Paragraph(
            f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            self.style_sheet["BodyText"]))
        elements.append(Paragraph(
            f"Keine Daten vorhanden", self.style_sheet["BodyText"]))

        return self._export(doc=doc, elements=elements)


def create() -> None:
    global member_card_pdf
    member_card_pdf = MemberCardPDF()
