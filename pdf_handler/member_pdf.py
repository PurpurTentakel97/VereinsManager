# Purpur Tentakel
# 06.03.2022
# VereinsManager / PDF / Member Table

from reportlab.lib import colors
from reportlab.lib.pagesizes import inch, A4
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1
from reportlab.lib.units import cm

from datetime import datetime
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
    _create_dir(dir_name)

    global style_sheet
    style_sheet = getSampleStyleSheet()
    doc = SimpleDocTemplate(f"{dir_name}/{file_name}", pagesize=[A4[1], A4[0]], rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    elements: list = [
        Paragraph("Mitglieder", style_sheet["Title"])
    ]

    data = table_data_handler.get_member_table_data(active=active)
    if isinstance(data, str):
        return data
    if not data:
        elements.append(Paragraph(
            f"Keine Mitglieder vorhanden // Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            style_sheet["BodyText"]))
        doc.build(elements)
        return

    type_ids = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"])
    if isinstance(type_ids, str):
        return type_ids
    type_ids = [[x[0], x[1]] for x in type_ids]

    for type_id, type in type_ids:
        all_members: list = data[type_id]
        elements.append(Paragraph(type, style_sheet["Heading3"]))
        if not all_members:
            elements.append(Paragraph(
                f"Keine Mitglieder vorhanden // Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                style_sheet["BodyText"]))
            continue

        table_data: list = [[
            f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
            "Name",
            "Adresse",
            "Alter",
            "Eintritt",
            "Telefon",
            "Mail",
        ]]
        style_data: list = [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ("LINEAFTER", (0, 0), (0, -1), 3, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 3, colors.black),
        ]
        for index, member in enumerate(all_members, start=1):
            member_data = member["member"]
            phone_data = member["phone"]
            mail_data = member["mail"]
            row_data: list = [
                str(index) if not member_data[9] else f"{str(index)} (E)",
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
            if member_data[6] is not None and (int(member_data[6]) % 10 == 0 or int(member_data[6]) == 18):
                style_data.append(("BACKGROUND", (3, index), (3, index), colors.lightgrey))
            if member_data[8] is not None and int(member_data[8]) % 5 == 0:
                style_data.append(("BACKGROUND", (4, index), (4, index), colors.lightgrey))

        table = Table(table_data, style=style_data, repeatRows=1)
        table._argW[3] = 1.5 * inch
        elements.append(table)
    doc.build(elements)


def _transform_path(path: str):
    global dir_name
    global file_name
    now = datetime.now()
    if path:
        dir_name, file_name = os.path.split(path)
        parts = file_name.split(".")
        file_type = parts[-1]
        name: str = str()
        for _ in parts[:-1]:
            name += _
        file_name = f"{name}_{now.strftime(c.config.date_format['path'])}.{file_type}"
        debug.info(item=debug_str, keyword="_transform_path", message=f"user = {file_name}")
    else:
        dir_name = f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.member_dir}/{c.config.export_dir}"
        file_name = f"Mitglieder_{now.strftime(c.config.date_format['path'])}.pdf"
        debug.info(item=debug_str, keyword="_transform_path", message=f"default = {file_name}")


def _paragraph(value) -> Paragraph:
    if isinstance(value, list):
        return Paragraph(str(value[0]) + ": " + str("---" if not value[1] else value[1]), style_sheet["BodyText"])
    else:
        return Paragraph(str("---" if not value else value), style_sheet["BodyText"])


def _create_dir(dirs: str) -> None:
    if not os.path.exists(dirs):
        os.mkdir(dirs)
