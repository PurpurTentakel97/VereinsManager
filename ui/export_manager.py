# Purpur Tentakel
# 26.04.2022
# VereinsManager / Export Manager

import os

from PyQt5.QtWidgets import QFileDialog

import transition
from config import config_sheet as c
from ui.windows.base_window import BaseWindow


def export_member_anniversary(index: int, year: int) -> tuple[str, bool]:
    transition.create_default_dir("member_anniversary")
    file = c.config.files['member_anniversary_pdf']
    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs['save'],
                                                           c.config.dirs['organisation'],
                                                           c.config.dirs['export'],
                                                           c.config.dirs['member'],
                                                           c.config.dirs['member_anniversary'],
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False
    message, result = "", True
    match index:
        case 0:
            message, result = transition.get_member_anniversary_pdf(path=file)
        case 1:
            message, result = transition.get_member_anniversary_pdf(path=file, year=year)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_log(name: str, ID: int, active: bool) -> tuple[str, bool]:
    transition.create_default_dir("member_log")

    name = name.replace(" ", "_")
    file = c.config.files['member_log_pdf']
    file = file.replace('<name>', name)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs['save'],
                                                           c.config.dirs['organisation'],
                                                           c.config.dirs['export'],
                                                           c.config.dirs['member'],
                                                           c.config.dirs['member_log'],
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    message, valid = transition.get_member_log_pdf(ID=ID, path=file,
                                                   active=active)
    if not valid:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_letter(name: str, ID: int, active: bool, log_id: int) -> tuple[str, bool]:
    transition.create_default_dir("member_letter")

    file: str = c.config.files['member_letter_pdf']
    file = file.replace('<name>', name)

    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs['save'],
                                                           c.config.dirs['organisation'],
                                                           c.config.dirs['export'],
                                                           c.config.dirs['member'],
                                                           c.config.dirs['member_letter'],
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    message, valid = transition.get_member_entry_letter_pdf(ID=ID, path=file, active=active, log_id=log_id)
    if not valid:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_table() -> tuple[str, bool]:
    transition.create_default_dir("member_list")
    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(), c.config.dirs['save'],
                                                           c.config.dirs['organisation'],
                                                           c.config.dirs['export'],
                                                           c.config.dirs['member'],
                                                           c.config.dirs['member_list'],
                                                           c.config.files['member_table_pdf']),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    message, result = transition.get_member_table_pdf(file)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True


def export_member_card(first_name: str, last_name: str, ID: int) -> tuple[str, bool]:
    transition.create_default_dir("member_card")
    file: str = c.config.files['member_card_pdf']
    file = file.replace('<first_name>', first_name)
    file = file.replace('<last_name>', last_name)
    file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                              os.path.join(os.getcwd(),
                                                           c.config.dirs['save'],
                                                           c.config.dirs['organisation'],
                                                           c.config.dirs['export'],
                                                           c.config.dirs['member'],
                                                           c.config.dirs['member_card'],
                                                           file),
                                              "PDF (*.pdf);;All Files (*)")
    if not check:
        return "Export abgebrochen", False

    message, result = transition.get_member_card_pdf(ID=ID, path=file)

    if not result:
        return message, False

    if BaseWindow.is_open_permission():
        transition.open_latest_export()

    return "Export abgeschlossen", True
