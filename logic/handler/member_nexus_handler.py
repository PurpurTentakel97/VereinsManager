# Purpur Tentakel
# 28.03.2022
# VereinsManager / Member Nexus Handler

from sqlite import add_handler as a_h, select_handler as s_h, update_handler as u_h, log_handler as l_h, \
    delete_handler as d_h, statistics_handler as st_h
from logic import validation as v
from config import config_sheet as c
import debug

debug_str: str = "Member Nexus Handler"


# no try / catch -> try / catch in member_handler.py


# add
def _add_member_nexus_phone(type_id: int, value: str, member_id: int, log_date: int | None) -> int:
    ID = a_h.add_handler.add_member_nexus_phone(type_id=type_id, value=value, member_id=member_id, log_date=log_date)
    st_h.statistics_handler.statistics(type_="phone", raw_type_id=c.config.raw_type_id["phone"],
                                       new_type_id=type_id, new_data=value)
    return ID


def _add_member_nexus_mail(type_id: int, value: str, member_id: int, log_date: int | None) -> int:
    ID = a_h.add_handler.add_member_nexus_mail(type_id=type_id, value=value, member_id=member_id, log_date=log_date)
    st_h.statistics_handler.statistics(type_="mail", raw_type_id=c.config.raw_type_id["mail"],
                                       new_type_id=type_id, new_data=value)
    return ID


def _add_member_nexus_position(type_id: int, value: bool, member_id: int, log_date: int | None) -> int:
    ID = a_h.add_handler.add_member_nexus_position(type_id=type_id, value=value, member_id=member_id,
                                                   log_date=log_date)
    st_h.statistics_handler.statistics(type_="position", raw_type_id=c.config.raw_type_id["position"],
                                       new_type_id=type_id, new_data=value)
    return ID


# get
def get_phone_number_by_member_id(member_id: int) -> tuple:
    v.must_positive_int(int_=member_id, max_length=None)
    phone_data = s_h.select_handler.get_phone_number_by_member_id(member_id=member_id)
    types = s_h.select_handler.get_single_raw_type_types(raw_type_id=c.config.raw_type_id['phone'], active=True)
    checked_phone_data: list = list()
    for entry in phone_data:
        _, type_id, *_ = entry
        for type_id_, *_ in types:
            if type_id == type_id_:
                checked_phone_data.append(entry)

    return tuple(checked_phone_data)


def get_mail_by_member_id(member_id: int) -> tuple:
    v.must_positive_int(int_=member_id, max_length=None)
    mail_data = s_h.select_handler.get_mail_by_member_id(member_id=member_id)
    types = s_h.select_handler.get_single_raw_type_types(raw_type_id=c.config.raw_type_id['mail'], active=True)
    checked_mail_data: list = list()
    for entry in mail_data:
        _, type_id, *_ = entry
        for type_id_, *_ in types:
            if type_id == type_id_:
                checked_mail_data.append(entry)
    return tuple(checked_mail_data)


def get_position_by_member_id(member_id: int) -> tuple:
    v.must_positive_int(int_=member_id, max_length=None)
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
def update_add_member_nexus(data: dict, member_id: int, log_date: int | None) -> dict:
    v.must_dict(data)

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
        v.update_member_nexus(data=[ID, type_id, Type, phone_number], type_="phone")

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
        v.update_member_nexus(data=[ID, type_id, Type, mail_], type_="mail")

        if ID is None:
            new_ID = _add_member_nexus_mail(type_id=type_id, value=mail_, member_id=member_id, log_date=log_date)
        else:
            new_ID = _update_member_nexus_mail(ID=ID, mail=mail_, log_date=log_date)
        mail_ids.append(new_ID)

    return mail_ids


def _update_add_member_nexus_position(position: list, member_id: int, log_date: int) -> list:
    position_ids: list = list()
    for ID, type_id, Type, active in position:
        v.update_member_nexus(data=[ID, type_id, Type, active], type_="position")

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
    st_h.statistics_handler.statistics(type_="phone", raw_type_id=c.config.raw_type_id['phone'],
                                       new_type_id=reference_data[1], new_data=number, old_data=reference_data[0])


def _update_member_nexus_mail(ID: int, mail: str, log_date: int) -> None:  # no Validation
    reference_data = s_h.select_handler.get_mail_member_by_ID(ID=ID)
    u_h.update_handler.update_member_nexus_mail(ID=ID, mail=mail)
    l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=mail, log_date=log_date,
                                     type_="mail")
    st_h.statistics_handler.statistics(type_="mail", raw_type_id=c.config.raw_type_id['mail'],
                                       new_type_id=reference_data[1], new_data=mail, old_data=reference_data[0])


def _update_member_nexus_position(ID: int, active: bool, log_date: int) -> None:  # no Validation
    reference_data = s_h.select_handler.get_position_member_by_ID(ID=ID)
    u_h.update_handler.update_member_nexus_position(ID=ID, active=active)
    l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=active, log_date=log_date,
                                     type_="position")
    st_h.statistics_handler.statistics(type_="position", raw_type_id=c.config.raw_type_id['position'],
                                       new_type_id=reference_data[1], new_data=active, old_data=reference_data[0])


def update_member_nexus_activity(member_id: int, active: bool) -> None:
    _update_member_nexus_activity_phone(member_id=member_id, active=active)
    _update_member_nexus_activity_mail(member_id=member_id, active=active)
    _update_member_nexus_activity_position(member_id=member_id, active=active)


def _update_member_nexus_activity_phone(member_id: int, active: bool) -> None:
    reference_data: tuple = s_h.select_handler.get_phone_number_by_member_id(member_id=member_id)
    u_h.update_handler.update_member_active_phone(member_id=member_id, active=active)
    for ID, type_id, _ in reference_data:
        if s_h.select_handler.get_phone_number_by_ID(ID=ID)[0]:
            st_h.statistics_handler.statistics(type_="phone", raw_type_id=c.config.raw_type_id['phone'],
                                               new_type_id=type_id, new_data=active, old_data=not active)


def _update_member_nexus_activity_mail(member_id: int, active: bool) -> None:
    reference_data: tuple = s_h.select_handler.get_mail_by_member_id(member_id=member_id)
    u_h.update_handler.update_member_active_mail(member_id=member_id, active=active)
    for ID, type_id, _ in reference_data:
        if s_h.select_handler.get_mail_member_by_ID(ID=ID)[0]:
            st_h.statistics_handler.statistics(type_="mail", raw_type_id=c.config.raw_type_id['mail'],
                                               new_type_id=type_id, new_data=active, old_data=not active)


def _update_member_nexus_activity_position(member_id: int, active: bool) -> None:
    reference_data: tuple = s_h.select_handler.get_position_by_member_id(member_id=member_id)
    u_h.update_handler.update_member_active_position(member_id=member_id, active=active)
    for ID, type_id, _ in reference_data:
        if s_h.select_handler.get_position_member_by_ID(ID=ID)[0]:
            st_h.statistics_handler.statistics(type_="position", raw_type_id=c.config.raw_type_id['position'],
                                               new_type_id=type_id, new_data=active, old_data=not active)


# delete
def delete_inactive_member_nexus(member_id: int) -> None:
    _delete_inactive_member_phone(member_id=member_id)
    _delete_inactive_member_mail(member_id=member_id)
    _delete_inactive_member_position(member_id=member_id)


def _delete_inactive_member_phone(member_id: int) -> None:
    reference_data = s_h.select_handler.get_phone_number_by_member_id(member_id=member_id)
    for ID, *_ in reference_data:
        l_h.log_handler.delete_log(target_id=ID, target_table="member_phone")
    d_h.delete_handler.delete_member_phone(member_id=member_id)


def _delete_inactive_member_mail(member_id: int) -> None:
    reference_data = s_h.select_handler.get_mail_by_member_id(member_id=member_id)
    for ID, *_ in reference_data:
        l_h.log_handler.delete_log(target_id=ID, target_table="member_mail")
    d_h.delete_handler.delete_member_mail(member_id=member_id)


def _delete_inactive_member_position(member_id: int) -> None:
    reference_data = s_h.select_handler.get_position_by_member_id(member_id=member_id)
    for ID, *_ in reference_data:
        l_h.log_handler.delete_log(target_id=ID, target_table="member_position")
    d_h.delete_handler.delete_member_position(member_id=member_id)
