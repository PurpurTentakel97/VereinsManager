# Purpur Tentakel
# 06.05.2022
# VereinsManager // Location Window

from logic.pdf_handler.base_pdf import BasePDF

location_pdf: "LocationPDF"


class LocationPDF(BasePDF):
    def __init__(self):
        super().__init__()

    def create_PDF(self, path: str, ID: int) -> tuple[None or str, bool]:
        print(path, ID)


def create() -> None:
    global location_pdf
    location_pdf = LocationPDF()
