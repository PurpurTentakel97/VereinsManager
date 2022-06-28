# Purpur Tentakel
# 06.03.2022
# VereinsManager / Table Data Handler

import sys
import datetime

from helpers import helper
from logic.sqlite import select_handler as s_h
from logic.main_handler import member_nexus_handler
from config import config_sheet as c, exception_sheet as e

import debug

debug_str: str = "Table Data Handler"


def get_member_table_data(active: bool) -> tuple[str | dict, bool]:
    # validation
    try:
        types: tuple = s_h.select_handler.get_single_raw_type_types(c.config.raw_type_id.membership, active=True)
        type_ids: list = [x[0] for x in types]

        final_data: dict = dict()
        for type_id in type_ids:
            type_id: int
            member_data: tuple = s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                                               membership_type_id=type_id)
            final_members_list: list = list()

            for member in member_data:
                member_data: dict = _transform_member_data(member=member)
                phone_data: tuple = member_nexus_handler.get_phone_number_by_member_id(member_id=member_data['ID'])
                mail_data: tuple = member_nexus_handler.get_mail_by_member_id(member_id=member_data['ID'])
                phone_list: list = _transform_nexus_data(nexus_data=phone_data)
                mail_list: list = _transform_nexus_data(nexus_data=mail_data)

                single_member_data: dict = {
                    'member': member_data,
                    'phone': phone_list,
                    'mail': mail_list,
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


def _get_years_from_date_to_now(date: datetime.datetime) -> str:
    if not date:
        return helper.None_str

    years: int = helper.get_accurate_years_from_date_to_now(date=date)

    return str(years)


def _get_member_dict(member):
    member_data: dict = {
        'ID': member[0],
        'first_name': member[1],
        'last_name': member[2],
        'street': member[3],
        'number': member[4],
        'zip_code': member[5],
        'city': member[6],
        'country': member[7],
        'maps': member[8],
        'b_date': member[9],
        'entry_date': member[10],
        'special_member': member[12],
    }
    return member_data


def _transform_member_data(member: list) -> dict:
    member_data = _get_member_dict(member)

    member_data['b_date'] = helper.transform_timestamp_to_datetime(member_data['b_date'])
    member_data['entry_date'] = helper.transform_timestamp_to_datetime(member_data['entry_date'])
    member_data['age'] = _get_years_from_date_to_now(member_data['b_date'])
    member_data['membership_years'] = _get_years_from_date_to_now(member_data['entry_date'])
    member_data['b_date'] = _transform_date_to_str(member_data['b_date'])
    member_data['entry_date'] = _transform_date_to_str(member_data['entry_date'])
    member_data['special_member'] = helper.transform_int_to_str(integer=member_data['special_member'])
    member_data['country'] = _transform_country(member_data['country'])
    member_data['maps'] = _transform_maps(data=member_data)
    member_data = _transform_strings(data=member_data)
    member_data['street'] = _transform_street_and_number(street=member_data['street'],
                                                         number=member_data['number'])
    del member_data['number']

    return member_data


def _transform_country(country_id: int) -> str:
    if country_id:
        name, _ = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=country_id)
        return name


def _transform_nexus_data(nexus_data: tuple) -> list:
    nexus_list: list = list()
    for data in nexus_data:
        nexus_dict: dict = {
            "ID": data[0],
            "type": data[1],
            "number": helper.try_transform_to_None_string(string=data[2]),
        }
        type_name = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=nexus_dict["type"])

        nexus_dict["type"] = type_name[0]
        data: list = [
            nexus_dict["type"],
            nexus_dict["number"],
        ]
        nexus_list.append(data)
    return nexus_list


def _transform_date_to_str(date: datetime) -> str:
    if not date:
        return helper.None_str

    return date.strftime(c.config.date_format.short)


def _transform_street_and_number(street: str, number: str) -> str:
    return helper.combine_strings(strings=(street, number))


def _transform_strings(data: dict) -> dict:
    keys: tuple = (
        "first_name",
        "last_name",
        "zip_code",
        "city",
    )

    key: str
    for key in keys:
        data[key] = helper.try_transform_to_None_string(string=data[key])

    return data


def _transform_maps(data: dict) -> str:
    maps = helper.combine_maps_string(street=data['street'], number=data['number'], zip_code=data['zip_code'],
                                      city=data['city'])
    return maps
