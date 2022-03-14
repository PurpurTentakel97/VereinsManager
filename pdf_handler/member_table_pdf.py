# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Table PDF

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from datetime import datetime

from logic import member_table_data_handler
from sqlite import select_handler as s_h
from config import config_sheet as c
from pdf_handler.base_pdf import BasePDF
import debug

debug_str: str = "MemberTablePDF"

member_table_pdf: "MemberTablePDF"


class MemberTablePDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_pdf(self, path: str, active: bool):
        self.transform_path(path=path)
        self.create_dir()

        self.style_sheet = getSampleStyleSheet()
        doc = SimpleDocTemplate(f"{self.dir_name}/{self.file_name}", pagesize=A4, rightMargin=1.5 * cm,
                                leftMargin=1.5 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.5 * cm)
        elements: list = [
            Paragraph("Mitglieder", self.style_sheet["Title"])
        ]

        data = member_table_data_handler.get_member_table_data(active=active)
        if isinstance(data, str):
            return data
        if not data:
            elements.append(Paragraph(
                f"Stand: {datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                self.style_sheet["BodyText"]))
            elements.append(Paragraph(
                f"Keine Mitglieder vorhanden", self.style_sheet["BodyText"]))
            doc.build(elements)
            return

        type_ids = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"])
        if isinstance(type_ids, str):
            return type_ids
        type_ids = [[x[0], x[1]] for x in type_ids]

        for type_id, type_ in type_ids:
            all_members: list = data[type_id]
            elements.append(Paragraph(type_, self.style_sheet["Heading3"]))
            elements.append(Paragraph(f"Stand:{datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                      self.style_sheet["BodyText"]))
            if not all_members:
                elements.append(Paragraph(
                    f"Keine Mitglieder vorhanden",
                    self.style_sheet["BodyText"]))
                continue

            table_data: list = [[
                "",
                "Name / Adresse",
                "Alter / Eintritt",
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
                debug.debug(item=debug_str, keyword="create_pdf", message=f"street = {member_data['street']}")
                row_data: list = [
                    str(index) if not member_data["special_member"] else f"{str(index)} (E)",
                    [Paragraph(f"{member_data['first_name']} {member_data['last_name']}"),
                     self.paragraph(member_data["street"]), self.paragraph(member_data["zip_code"]),
                     self.paragraph(member_data["city"])],
                    [self.paragraph(["Alter", member_data["age"]]), self.paragraph(member_data["b_date"]),
                     self.paragraph(["Eintritt", member_data["membership_years"]]),
                     self.paragraph(member_data["entry_date"])],
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

            table = Table(table_data, style=style_data, repeatRows=1)
            elements.append(table)
            elements.append(Paragraph("(E) = Ehrenmitglied"))
        doc.build(elements)


def create_member_table_pdf() -> None:
    global member_table_pdf
    member_table_pdf = MemberTablePDF()
