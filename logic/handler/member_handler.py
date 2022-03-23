# Purpur Tentakel
# 21.03.2022
# VereinsManager / Member Handler

from config import config_sheet as c, exception_sheet as e
from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, log_handler as l_h
from logic import validation as v
import debug

debug_str: str = "Member Handler"


# member
# add
def _add_member(data: dict, log_date: int | None) -> int:  # No Validation
    type_id = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])

    data = _transform_membership_for_safe(data=data, ID=type_id)
    data = _transform_dates_for_save(data=data)

    return a_h.add_handler.add_member(data=data, log_date=log_date)


# get
def get_member_data(ID: int, active: bool = True) -> [str | dict, bool]:
    try:
        v.validation.must_positive_int(int_=ID)
        v.validation.must_bool(bool_=active)

        member_data = _get_member_data_by_id(ID=ID, active=active)
        phone_data = _get_phone_number_by_member_id(member_id=ID)
        mail_data = _get_mail_by_member_id(member_id=ID)
        position_data = _get_position_by_member_id(member_id=ID)

        return {
                   "member_data": member_data,
                   "phone": phone_data,
                   "mail": mail_data,
                   "position": position_data,
               }, True

    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="get_member_data", message=f"Error = {error.message}")
        return error.message, False


def get_names_of_member(active: bool = True) -> tuple:
    try:
        v.validation.must_bool(bool_=active)
        return s_h.select_handler.get_names_of_member(active=active), True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="get_names_of_member", message=f"Error = {error.message}")
        return error.message, False


def _get_member_data_by_id(ID: int, active: bool = True) -> dict:
    v.validation.must_positive_int(int_=ID, max_length=None)
    v.validation.must_bool(bool_=active)

    data = s_h.select_handler.get_member_data_by_id(ID=ID, active=active)
    data = _transform_to_dict(data)
    data = _transform_membership_for_load(data=data)
    data = _transform_dates_for_load(data)

    return data


def _get_member_activity_by_id(ID: int) -> bool:
    v.validation.must_positive_int(int_=ID, max_length=None)

    data = s_h.select_handler.get_member_activity_by_id(ID=ID)
    if isinstance(data[0], int):
        data = data[0] == 1

    return data


# update
def update_member_data(ID: int, data: dict, log_date: int | None) -> [str | dict, bool]:
    try:
        v.validation.must_dict(dict_=data)
        v.validation.must_default_user(c.config.user_id, False)
        if ID is not None:
            v.validation.must_positive_int(int_=ID, max_length=None)

        member_data: dict = data["member_data"]
        member_nexus_data: dict = data["member_nexus_data"]

        v.validation.update_member(data=member_data)

        if ID is None:
            ID = _add_member(data=member_data, log_date=log_date)
        else:
            _update_member(ID=ID, data=member_data, log_date=log_date)

        ids = _update_add_member_nexus(data=member_nexus_data, member_id=ID, log_date=log_date)

        ids["member_id"] = ID
        return ids, True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
        return error.message, False


def _update_member(ID: int | None, data: dict, log_date: int | None) -> None:  # No Validation
    type_id = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])

    data = _transform_membership_for_safe(data=data, ID=type_id)
    data = _transform_dates_for_save(data=data)

    reference_data = _get_member_data_by_id(ID=ID, active=True)
    u_h.update_handler.update_member(ID=ID, data=data)
    l_h.log_handler.log_member(target_id=ID, old_data=reference_data, new_data=data, log_date=log_date)


def update_member_activity(ID: int, active: bool, log_date: int | None) -> [str | None, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
        v.validation.must_bool(bool_=active)
        v.validation.must_default_user(c.config.user_id, False)

        reference_data = _get_member_activity_by_id(ID=ID)
        u_h.update_handler.update_member_activity(ID=ID, active=active)
        l_h.log_handler.log_member_activity(target_id=ID, old_activity=reference_data, new_activity=active,
                                            log_date=log_date)
        return None, True

    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="update_member_activity", message=f"Error = {error.message}")
        return error.message, False


# helper
def _transform_membership_for_safe(data, ID) -> dict:
    if ID:
        data["membership_type"] = ID[0]
    else:
        data["membership_type"] = ID
    return data


def _transform_membership_for_load(data: dict) -> dict:
    if isinstance(data["membership_type"], int):
        data["membership_type"] = s_h.select_handler.get_type_name_by_ID(data["membership_type"])[0]
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
        "maps": data[7],
        "birth_date": data[8],
        "entry_date": data[9],
        "membership_type": data[10],
        "special_member": data[11],
        "comment_text": data[12],
    }


# member nexus
# add
def _add_member_nexus_phone(type_id: int, value: str, member_id: int, log_date: int | None) -> int:
    return a_h.add_handler.add_member_nexus_phone(type_id=type_id, value=value, member_id=member_id, log_date=log_date)


def _add_member_nexus_mail(type_id: int, value: str, member_id: int, log_date: int | None) -> int:
    return a_h.add_handler.add_member_nexus_mail(type_id=type_id, value=value, member_id=member_id, log_date=log_date)


def _add_member_nexus_position(type_id: int, value: bool, member_id: int, log_date: int | None) -> int:
    return a_h.add_handler.add_member_nexus_position(type_id=type_id, value=value, member_id=member_id,
                                                     log_date=log_date)


# get
def _get_phone_number_by_member_id(member_id: int) -> tuple:
    v.validation.must_positive_int(int_=member_id, max_length=None)
    return s_h.select_handler.get_phone_number_by_member_id(member_id=member_id)


def _get_mail_by_member_id(member_id: int) -> tuple:
    v.validation.must_positive_int(int_=member_id, max_length=None)
    return s_h.select_handler.get_mail_by_member_id(member_id=member_id)


def _get_position_by_member_id(member_id: int) -> tuple:
    v.validation.must_positive_int(int_=member_id, max_length=None)
    data = s_h.select_handler.get_position_by_member_id(member_id=member_id)

    data = list(data)
    for i in range(len(data)):
        data[i] = list(data[i])
    for i in data:
        data[data.index(i)][2] = data[data.index(i)][2] == 1
    for i in range(len(data)):
        data[i] = tuple(data[i])

    return tuple(data)


# update
def _update_add_member_nexus(data: dict, member_id: int, log_date: int | None) -> dict:
    v.validation.must_dict(data)

    phone_ids = _update_add_member_nexus_phone(phone=data["phone"], member_id=member_id, log_date=log_date)
    mail_ids = _update_add_member_nexus_mail(mail=data["mail"], member_id=member_id, log_date=log_date)
    position_ids = _update_add_member_nexus_position(position=data["position"], member_id=member_id, log_date=log_date)

    return {
        "phone": phone_ids,
        "mail": mail_ids,
        "position": position_ids,
    }


def _update_add_member_nexus_phone(phone: list, member_id: int, log_date: int) -> list:
    phone_ids: list = list()
    for ID, type_id, Type, phone_number in phone:
        v.validation.update_member_nexus(data=[ID, type_id, Type, phone_number], type_="phone")

        if ID is None:
            new_ID = _add_member_nexus_phone(type_id=type_id, value=phone_number, member_id=member_id,
                                             log_date=log_date)
        else:
            new_ID = _update_member_nexus_phone(ID=ID, number=phone_number, log_date=log_date)
        phone_ids.append(new_ID)

    return phone_ids


def _update_add_member_nexus_mail(mail: list, member_id: int, log_date: int) -> list:
    mail_ids: list = list()
    for ID, type_id, Type, mail_ in mail:
        v.validation.update_member_nexus(data=[ID, type_id, Type, mail_], type_="mail")

        if ID is None:
            new_ID = _add_member_nexus_mail(type_id=type_id, value=mail_, member_id=member_id, log_date=log_date)
        else:
            new_ID = _update_member_nexus_mail(ID=ID, mail=mail_, log_date=log_date)
        mail_ids.append(new_ID)

    return mail_ids


def _update_add_member_nexus_position(position: list, member_id: int, log_date: int) -> list:
    position_ids: list = list()
    for ID, type_id, Type, active in position:
        v.validation.update_member_nexus(data=[ID, type_id, Type, active], type_="position")

        if ID is None:
            new_ID = _add_member_nexus_position(type_id=type_id, value=active, member_id=member_id, log_date=log_date)
        else:
            new_ID = _update_member_nexus_position(ID=ID, active=active, log_date=log_date)
        position_ids.append(new_ID)

    return position_ids


def _update_member_nexus_phone(ID: int, number: str, log_date: int) -> None:  # no Validation
    reference_data = s_h.select_handler.get_phone_number_by_ID(ID=ID)
    u_h.update_handler.update_member_nexus_phone(ID=ID, number=number)
    l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=number, log_date=log_date,
                                     type_="phone")


def _update_member_nexus_mail(ID: int, mail: str, log_date: int) -> None:  # no Validation
    reference_data = s_h.select_handler.get_mail_member_by_ID(ID=ID)
    u_h.update_handler.update_member_nexus_mail(ID=ID, mail=mail)
    l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=mail, log_date=log_date,
                                     type_="mail")


def _update_member_nexus_position(ID: int, active: bool, log_date: int) -> None:  # no Validation
    reference_data = s_h.select_handler.get_position_member_by_ID(ID=ID)
    u_h.update_handler.update_member_nexus_position(ID=ID, active=active)
    l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=active, log_date=log_date,
                                     type_="position")
