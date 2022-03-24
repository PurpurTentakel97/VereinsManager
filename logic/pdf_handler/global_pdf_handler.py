# Purpur Tentakel
# 06.03.2022
# VereinsManager / Global PDF Handler
import os

from logic.pdf_handler import base_pdf as b_p, member_table_pdf as m_t_p, member_anniversary_pdf as m_a_p
from config import config_sheet as c


def create_pdf_handler() -> None:
    b_p.create_base_pdf()
    m_t_p.create_member_table_pdf()
    m_a_p.create_member_anniversary_pdf()


def open_last_export() -> None:
    os.startfile(c.config.last_export_path)
