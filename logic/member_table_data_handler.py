# Purpur Tentakel
# 06.03.2022
# VereinsManager / Table Data Handler

import datetime

from config import config_sheet as c
from sqlite import select_handler as s_h

import debug

debug_str: str = "table_data_handler"


def get_member_table_data(active: bool) -> dict | str:
    types = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"])
    if isinstance(types, str):
        return types
    type_ids: list = [x[0] for x in types]

    final_data: dict = dict()
    for type_id in type_ids:
        # get data
        member_data = s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                                    membership_type_id=type_id)
        if isinstance(member_data, str):
            return member_data

        final_members_list: list = list()
        # member
        for member in member_data:
            member_dict = _transform_member_data(member=member)

            phone_data = s_h.select_handler.get_phone_number_by_member_id(member_id=member_dict["ID"])
            if isinstance(phone_data, str):
                return phone_data

            mail_data = s_h.select_handler.get_mail_by_member_id(member_id=member_dict["ID"])
            if isinstance(mail_data, str):
                return mail_data

            phone_list = _transform_nexus_data(nexus_data=phone_data)
            if isinstance(phone_list, str):
                return phone_list

            mail_list = _transform_nexus_data(nexus_data=mail_data)
            if isinstance(mail_list, str):
                return mail_list

            single_member_data: dict = {
                "member": member_dict,
                "phone": phone_list,
                "mail": mail_list,
            }
            final_members_list.append(single_member_data)
        final_data[type_id] = final_members_list
    return final_data


def _transform_member_data(member: list) -> dict:
    member_dict: dict = {
        "ID": member[0],
        "first_name": member[1],
        "last_name": member[2],
        "street": member[3],
        "number": member[4],
        "zip_code": member[5],
        "city": member[6],
        "maps": member[7],
        "b_date": member[8],
        "entry_date": member[9],
        "special_member": member[11],
    }

    member_dict["street"] = _transform_street_and_number(street=member_dict["street"],
                                                         number=member_dict["number"])
    del member_dict["number"]
    member_dict["zip_code"] = None if not member_dict["zip_code"] else str(member_dict["zip_code"])
    member_dict["b_date"] = _transform_timestamp_to_datetime(member_dict["b_date"])
    member_dict["entry_date"] = _transform_timestamp_to_datetime(member_dict["entry_date"])
    member_dict["age"] = _get_years_from_date_to_now(member_dict["b_date"])
    member_dict["membership_years"] = _get_years_from_date_to_now(member_dict["entry_date"])
    member_dict["b_date"] = _transform_date_to_str(member_dict["b_date"])
    member_dict["entry_date"] = _transform_date_to_str(member_dict["entry_date"])
    member_dict["special_member"] = "X" if member_dict["special_member"] else ""

    return member_dict


def _transform_nexus_data(nexus_data: list) -> str | list:
    nexus_list: list = list()
    for data in nexus_data:
        nexus_dict: dict = {
            "ID": data[0],
            "type": data[1],
            "number": data[2],
        }
        result = s_h.select_handler.get_type_name_by_ID(ID=nexus_dict["type"])
        if isinstance(result, str):
            return result

        nexus_dict["type"] = result[0]
        data: list = [
            nexus_dict["type"],
            nexus_dict["number"],
        ]
        nexus_list.append(data)
    return nexus_list


def _transform_timestamp_to_datetime(timestamp: int) -> datetime:
    if timestamp:
        if timestamp > 0:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)


def _get_years_from_date_to_now(date: datetime.datetime) -> str | None:
    if not date:
        return None
    else:
        now = datetime.datetime.now()
        years = now.year - date.year
        if now.month < date.month or (now.month == date.month and now.day < date.day):
            years -= 1
        return str(years)


def _transform_date_to_str(date: datetime) -> str | None:
    if not date:
        return None
    else:
        return date.strftime(c.config.date_format["short"])


def _transform_street_and_number(street: str, number: str) -> str or None:
    if street and number:
        return f"{street} {number}"
    elif street:
        return street
    elif number:
        return number
    else:
        return None
