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
def _add_member(data: dict, log_date: int | None) -> [int | str, bool]:  # No Validation
    result, valid = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])
    if not valid:
        return result, False
    if result:
        data["membership_type"] = result[0]
    else:
        data["membership_type"] = result

    if data["birth_date"] == c.config.date_format["None_date"]:
        data["birth_date"] = None
    if data["entry_date"] == c.config.date_format["None_date"]:
        data["entry_date"] = None

    return a_h.add_handler.add_member(data=data, log_date=log_date)


# get
def get_member_data(ID: int, active: bool = True) -> [dict | str, bool]:
    member_data, valid = get_member_data_by_id(ID=ID, active=active)
    if not valid:
        return member_data, False

    phone_data, valid = get_phone_number_by_member_id(member_id=ID)
    if not valid:
        return phone_data, False

    mail_data, valid = get_mail_by_member_id(member_id=ID)
    if not valid:
        return mail_data, False

    position_data, valid = get_position_by_member_id(member_id=ID)
    if not valid:
        return position_data, False

    data: dict = {
        "member_data": member_data,
        "phone": phone_data,
        "mail": mail_data,
        "position": position_data,
    }

    return data, True


def get_names_of_member(active: bool = True) -> [tuple | str, bool]:
    try:
        v.validation.must_bool(bool_=active)
    except e.NoBool as error:
        debug.error(item=debug_str, keyword="get_names_of_member", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_names_of_member(active=active)


def get_name_and_dates_from_member(active: bool = True) -> [tuple | str, bool]:
    try:
        v.validation.must_bool(bool_=active)
    except e.NoBool as error:
        debug.error(item=debug_str, keyword="get_name_and_dates_from_member", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_name_and_dates_from_member(active=active)


def get_data_from_member_by_membership_type_id(active: bool, membership_type_id: int) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=membership_type_id, max_length=None)
        v.validation.must_bool(bool_=active)
    except (e.NoInt, e.NoPositiveInt, e.ToLong, e.NoBool) as error:
        debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                    message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_data_from_member_by_membership_type_id(active=active,
                                                                         membership_type_id=membership_type_id)


def get_member_data_by_id(ID: int, active: bool = True) -> [dict | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
        v.validation.must_bool(bool_=active)
    except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
        return error.message, False

    data, valid = s_h.select_handler.get_member_data_by_id(ID=ID, active=active)
    if not valid:
        return data, False

    data_ = {
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
    if isinstance(data_["membership_type"], int):
        data, valid = s_h.select_handler.get_type_name_by_ID(data_["membership_type"])
        if not valid:
            return data, False
        else:
            data_["membership_type"] = data[0]

    if data_["birth_date"] is None:
        data_["birth_date"] = c.config.date_format["None_date"]
    if data_["entry_date"] is None:
        data_["entry_date"] = c.config.date_format["None_date"]

    return data_, True


def get_member_activity_by_id(ID: int) -> [bool | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
        return error.message, False

    data, valid = s_h.select_handler.get_member_activity_by_id(ID=ID)
    if not valid:
        return data, False

    if isinstance(data[0], int):
        data = data[0] == 1

    return data, True


def get_all_IDs_from_member(active: bool = True) -> [list or None, bool]:
    try:
        v.validation.must_bool(bool_=active)
    except e.NoBool as error:
        debug.error(item=debug_str, keyword="get_all_IDs_from_member", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_all_IDs_from_member(active=active)


# update
def update_member_data(ID: int, data: dict, log_date: int | None) -> [str | dict, bool]:
    try:
        v.validation.must_dict(dict_=data)
    except e.NoDict as error:
        debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
        return error.message, False

    member_data: dict = data["member_data"]
    member_nexus_data: dict = data["member_nexus_data"]

    try:
        v.validation.update_member(data=member_data)
    except (e.NoDict, e.NoStr, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
        debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
        return error.message, False

    is_bool = True
    if ID is None:
        ID, valid = _add_member(data=member_data, log_date=log_date)
        if not valid:
            return ID, False
        is_bool = False
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
        return error.message, False

    if is_bool:
        result, valid = _update_member(ID=ID, data=member_data, log_date=log_date)
        if not valid:
            return result, False

    ids, valid = _update_member_nexus(data=member_nexus_data, member_id=ID, log_date=log_date)
    if not valid:
        return ids, False

    ids["member_id"] = ID
    return ids, True


def _update_member(ID: int | None, data: dict, log_date: int | None) -> [str | None, bool]:  # No Validation
    result, valid = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])
    if not valid:
        return result, False

    if result:
        data["membership_type"] = result[0]
    else:
        data["membership_type"] = result

    if data["birth_date"] == c.config.date_format["None_date"]:
        data["birth_date"] = None
    if data["entry_date"] == c.config.date_format["None_date"]:
        data["entry_date"] = None

    reference_data, valid = get_member_data_by_id(ID=ID, active=True)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_member(ID=ID, data=data)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_member(target_id=ID, old_data=reference_data, new_data=data,
                                               log_date=log_date)
    if not valid:
        return result, False

    return None, True


def update_member_activity(ID: int, active: bool, log_date: int | None) -> [str | None, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
        v.validation.must_bool(bool_=active)
    except (e.NoPositiveInt, e.NoBool) as error:
        debug.error(item=debug_str, keyword="update_member_activity", message=f"Error = {error.message}")
        return error.message, False

    reference_data, valid = s_h.select_handler.get_member_activity_by_id(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_member_activity(ID=ID, active=active)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_member_activity(target_id=ID, old_activity=reference_data,
                                                        new_activity=active,
                                                        log_date=log_date)
    if not valid:
        return result, False

    return None, True


# member nexus
# add
def _add_member_nexus_phone(type_id: int, value: str, member_id: int, log_date: int | None) \
        -> [int | str, bool]:
    return a_h.add_handler.add_member_nexus_phone(type_id=type_id, value=value, member_id=member_id, log_date=log_date)


def _add_member_nexus_mail(type_id: int, value: str, member_id: int, log_date: int | None) \
        -> [int | str, bool]:
    return a_h.add_handler.add_member_nexus_mail(type_id=type_id, value=value, member_id=member_id, log_date=log_date)


def _add_member_nexus_position(type_id: int, value: bool, member_id: int, log_date: int | None) \
        -> [int or str, bool]:
    return a_h.add_handler.add_member_nexus_position(type_id=type_id, value=value, member_id=member_id,
                                                     log_date=log_date)


# get
def get_phone_number_by_member_id(member_id: int) -> [tuple or None, bool]:
    try:
        v.validation.must_positive_int(int_=member_id, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_phone_number_by_member_id(member_id=member_id)


def get_phone_number_by_ID(ID: int) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_phone_number_by_ID(ID=ID)


def get_mail_by_member_id(member_id: int) -> [tuple or None, bool]:
    try:
        v.validation.must_positive_int(int_=member_id, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_mail_by_member_id(member_id=member_id)


def get_mail_member_by_ID(ID: int) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_mail_member_by_ID(ID=ID)


def get_position_by_member_id(member_id: int) -> [tuple or None, bool]:
    try:
        v.validation.must_positive_int(int_=member_id, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
        return error.message, False

    data, valid = s_h.select_handler.get_position_by_member_id(member_id=member_id)
    if not valid:
        return data, False

    for i in range(len(data)):
        data[i] = list(data[i])
    for i in data:
        data[data.index(i)][2] = data[data.index(i)][2] == 1
    for i in range(len(data)):
        data[i] = tuple(data[i])

    return data, True


def get_position_member_by_ID(ID: int) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_position_member_by_ID", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_position_member_by_ID(ID=ID)


# update
def _update_member_nexus(data: dict, member_id: int, log_date: int | None) -> [str | dict, bool]:
    try:
        v.validation.must_dict(data)
    except e.NoDict as error:
        debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
        return error.message, False

    try:
        phone = data["phone"]
        mail = data["mail"]
        position = data["position"]
    except KeyError:
        debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = KeyError")
        return e.NoDict(info="Member Nexus").message, False

    # phone
    phone_ids: list = list()
    for ID, type_id, Type, phone_number in phone:
        try:
            v.validation.update_member_nexus(data=[ID, type_id, Type, phone_number], type_="phone")
        except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
            return error.message, False
        try:
            v.validation.must_positive_int(ID, max_length=None)
            result, valid = _update_member_nexus_phone(ID=ID, number=phone_number, log_date=log_date)
            if not valid:
                return result, False
            phone_ids.append(result)
        except (e.NoPositiveInt, e.NoInt, e.ToLong):
            result, valid = _add_member_nexus_phone(type_id=type_id, value=phone_number,
                                                    member_id=member_id, log_date=log_date)
            if not valid:
                return result, False
            phone_ids.append(result)

    # mail
    mail_ids: list = list()
    for ID, type_id, Type, mail_ in mail:
        try:
            v.validation.update_member_nexus(data=[ID, type_id, Type, mail_], type_="mail")
        except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
            return error.message, False
        try:
            v.validation.must_positive_int(ID, max_length=None)
            result, valid = _update_member_nexus_mail(ID=ID, mail=mail_, log_date=log_date)
            if not valid:
                return result, False
            mail_ids.append(result)
        except (e.NoPositiveInt, e.NoInt, e.ToLong):
            result, valid = _add_member_nexus_mail(type_id=type_id, value=mail_,
                                                   member_id=member_id, log_date=log_date)
            if not valid:
                return result, False
            mail_ids.append(result)

    # position
    position_ids: list = list()
    for ID, type_id, Type, active in position:
        try:
            v.validation.update_member_nexus(data=[ID, type_id, Type, active], type_="position")
        except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
            return error.message, False
        try:
            v.validation.must_positive_int(ID, max_length=None)
            result, valid = _update_member_nexus_position(ID=ID, active=active, log_date=log_date)
            if not valid:
                return result, False
            position_ids.append(result)
        except (e.NoPositiveInt, e.NoInt, e.ToLong):
            result, valid = _add_member_nexus_position(type_id=type_id, value=active,
                                                       member_id=member_id, log_date=log_date)
            if not valid:
                return result, False
            position_ids.append(result)

    # result
    return {
               "phone": phone_ids,
               "mail": mail_ids,
               "position": position_ids,
           }, True


def _update_member_nexus_phone(ID: int, number: str, log_date: int) -> [str | None, bool]:  # no Validation
    reference_data, valid = s_h.select_handler.get_phone_number_by_ID(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_member_nexus_phone(ID=ID, number=number)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=number,
                                                     log_date=log_date, type_="phone")
    if not valid:
        return result, False

    return None, True


def _update_member_nexus_mail(ID: int, mail: str, log_date: int) -> [str | None, bool]:  # no Validation
    reference_data, valid = s_h.select_handler.get_mail_member_by_ID(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_member_nexus_mail(ID=ID, mail=mail)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=mail,
                                                     log_date=log_date, type_="mail")
    if not valid:
        return result, False

    return None, True


def _update_member_nexus_position(ID: int, active: bool, log_date: int) -> [str | None, bool]:  # no Validation
    reference_data, valid = s_h.select_handler.get_position_member_by_ID(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_member_nexus_position(ID=ID, active=active)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=active,
                                                     log_date=log_date, type_="position")
    if not valid:
        return result, False

    return None, True
