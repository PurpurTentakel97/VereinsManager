# Purpur Tentakel
# 06.03.2022
# VereinsManager / Table Data Handler

from datetime import datetime

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
        # get data
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

            # transform data
            single_member_data = list(single_member_data)
            for i in [0, -3, -1]:
                single_member_data.pop(i)
            if single_member_data[4]:
                single_member_data[4] = str(single_member_data[4])
            single_member_data[8] = "X" if single_member_data[8] else ""
            if single_member_data[2] and single_member_data[3]:
                single_member_data.insert(2, single_member_data.pop(2) + " " + single_member_data.pop(2))
            elif single_member_data[2]:
                single_member_data.insert(2, single_member_data.pop(2))
                single_member_data.pop(3)
            elif single_member_data[3]:
                single_member_data.insert(2, single_member_data.pop(3))
                single_member_data.pop(3)
            else:
                single_member_data.pop(2)
                single_member_data.pop(2)
                single_member_data.insert(2, None)

            for phone in phone_data:
                phone_list = list(phone)
                result = s_h.select_handler.get_type_name_by_id(ID=phone_list[1])
                if isinstance(result, str):
                    return result
                phone_list[1] = result[0]
                phone_list.pop(0)
                phone_data[phone_data.index(phone)] = phone_list

            for mail in mail_data:
                mail_list = list(mail)
                result = s_h.select_handler.get_type_name_by_id(ID=mail_list[1])
                if isinstance(result, str):
                    return result
                mail_list[1] = result[0]
                mail_list.pop(0)
                mail_data[mail_data.index(mail)] = mail_list

            # dates
            single_member_data[5] = _get_datetime_from_timestamp(single_member_data[5])
            single_member_data[6] = _get_datetime_from_timestamp(single_member_data[6])
            single_member_data.insert(7, _get_years_from_date_to_now(single_member_data[6]))
            single_member_data.insert(6, _get_years_from_date_to_now(single_member_data[5]))
            single_member_data[5] = _transform_date_to_str(single_member_data[5])
            single_member_data[7] = _transform_date_to_str(single_member_data[7])

            nexus_data: dict = {
                "member": single_member_data,
                "phone": phone_data,
                "mail": mail_data,
            }
            complete_type.append(nexus_data)
        data[type_id] = complete_type
    return data


def _get_datetime_from_timestamp(timestamp: int) -> datetime | None:
    if timestamp:
        return datetime.fromtimestamp(timestamp)


def _get_years_from_date_to_now(date: datetime) -> str | None:
    if not date:
        return None
    else:
        now = datetime.now()
        years = now.year - date.year
        if now.month > date.month or (now.month == date.month and now.day > date.day):
            years -= 1
        return str(years)


def _transform_date_to_str(date: datetime) -> str | None:
    if not date:
        return None
    else:
        return date.strftime(c.config.date_format["short"])
