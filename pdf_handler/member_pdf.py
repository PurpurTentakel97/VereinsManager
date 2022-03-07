# Purpur Tentakel
# 06.03.2022
# VereinsManager / PDF / Member Table

from reportlab.lib import colors
from reportlab.lib.pagesizes import inch, A4
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1

import os

from logic import table_data_handler
from sqlite import select_handler as s_h
from config import config_sheet as c
import debug

debug_str: str = "PDF"

dir_name: str = str()
file_name: str = str()
style_sheet: StyleSheet1


def member_pdf(path: str, active: bool):
    _transform_path(path=path)

    data = table_data_handler.get_member_table_data(active=active)

    type_ids = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"])
    type_ids = [[x[0], x[1]] for x in type_ids]

    global style_sheet
    style_sheet = getSampleStyleSheet()
    doc = SimpleDocTemplate("test.pdf", pagesize=[A4[1], A4[0]])

    elements: list = list()
    for type_id, type in type_ids:
        all_members: list = data[type_id]
        if not all_members:
            continue
        table_data: list = [[type, "Name", "Adresse", "Alter", "Eintritt", "Telefon", "Mail"]]
        style_data: list = []
        for index, member in enumerate(all_members, start=1):
            member_data = member["member"]
            phone_data = member["phone"]
            mail_data = member["mail"]
            row_data: list = [
                str(index),
                [_paragraph(member_data[0]), _paragraph(member_data[1])],
                [_paragraph(member_data[2]), _paragraph(member_data[3]), _paragraph(member_data[4])],
                [_paragraph(member_data[6]), _paragraph(member_data[5])],
                [_paragraph(member_data[8]), _paragraph(member_data[7])],
                [_paragraph(x) for x in phone_data],
                [_paragraph(x) for x in mail_data],
            ]
            table_data.append(row_data)

            if member_data[9]:
                style_data.append(("BACKGROUND", (0, index), (0, index), colors.lightgrey))
            if member_data[6] is not None and int(member_data[6]) % 5 == 0:
                style_data.append(("BACKGROUND", (3, index), (3, index), colors.lightgrey))
            if member_data[8] is not None and int(member_data[8]) % 5 == 0:
                style_data.append(("BACKGROUND", (4, index), (4, index), colors.lightgrey))

        t = Table(table_data, style=style_data)
        t._argW[3] = 1.5 * inch
        elements.append(t)
    doc.build(elements)


def _transform_path(path: str):
    global dir_name
    global file_name
    if path:
        dir_name, file_name = os.path.split(path)
    else:
        dir_name = "pdf"
        file_name = "Mitglieder_pdf"


def _paragraph(value) -> Paragraph:
    if isinstance(value, list):
        return Paragraph(str(value[0]) + ": " + str("---" if not value[1] else value[1]), style_sheet["BodyText"])
    else:
        return Paragraph(str("---" if not value else value), style_sheet["BodyText"])
