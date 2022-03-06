# Purpur Tentakel
# 06.03.2022
# VereinsManager / PDF / Member Table

from fpdf import FPDF

from sqlite import select_handler as s_h


class PDF(FPDF):
    def get_member_data(self, active: bool, membership_type_id: int):
        return s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                             membership_type_id=membership_type_id)


def create_member_table_pdf():
    pass
