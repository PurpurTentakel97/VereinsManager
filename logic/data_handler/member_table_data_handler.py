# Purpur Tentakel
# 06.03.2022
# VereinsManager / Table Data Handler

import datetime
import sys

from config import config_sheet as c, exception_sheet as e
from logic.sqlite import select_handler as s_h
from logic.main_handler import member_nexus_handler as m_n_h

import debug

debug_str: str = "table_data_handler"


def get_member_table_data(active: bool) -> [str | dict, bool]:
    # validation
    try:
        types = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id["membership"], active=True)
        type_ids: list = [x[0] for x in types]

        final_data: dict = dict()
        for type_id in type_ids:
            member_data = s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                                        membership_type_id=type_id)
            final_members_list: list = list()

            for member in member_data:
                member_dict = _transform_member_data(member=member)
                phone_data = m_n_h.get_phone_number_by_member_id(member_id=member_dict["ID"])
                mail_data = m_n_h.get_mail_by_member_id(member_id=member_dict["ID"])
                phone_list = _transform_nexus_data(nexus_data=phone_data)
                mail_list = _transform_nexus_data(nexus_data=mail_data)

                single_member_data: dict = {
                    "member": member_dict,
                    "phone": phone_list,
                    "mail": mail_list,
                }
                final_members_list.append(single_member_data)
            final_data[type_id] = final_members_list
        return final_data, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_member_table_data", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_member_table_data", error_=sys.exc_info())
        return error.message, False


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


def _transform_nexus_data(nexus_data: tuple) -> list:
    nexus_list: list = list()
    for data in nexus_data:
        nexus_dict: dict = {
            "ID": data[0],
            "type": data[1],
            "number": data[2],
        }
        type_name = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=nexus_dict["type"])

        nexus_dict["type"] = type_name[0]
        data: list = [
            nexus_dict["type"],
            nexus_dict["number"],
        ]
        nexus_list.append(data)
    return nexus_list


def _transform_timestamp_to_datetime(timestamp: int) -> datetime:
    if timestamp:
        return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)


def _get_years_from_date_to_now(date: datetime.datetime) -> str or None:
    if not date:
        return

    now = datetime.datetime.now()
    years = now.year - date.year
    if now.month < date.month or (now.month == date.month and now.day < date.day):
        years -= 1
    return str(years)


def _transform_date_to_str(date: datetime) -> str or None:
    if not date:
        return

    return date.strftime(c.config.date_format["short"])


def _transform_street_and_number(street: str, number: str) -> str or None:
    if street and number:
        return f"{street} {number}"
    elif street:
        return street
    elif number:
        return number
