# Purpur Tentakel
# 11.04.2022
# VereinsManager / Log Handler

import sys
import datetime

from sqlite import select_handler as s_h
from config import exception_sheet as e, config_sheet as c
import debug

debug_str: str = "Log Handler"


def get_log_member_data(target_id: int) -> [str | tuple, bool]:
    try:
        data = s_h.select_handler.get_log_data()
        new_data = _transform_member_data(data=data, target_id=target_id)
        return new_data, True
    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_log_data", error_=sys.exc_info())
        return error.message, False


def _transform_member_data(data: list, target_id: int) -> list:
    new_data: list = list()
    for entry in data:
        entry = list(entry)
        result = None
        match entry[0]:
            case "member":
                result = _transform_member(data_entry=entry, target_id=target_id)
            case 'member_phone':
                result = _transform_member_phone(data_entry=entry, target_id=target_id)
            case 'member_mail':
                result = _transform_member_mail(data_entry=entry, target_id=target_id)
            case 'member_position':
                result = _transform_member_position(data_entry=entry, target_id=target_id)

        if result:
            new_data.append(result)
    new_data = sorted(new_data, key=lambda x: [x[0], x[1]], reverse=True)
    return new_data


def _transform_member(data_entry: list, target_id: int) -> list | None:
    if not data_entry[1] == target_id:
        return
    data_entry = data_entry[2:]
    data_entry[0] = _transform_timestamp_to_date(timestamp=data_entry[0])

    reverence_entrys: tuple = (
        ("first_name", "Vorname"),
        ("last_name", "Nachname"),
        ("street", "Straße"),
        ("number", "Hausnummer"),
        ("zip_code", "PLZ"),
        ("city", "Stadt"),
        ("country", "Land"),
        ("maps", "Maps-Link"),
        ("b_day", "Geburtstag"),
        ("entry_day", "Eintritt"),
        ("membership_type", "Mitgliedsart"),
        ("special_member", "Ehrenmitglied"),
        ("comment_text", "Kommantar"),
    )
    for reverence_entry in reverence_entrys:
        if data_entry[1] not in reverence_entry:
            continue
        type_, name = reverence_entry
        match type_:
            case 'country':
                data_entry = _transform_type_id_into_name(entry=data_entry)
            case 'membership_type':
                data_entry = _transform_type_id_into_name(entry=data_entry)
            case "b_day":
                data_entry[2] = _transform_timestamp_to_date(timestamp=data_entry[2])
                data_entry[3] = _transform_timestamp_to_date(timestamp=data_entry[3])
            case "entry_day":
                data_entry[2] = _transform_timestamp_to_date(timestamp=data_entry[2])
                data_entry[3] = _transform_timestamp_to_date(timestamp=data_entry[3])
            case "special_member":
                data_entry = _transform_special_member_to_text(entry=data_entry)
            case "comment_text":
                data_entry = _transform_comment_text(entry=data_entry)

        data_entry[1] = name

        return data_entry


def _transform_member_phone(data_entry: list, target_id: int) -> list | None:
    _, type_id, reference_target_id = s_h.select_handler.get_phone_number_by_ID(ID=data_entry[1])
    if reference_target_id != target_id:
        return

    return _transform_member_nexus(data_entry=data_entry, type_id=type_id)


def _transform_member_mail(data_entry: list, target_id: int) -> list | None:
    _, type_id, reference_target_id = s_h.select_handler.get_mail_member_by_ID(ID=data_entry[1])
    if reference_target_id != target_id:
        return

    return _transform_member_nexus(data_entry=data_entry, type_id=type_id)


def _transform_member_position(data_entry: list, target_id: int) -> list | None:
    _, type_id, reference_target_id = s_h.select_handler.get_position_member_by_ID(ID=data_entry[1])
    if reference_target_id != target_id:
        return
    if data_entry[4] is None or data_entry[5] is None:
        return

    data_entry = _transform_member_nexus(data_entry=data_entry, type_id=type_id)
    data_entry = _transform_special_member_to_text(entry=data_entry)
    return data_entry


def _transform_member_nexus(data_entry: list, type_id: int) -> list:
    data_entry = data_entry[2:]
    data_entry[0] = _transform_timestamp_to_date(timestamp=data_entry[0])
    data_entry[1] = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]

    return data_entry


# helper
def _transform_timestamp_to_date(timestamp: int) -> str | None:
    if timestamp:
        return datetime.datetime.strftime(
            datetime.datetime(1970, 1, 1, 2, 0, 0) + datetime.timedelta(seconds=timestamp),
            c.config.date_format['short'])


def _transform_type_id_into_name(entry: list) -> list:
    for index in range(2, 4):
        if entry[index] is None:
            continue
        entry[index], _ = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=entry[index])
    return entry


def _transform_special_member_to_text(entry: list) -> list:
    for index in range(2, 4):
        if entry[index] == 1:
            entry[index] = "Ja"
        else:
            entry[index] = "Nein"
    return entry


def _transform_comment_text(entry: list) -> list:
    for index in range(2, 4):
        if entry[index] is None:
            continue
        if len(entry[index]) > 20:
            entry[index] = entry[index][:20]
    return entry
