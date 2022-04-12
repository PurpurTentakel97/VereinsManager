# Purpur Tentakel
# 11.04.2022
# VereinsManager / Log Handler

import sys
import datetime

from logic.sqlite import select_handler as s_h
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


# transform
def _transform_member_data(data: list, target_id: int) -> list:
    new_data: list = list()
    for entry_list in data:
        entry: dict = _transform_to_dict(data=entry_list)
        result = None
        match entry['target_table']:
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
    new_data = sorted(new_data, key=lambda x: [x['log_date'], x['target_table']], reverse=True)
    return new_data


def _transform_to_dict(data: tuple) -> dict:
    return {
        "ID": data[0],
        "target_table": data[1],
        "target_id": data[2],
        "log_date": data[3],
        "target_colum": data[4],
        "old_data": data[5],
        "new_data": data[6],
        "display_name": None,
    }


def _transform_member(data_entry: dict, target_id: int) -> dict | None:
    if not data_entry['target_id'] == target_id:
        return
    data_entry['log_date'] = _transform_timestamp_to_date(timestamp=data_entry['log_date'])

    reverence_entries: tuple = (
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
    for reverence_entry in reverence_entries:
        if data_entry['target_colum'] not in reverence_entry:
            continue
        reverence_target_column, display_name = reverence_entry
        match reverence_target_column:
            case 'country':
                data_entry['old_data'] = _transform_type_id_into_name(entry=data_entry['old_data'])
                data_entry['new_data'] = _transform_type_id_into_name(entry=data_entry['new_data'])
            case 'membership_type':
                data_entry['old_data'] = _transform_type_id_into_name(entry=data_entry['old_data'])
                data_entry['new_data'] = _transform_type_id_into_name(entry=data_entry['new_data'])
            case "b_day":
                data_entry['old_data'] = _transform_timestamp_to_date(timestamp=data_entry['old_data'])
                data_entry['new_data'] = _transform_timestamp_to_date(timestamp=data_entry['new_data'])
            case "entry_day":
                data_entry['old_data'] = _transform_timestamp_to_date(timestamp=data_entry['old_data'])
                data_entry['new_data'] = _transform_timestamp_to_date(timestamp=data_entry['new_data'])
            case "special_member":
                data_entry['old_data'] = _transform_bool_to_text(entry=data_entry['old_data'])
                data_entry['new_data'] = _transform_bool_to_text(entry=data_entry['new_data'])
            case "comment_text":
                data_entry['old_data'], data_entry['new_data'] = _transform_comment_text(
                    old_entry=data_entry['old_data'], new_entry=data_entry['new_entry'])

        data_entry['display_name'] = display_name

        return data_entry


def _transform_member_phone(data_entry: dict, target_id: int) -> dict | None:
    _, type_id, reference_target_id = s_h.select_handler.get_phone_number_by_ID(ID=data_entry['target_id'])
    if reference_target_id != target_id:
        return

    return _transform_member_nexus(data_entry=data_entry, type_id=type_id)


def _transform_member_mail(data_entry: dict, target_id: int) -> dict | None:
    _, type_id, reference_target_id = s_h.select_handler.get_mail_member_by_ID(ID=data_entry['target_id'])
    if reference_target_id != target_id:
        return

    return _transform_member_nexus(data_entry=data_entry, type_id=type_id)


def _transform_member_position(data_entry: dict, target_id: int) -> dict | None:
    _, type_id, reference_target_id = s_h.select_handler.get_position_member_by_ID(ID=data_entry['target_id'])
    if reference_target_id != target_id:
        return
    if data_entry['old_data'] is None or data_entry['new_data'] is None:
        return

    data_entry = _transform_member_nexus(data_entry=data_entry, type_id=type_id)
    data_entry['old_data'] = _transform_bool_to_text(entry=data_entry['old_data'])
    data_entry['new_data'] = _transform_bool_to_text(entry=data_entry['new_data'])
    return data_entry


def _transform_member_nexus(data_entry: dict, type_id: int) -> dict:
    data_entry['log_date'] = _transform_timestamp_to_date(timestamp=data_entry['log_date'])
    data_entry['display_name'] = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=type_id)[0]

    return data_entry


# helper
def _transform_timestamp_to_date(timestamp: int) -> str | None:
    if timestamp:
        return datetime.datetime.strftime(
            datetime.datetime(1970, 1, 1, 2, 0, 0) + datetime.timedelta(seconds=timestamp),
            c.config.date_format['short'])


def _transform_type_id_into_name(entry: int) -> str | None:
    if entry is None:
        return
    entry, _ = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=entry)
    return entry


def _transform_bool_to_text(entry: int) -> str:
    if entry == 1:
        entry = "Ja"
    else:
        entry = "Nein"
    return entry


def _transform_comment_text(old_entry: str, new_entry: str) -> [str | None, str | None]:
    if old_entry or new_entry is None:
        return old_entry, new_entry
    if len(new_entry) > 20:
        index: int = 0
        for new_character, old_character in zip(new_entry, old_entry):
            if old_character != new_character:
                index = new_entry.index(new_character)
                break
        new_entry = new_entry[index:]
        old_entry = old_entry[index:]
        if len(new_entry) > 20:
            new_entry = new_entry[:20]
        if len(old_entry) > 20:
            old_entry = old_entry[:20]

    return old_entry, new_entry
