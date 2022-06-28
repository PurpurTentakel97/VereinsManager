# Purpur Tentakel
# 26.04.2022
# VereinsManager / Export Manager

import os
from datetime import datetime

from PyQt5.QtWidgets import QFileDialog

import transition
from config import config_sheet as c
from ui.base_window import BaseWindow


def _add_date_to_filename(file_name: str, first_name: str = None, last_name: str = None, name: str = None) -> str:
    if first_name:
        first_name = first_name.replace(" ", "_")
        file_name = file_name.replace('<first_name>', first_name)
    if last_name:
        last_name = last_name.replace(" ", "_")
        file_name = file_name.replace('<last_name>', last_name)
    if name:
        name = name.replace(" ", "_")
        file_name = file_name.replace('<name>', name)

    file_name += "_" + datetime.strftime(datetime.now(), c.config.date_format.short_save)
    file_name = file_name.replace(" ", "_")
    return file_name


def _delete_date_from_filename(file_name: str) -> str:
    file_type = file_name.split(".")[-1]
    file_name = file_name[:-(len(file_type) + 1)]  # remove filetype

    if file_name[-c.config.date_format.short_length:] == datetime.strftime(datetime.now(),
                                                                              c.config.date_format.short_save):
        file_name = file_name[:-(c.config.date_format.short_length + 1)]

    return file_name


def export_member_anniversary(index: int, year: int) -> tuple[str, bool]:
    transition.create_default_dir("member_anniversary")

    file = c.config.files.member_anniversary_pdf
    if index == 1:
        file += "_" + str(year)
    file = _add_date_to_filename(file_name=file)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.member,
                                                           c.config.dirs.member_anniversary,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, result = "", True
    match index:
        case 0:
            message, result = transition.create_member_anniversary_pdf(path=file)
        case 1:
            message, result = transition.create_member_anniversary_pdf(path=file, year=year)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_log(name: str, ID: int, active: bool) -> tuple[str, bool]:
    transition.create_default_dir("member_log")
    file = _add_date_to_filename(file_name=c.config.files.member_log_pdf, name=name)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.member,
                                                           c.config.dirs.member_log,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, valid = transition.create_member_log_pdf(ID=ID, path=file,
                                                      active=active)
    if not valid:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_letter(name: str, ID: int, active: bool, log_id: int, letter_id: int) -> tuple[str, bool]:
    transition.create_default_dir("member_letter")

    match letter_id:
        case 1:
            file: str = _add_date_to_filename(file_name=c.config.files.member_letter_active_pdf, name=name)
        case 2:
            file: str = _add_date_to_filename(file_name=c.config.files.member_letter_membership_pdf, name=name)
        case _:
            file: str = "No filename found"

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.member,
                                                           c.config.dirs.member_letter,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, valid = transition.create_member_entry_letter_pdf(ID=ID, path=file, active=active, log_id=log_id)
    if not valid:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_table() -> tuple[str, bool]:
    transition.create_default_dir("member_list")
    file = _add_date_to_filename(file_name=c.config.files.member_table_pdf)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(), c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.member,
                                                           c.config.dirs.member_list,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, result = transition.create_member_table_pdf(file)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_card(first_name: str, last_name: str, ID: int) -> tuple[str, bool]:
    transition.create_default_dir("member_card")
    file = _add_date_to_filename(file_name=c.config.files.member_card_pdf, first_name=first_name,
                                 last_name=last_name)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.member,
                                                           c.config.dirs.member_card,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, result = transition.create_member_card_pdf(ID=ID, path=file)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_location(name: str, ID: int) -> tuple[str, bool]:
    transition.create_default_dir("location")
    file = _add_date_to_filename(file_name=c.config.files.location_pdf, name=name)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs.save,
                                                           c.config.dirs.organisation,
                                                           c.config.dirs.export,
                                                           c.config.dirs.location,
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    file = _delete_date_from_filename(file_name=file)
    message, result = transition.create_location_pdf(ID=ID, path=file)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True
