# Purpur Tentakel
# 06.03.2022
# VereinsManager / Global PDF Handler

import os

from config import config_sheet as c
from logic.pdf_handler import member_table_pdf, member_card_pdf, member_anniversary_pdf, member_log_pdf, \
    member_entry_letter_pfd


def create_pdf_handler() -> None:
    member_table_pdf.create()
    member_card_pdf.create()
    member_anniversary_pdf.create()
    member_log_pdf.create()
    member_entry_letter_pfd.create()


def open_last_export() -> None:
    os.startfile(c.config.last_export_path)
