# Purpur Tentakel
# 06.03.2022
# VereinsManager / Global PDF Handler

import os

from config import config_sheet as c
from logic.pdf_handler import member_table_pdf, member_card_pdf, member_anniversary_pdf, member_log_pdf, \
    member_entry_letter_pfd, location_pdf_handler


def create_pdf_handler() -> None:
    member_table_pdf.create()
    member_card_pdf.create()
    member_anniversary_pdf.create()
    member_log_pdf.create()
    member_entry_letter_pfd.create()
    location_pdf_handler.create()


# member
def create_member_card(ID: int, path: str, active: bool = True) -> tuple[None or str, bool]:
    return member_card_pdf.member_card_pdf.create_pdf(path=path, active=active, ID=ID)


def create_member_table_pdf(path: str, active: bool = True) -> tuple[None or str, bool]:
    return member_table_pdf.member_table_pdf.create_pdf(path=path, active=active)


def create_member_anniversary_pdf(path: str, year: int or None = None, active: bool = True) -> tuple[None or str, bool]:
    return member_anniversary_pdf.member_anniversary_pdf.create_pdf(path=path, year=year, active=active)


def create_member_log_pdf(ID: int, path: str, active: bool) -> tuple[None or str, bool]:
    return member_log_pdf.member_log_pdf.create_pdf(path=path, ID=ID, active=active)


def create_member_entry_letter_pdf(ID: int, path: str, active: bool, log_id: int) -> tuple[None or str, bool]:
    return member_entry_letter_pfd.member_entry_letter_pdf.create_pdf(ID=ID, path=path, active=active, log_id=log_id)


# other
def create_location_pdf(ID: int, path: str) -> tuple[None or str, bool]:
    return location_pdf_handler.location_pdf.create_PDF(ID=ID, path=path)


def open_last_export() -> None:
    os.startfile(c.config.last_export_path)
