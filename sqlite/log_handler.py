# Purpur Tentakel
# 07.02.2022
# VereinsManager / Handler Log

from datetime import date

from sqlite import sql_database
from enum_sheet import TableTypes, date_format


def log_initial_data(new_data, type_: str, member_id: int, time_stamp: date):
    sql_database.database.log.log_data(member_id=member_id, log_type=type_, log_date=time_stamp, old_data=None,
                                       new_data=new_data)


def _log_data(new_data, old_data, type_: str, member_id: int, time_stamp: date):
    sql_database.database.log.log_data(member_id=member_id, log_type=type_, log_date=time_stamp, old_data=old_data,
                                       new_data=new_data)


def log_data(reference_data: tuple, output, time_stamp: date, table_type: TableTypes) -> None:
    match table_type:
        case TableTypes.MEMBER:
            _log_member(reference_data=reference_data, output=output, time_stamp=time_stamp)
        case TableTypes.MEMBER_PHONE:
            _log_member_phone(reference_data=reference_data, output=output, time_stamp=time_stamp)
        case TableTypes.MEMBER_MAIL:
            _log_member_mail(reference_data=reference_data, output=output, time_stamp=time_stamp)
        case TableTypes.MEMBER_POSITION:
            _log_member_position(reference_data=reference_data, output=output, time_stamp=time_stamp)


def _log_member(reference_data: tuple, output: dict, time_stamp: date) -> None:
    if reference_data is None:
        return
    member_id = reference_data[0]
    output_items = list(output.items())
    for i in range(1, len(reference_data) - 1):
        old_data = reference_data[i]
        type_, new_data = output_items[i]
        if type(new_data) == date:
            new_data = new_data.strftime(date_format)
        if reference_data[i] != new_data:
            _log_data(new_data=new_data, old_data=reference_data[i], type_=type_, member_id=member_id,
                      time_stamp=time_stamp)


def _log_member_phone(reference_data: tuple, output: tuple, time_stamp: date) -> None:
    if reference_data is None:
        return
    member_phone_id, member_id, type_id, old_data = reference_data
    _, _, type_, new_data = output
    if new_data != old_data:
        _log_data(new_data=new_data, old_data=old_data, type_=type_, member_id=member_id, time_stamp=time_stamp)


def _log_member_mail(reference_data: tuple, output: tuple, time_stamp: date) -> None:
    if reference_data is None:
        return
    member_phone_id, member_id, type_id, old_data = reference_data
    _, _, type_, new_data = output
    if new_data != old_data:
        _log_data(new_data=new_data, old_data=old_data, type_=type_, member_id=member_id, time_stamp=time_stamp)


def _log_member_position(reference_data: tuple, output: tuple, time_stamp: date) -> None:
    if reference_data is None:
        return
    member_position_id, member_id, type_id = reference_data
    _, _, type_, active = output
    if not active:
        _log_data(new_data=None, old_data=type_, type_=type_, member_id=member_id, time_stamp=time_stamp)
