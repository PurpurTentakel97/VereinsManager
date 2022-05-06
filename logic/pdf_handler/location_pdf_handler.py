# Purpur Tentakel
# 06.05.2022
# VereinsManager // Location PDF Handler
from datetime import datetime

from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from logic.pdf_handler.base_pdf import BasePDF
from logic.data_handler import location_data_handler
from config import config_sheet as c
import debug

debug_str: str = "LocationPDF"

location_pdf: "LocationPDF"


class LocationPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_PDF(self, path: str, ID: int) -> tuple[None or str, bool]:
        self.create_basics(path)
        doc: SimpleDocTemplate = self._get_doc()

        data, valid = location_data_handler.get_location_data(ID=ID)
        if not valid:
            return data, valid

        elements: list = list()
        elements.extend(self._get_header(name=data['name']))

        if not data:
            return self._no_data_return(doc=doc, elements=elements)

        elements.extend(self._get_location(data=data))

        debug.debug(item=debug_str, keyword="create_PDF", message=f"data = {data}")

        return self._export(doc=doc, elements=elements)

    def _get_header(self, name: str) -> list:
        elements: list = list()
        if self._is_icon():
            elements.append(self._get_icon('table'))
        elements.append(Paragraph(f"Stand:{datetime.strftime(datetime.now(), c.config.date_format['short'])}",
                                  self.custom_styles["CustomBodyTextRight"]))
        elements.append(Spacer(width=0, height=1 * cm))

        if name:
            elements.append(Paragraph(name, self.style_sheet["Title"]))

        elements.append(Spacer(width=0, height=0.5 * cm))
        return elements

    def _get_location(self, data: dict) -> list:
        data['comment'] = data['comment'].replace('\n', '<br/>')
        elements: list = list()
        address: Paragraph = Paragraph(
            f"<b>Adresse:</b><br/>"
            f"{data['name']}<br/>"
            f"{data['owner']}<br/>"
            f"{data['street']} {data['number']}<br/>"
            f"{data['zip_code']} {data['city']}<br/>"
            f"{data['country']}<br/>"
            f"{data['maps_link']}",
            self.style_sheet['BodyText']
        )
        elements.append(address)
        elements.append(Spacer(width=0, height=0.5 * cm))

        comment: Paragraph = Paragraph(
            f"<b>Kommentar:</b><br/>"
            f"{data['comment']}",
            self.style_sheet['BodyText']
        )
        elements.append(comment)

        return elements

    def _no_data_return(self, doc: SimpleDocTemplate, elements: list) -> tuple[str | None, bool]:
        elements.append(Paragraph("Keine Daten vorhanden", self.style_sheet['BodyText']))
        return self._export(doc=doc, elements=elements)


def create() -> None:
    global location_pdf
    location_pdf = LocationPDF()
