# Purpur Tentakel
# 21.03.2022
# VereinsManager / Member Handler

import sys

from helpers import validation
from logic.main_handler import member_nexus_handler
from config import config_sheet as c, exception_sheet as e
from logic.sqlite import select_handler as s_h, delete_handler as d_h, log_handler as l_h, update_handler as u_h, \
    statistics_handler as st_h, add_handler as a_h
import debug

debug_str: str = "Member Handler"


# add
def _add_member(data: dict, log_date: int | None) -> int:  # No Validation
    data = _transform_type_for_safe(data=data, raw_id=c.config.raw_type_id['membership'], key="membership_type")
    data = _transform_type_for_safe(data=data, raw_id=c.config.raw_type_id['country'], key="country")
    data = _transform_dates_for_save(data=data)
    result = a_h.add_handler.add_member(data=data, log_date=log_date)

    st_h.statistics_handler.statistics(type_="membership", raw_type_id=c.config.raw_type_id["membership"],
                                       new_type_id=data["membership_type"], old_type_id=None)

    return result


# get
def get_member_data(ID: int, active: bool = True) -> tuple[str | dict, bool]:
    try:
        validation.must_positive_int(int_=ID)
        validation.must_bool(bool_=active)

        member_data = _get_member_data_by_id(ID=ID, active=active)
        phone_data = member_nexus_handler.get_phone_number_by_member_id(member_id=ID)
        mail_data = member_nexus_handler.get_mail_by_member_id(member_id=ID)
        position_data = member_nexus_handler.get_position_by_member_id(member_id=ID)

        return {
                   "member_data": member_data,
                   "phone": phone_data,
                   "mail": mail_data,
                   "position": position_data,
               }, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_member_data", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_member_data", error_=sys.exc_info())
        return error.message, False


def get_names_of_member(active: bool = True) -> tuple:
    try:
        validation.must_bool(bool_=active)
        return s_h.select_handler.get_names_of_member(active=active), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_names_of_member", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_names_of_member", error_=sys.exc_info())
        return error.message, False


def _get_member_data_by_id(ID: int, active: bool = True) -> dict:
    validation.must_positive_int(int_=ID, max_length=None)
    validation.must_bool(bool_=active)

    data = s_h.select_handler.get_member_data_by_id(ID=ID, active=active)
    data = _transform_to_dict(data)
    data = _transform_type_for_load(data=data, key="membership_type")
    data = _transform_type_for_load(data=data, key="country")
    data = _transform_dates_for_load(data)

    return data


def _get_member_activity_and_membership_by_id(ID: int) -> list:
    validation.must_positive_int(int_=ID, max_length=None)

    data = s_h.select_handler.get_member_activity_and_membership_by_id(ID=ID)
    data = list(data)
    if isinstance(data[0], int):
        data[0] = data[0] == 1

    return data


# add / update
def add_update_member_data(ID: int, data: dict, log_date: int | None) -> tuple[str | dict, bool]:
    try:
        validation.must_dict(dict_=data)
        validation.must_default_user(c.config.user['ID'], False)
        if ID is not None:
            validation.must_positive_int(int_=ID, max_length=None)

        member_data: dict = data["member_data"]
        member_nexus_data: dict = data["member_nexus_data"]

        validation.check_update_member(data=member_data)

        if ID is None:
            ID = _add_member(data=member_data, log_date=log_date)
        else:
            _update_member(ID=ID, data=member_data, log_date=log_date)

        ids = member_nexus_handler.update_add_member_nexus(data=member_nexus_data, member_id=ID, log_date=log_date)

        ids["member_id"] = ID
        return ids, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="update_member_data", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_member_data", error_=sys.exc_info())
        return error.message, False


# update
def update_member_activity(ID: int, active: bool, log_date: int | None) -> tuple[str | None, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)
        validation.must_bool(bool_=active)
        validation.must_default_user(c.config.user['ID'], False)

        reference_data = _get_member_activity_and_membership_by_id(ID=ID)
        u_h.update_handler.update_member_activity(ID=ID, active=active)
        member_nexus_handler.update_member_nexus_activity(member_id=ID, active=active)
        l_h.log_handler.log_member_activity(target_id=ID, old_activity=reference_data[0], new_activity=active,
                                            log_date=log_date)
        st_h.statistics_handler.statistics(type_="membership", raw_type_id=c.config.raw_type_id["membership"],
                                           new_type_id=reference_data[1], old_type_id=None)
        return None, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="update_member_activity", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_member_activity", error_=sys.exc_info())
        return error.message, False


def _update_member(ID: int | None, data: dict, log_date: int | None) -> None:  # No Validation
    data = _transform_type_for_safe(data=data, raw_id=c.config.raw_type_id['membership'], key="membership_type")
    data = _transform_type_for_safe(data=data, raw_id=c.config.raw_type_id['country'], key="country")
    data = _transform_dates_for_save(data=data)

    reference_data = _get_member_data_by_id(ID=ID, active=True)
    u_h.update_handler.update_member(ID=ID, data=data)
    st_h.statistics_handler.statistics(type_="membership", raw_type_id=c.config.raw_type_id["membership"],
                                       new_type_id=data["membership_type"],
                                       old_type_id=s_h.select_handler.get_id_by_type_name(raw_id=1, name=reference_data[
                                           "membership_type"])[0])
    l_h.log_handler.log_member(target_id=ID, old_data=reference_data, new_data=data, log_date=log_date)


# delete
def delete_inactive_member() -> None:
    try:
        reference_data, _ = get_names_of_member(active=False)
        for ID, *_ in reference_data:
            member_nexus_handler.delete_inactive_member_nexus(member_id=ID)
            l_h.log_handler.delete_log(target_id=ID, target_table="member")
            d_h.delete_handler.delete_member(ID=ID)

    except e.OperationalError:
        debug.error(item=debug_str, keyword="delete_inactive_member", error_=sys.exc_info())


# helpers
def _transform_type_for_safe(data, raw_id, key) -> dict:
    type_id = s_h.select_handler.get_id_by_type_name(raw_id=raw_id, name=data[key])
    if type_id:
        data[key] = type_id[0]
    else:
        data[key] = type_id
    return data


def _transform_type_for_load(data: dict, key) -> dict:
    if isinstance(data[key], int):
        type_name, extra_value = s_h.select_handler.get_type_name_and_extra_value_by_ID(data[key])
        data[key] = type_name
        data[f"{key}_extra_value"] = extra_value
    return data


def _transform_dates_for_save(data) -> dict:
    if data["birth_date"] == c.config.date_format["None_date"]:
        data["birth_date"] = None
    if data["entry_date"] == c.config.date_format["None_date"]:
        data["entry_date"] = None
    return data


def _transform_dates_for_load(data) -> dict:
    if data["birth_date"] is None:
        data["birth_date"] = c.config.date_format["None_date"]
    if data["entry_date"] is None:
        data["entry_date"] = c.config.date_format["None_date"]
    return data


def _transform_to_dict(data) -> dict:
    return {
        "ID": data[0],
        "first_name": data[1],
        "last_name": data[2],
        "street": data[3],
        "number": data[4],
        "zip_code": data[5],
        "city": data[6],
        "country": data[7],
        "maps": data[8],
        "birth_date": data[9],
        "entry_date": data[10],
        "membership_type": data[11],
        "special_member": data[12],
        "comment_text": data[13],
    }
