# Purpur Tentakel
# 06.03.2022
# VereinsManager / Table Data Handler

from config import config_sheet as c
from sqlite import select_handler as s_h

import debug

debug_str: str = "table_data_handler"


def get_member_table_data(active: bool) -> dict | str:
    types = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"])
    if isinstance(types, str):
        return types
    type_ids: list = [x[0] for x in types]
    data: dict = dict()
    for type_id in type_ids:
        member_data = s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                                    membership_type_id=type_id)
        if isinstance(member_data, str):
            return member_data
        complete_type: list = list()
        for single_member_data in member_data:
            phone_data = s_h.select_handler.get_phone_number_by_member_id(member_id=single_member_data[0])
            if isinstance(phone_data, str):
                return phone_data
            mail_data = s_h.select_handler.get_mail_by_member_id(member_id=single_member_data[0])
            if isinstance(mail_data, str):
                return mail_data
            nexus_data: dict = {
                "member": single_member_data,
                "phone": phone_data,
                "mail": mail_data,
            }
            complete_type.append(nexus_data)
        data[type_id] = complete_type
    return data
