# Purpur Tentakel
# 06.03.2022
# VereinsManager / PDF / Member Table

from pdf_handler import base_pdf as b_p, member_table_pdf as m_t_p


def create_pdf_handler() -> None:
    b_p.create_base_pdf()
    m_t_p.create_member_table_pdf()
