# Purpur Tentakel
# 18.02.2022L
# VereinsManager / Validation

from helper import password_validation
from logic.main_handler import type_handler, organisation_handler
from logic.sqlite import select_handler as s_h
from config import exception_sheet as e, config_sheet as c
import debug

debug_str: str = "Validation"


# type
def check_add_type(type_name: str, raw_type_id: int, extra_value: str) -> None:
    must_str(str_=type_name)
    must_positive_int(int_=raw_type_id, max_length=None)
    if extra_value is not None:
        must_str(str_=extra_value)

    data = s_h.select_handler.get_all_single_type()
    type_name = type_name.strip().title()
    for _, name, id_, *_ in data:
        if type_name == name and id_ == raw_type_id:
            raise e.AlreadyExists()


def check_update_type(ID: int, new_name: str, new_extra_value: str) -> None:
    must_str(new_name)
    must_positive_int(ID, max_length=None)
    if new_extra_value is not None:
        must_str(new_extra_value)

    data = s_h.select_handler.get_all_single_type()
    exists: bool = False
    for old_id, old_name, _, _, old_extra_value in data:
        if ID == old_id:
            if new_name.strip().title() == old_name:
                if new_extra_value is None:
                    if new_extra_value == old_extra_value:
                        raise e.NoChance(info=new_name)
                if new_extra_value.strip().title() == old_extra_value:
                    raise e.NoChance(info=new_name)
            exists = True
            break

    if not exists:
        raise e.NotFound(info=new_name)


def check_update_type_activity(ID: int, active: bool) -> None:
    must_positive_int(int_=ID, max_length=None)
    must_bool(bool_=active)

    data = s_h.select_handler.get_all_single_type()
    exists: bool = False
    for old_id, _, _, old_active, _ in data:
        if old_id == ID:
            if old_active == active:
                raise e.NoChance(info="Type Aktivität")
            exists = True
            break

    if not exists:
        raise e.NotFound(info="Typ Aktivität")


# member
def check_update_member(data: dict) -> None:
    must_dict(dict_=data)
    _must_multiple_str_in_dict([
        "first_name",
        "last_name",
        "street",
        "number",
        "city",
        "country",
        "maps",
        "zip_code",
    ], data)

    if data['membership_type'] is not None:
        must_membership_type(data['membership_type'])

    if data["comment_text"] is not None:
        must_str(str_=data["comment_text"], length=2000)

    keys: list = [
        "birth_date",
        "entry_date",
    ]
    for key in keys:
        if data[key] is not None:
            must_int(int_=data[key])

    if data["special_member"] is not None:
        must_bool(bool_=data["special_member"])


# member nexus
def check_update_member_nexus(data: list, type_: str) -> None:
    try:
        must_list(data)
        must_length(4, data)

        ID, type_id, Type, value = data
        must_positive_int(type_id, max_length=None)

        if ID is not None:
            must_positive_int(ID, max_length=None)

        if Type is not None:
            must_str(Type)

        match type_:
            case "phone":
                _check_update_member_nexus_phone(phone=value)
            case "mail":
                _check_update_member_nexus_mail(mail=value)
            case "position":
                _check_update_member_nexus_position(active=value)
            case _:
                raise e.CaseException(f"validation // type: {type_}")
    except e.GeneralError as error:
        debug.debug(item=debug_str, keyword="update_member_nexus", message=f"Error = {error.message}")


def _check_update_member_nexus_phone(phone: str) -> None:
    if phone is not None:
        must_str(phone)


def _check_update_member_nexus_mail(mail: str) -> None:
    if mail is not None:
        must_str(mail)


def _check_update_member_nexus_position(active: bool) -> None:
    if active is not None:
        must_bool(active)


# User
def check_add_update_user(data: dict) -> None:
    must_dict(dict_=data)
    if data["ID"] is not None:
        must_positive_int(int_=data["ID"], max_length=None)
        must_default_user(ID=data["ID"], same=False)
        must_current_user(ID=data["ID"], same=True)

    if data["ID"] is None or data["password_1"] is not None:
        password_validation.must_password(password_1=data["password_1"], password_2=data["password_2"])

    _must_multiple_str_in_dict([
        "firstname",
        "lastname",
        "street",
        "number",
        "city",
        "country",
        "phone",
        "mail",
        "position",
        "zip_code",
    ], data)


def check_delete_user(ID: int, active: bool) -> None:
    must_positive_int(int_=ID)
    must_bool(bool_=active)
    must_current_user(ID=ID, same=not active)
    must_default_user(ID=ID, same=False)
    must_current_contact_person(ID=ID, same=False)


def must_current_user(ID: int, same: bool) -> None:
    if (ID == c.config.user['ID']) != same:
        raise e.CurrentUserException()


def must_default_user(ID: int, same: bool) -> None:
    if (ID == c.config.user['default_user_id']) != same:
        raise e.DefaultUserException()


def must_current_contact_person(ID: int, same: bool) -> None:
    reference_data, _ = organisation_handler.get_organisation_data()
    if (ID == reference_data['contact_person'][0]) != same:
        raise e.CurrentContactPersonException(info=_get_combined_str(str_1=reference_data['contact_person'][1],
                                                                     str_2=reference_data['contact_person'][2]))


# organisation
def check_add_update_organisation(data: dict) -> None:
    must_dict(dict_=data)
    must_length(data=data, len_=14)

    _must_multiple_str_in_dict(keys=[
        "name",
        "street",
        "number",
        "zip_code",
        "city",
        "country",
        "bank_name",
        "bank_owner",
        "bank_IBAN",
        "bank_BIC",
        "web_link",
    ], data=data)

    if data["extra_text"] is not None:
        must_str(data["extra_text"], length=3000)
    keys: tuple = (
        "ID",
        "contact_person",
    )
    for key in keys:
        if data[key] is not None:
            must_positive_int(int_=data[key], max_length=None)


# pdf
def check_member_entry_letter_export(log_data: dict) -> None:
    must_dict(dict_=log_data)

    allowed_target_columns: tuple = (
        "membership_type",
        "active",
    )
    allowed: bool = False
    for allowed_target_column in allowed_target_columns:
        if log_data['target_table'] == "member":
            if log_data['target_column'] == allowed_target_column:
                allowed = True
                break

    if not allowed:
        raise e.WrongLetterType(info=log_data['display_name'])

    if log_data['target_column'] == "membership_type":
        if log_data['new_data'] is None or log_data['old_data'] is None:
            raise e.NoChance(info=log_data['display_name'])


# helper
def must_str(str_: str, length: int | None = 50) -> None:
    if not isinstance(str_, str) or len(str_.strip()) == 0:
        raise e.NoStr(info=str_)
    if length is not None:
        if len(str_.strip()) > length:
            raise e.ToLong(max_length=length, text=str_)


def must_membership_type(str_: str) -> None:
    if not isinstance(str_, str) or len(str_.strip()) == 0:
        raise e.NoMembership(info=str_)
    reference_data, _ = type_handler.get_single_raw_type_types(raw_type_id=c.config.raw_type_id['membership'],
                                                               active=True)
    not_found: bool = True
    for entry in reference_data:
        if str_ in entry:
            not_found = False
            break

    if not_found:
        raise e.NotFound(info=str_)


def must_bool(bool_: bool) -> None:
    if not isinstance(bool_, bool):
        raise e.NoBool(info=str(bool_))


def must_positive_int(int_: int, max_length: int | None = 15) -> None:
    if not isinstance(int_, int):
        raise e.NoInt(info=str(int_))
    if type(int_) == bool:
        raise e.NoInt(info=str(int_))
    if int_ <= 0:
        raise e.NoPositiveInt(info=str(int_))
    if max_length is not None and len(str(int_)) > max_length:
        raise e.ToLong(max_length=max_length, text=int_)


def must_int(int_: int, max_length: int | None = 15) -> None:
    if not isinstance(int_, int):
        raise e.NoInt(info=str(int_))
    if type(int_) == bool:
        raise e.NoInt(info=str(int_))
    if max_length is not None and len(str(int_)) > max_length:
        raise e.ToLong(max_length=max_length, text=int_)


def must_dict(dict_: dict) -> None:
    if not isinstance(dict_, dict):
        raise e.NoDict(str(dict_))


def must_list(list_: list) -> None:
    if not isinstance(list_, list):
        raise e.NoList(str(list_))


def must_length(len_: int, data) -> None:
    must_positive_int(len_)
    if not len(data) == len_:
        raise e.WrongLength(str(len_) + " // " + str(data))


def _must_multiple_str_in_dict(keys: list, data: dict) -> None:
    for key in keys:
        if data[key] is not None:
            must_str(str_=data[key])


def _get_combined_str(str_1: str, str_2: str) -> str:
    if str_1 and str_2:
        return f"{str_1} {str_2}"
    elif str_1:
        return str_1
    elif str_2:
        return str_2
    else:
        return "Kein Name vorhanden"
