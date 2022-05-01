# Purpur Tentakel
# 21.01.2022
# VereinsManager / Base Window

import sys
import os.path

from PyQt5.QtGui import QIcon
from PIL import Image, UnidentifiedImageError
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from config import config_sheet as c, exception_sheet as e

import debug

debug_str: str = "BaseWindow"

app: QApplication | None = None


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_base_window_information()
        self._create_menu()

    def _create_menu(self) -> None:
        pass

    def _set_base_window_information(self) -> None:
        if self.is_ui_icon():
            self.setWindowIcon(QIcon(c.config.get_icon_path()))
        else:
            self.setWindowIcon(QIcon(c.config.get_default_icon_path()))

    def set_widget(self, widget) -> None:
        self.setCentralWidget(widget)

    def set_error_bar(self, message: str) -> None:
        self.statusBar().showMessage("ERROR: " + message, 10000)

    def set_info_bar(self, message: str) -> None:
        self.statusBar().showMessage("Info: " + message, 2000)

    def is_ui_icon(self) -> bool:
        if not os.path.exists(c.config.get_icon_path()):
            return False
        try:
            image = Image.open(c.config.get_icon_path())
            if 1.05 > image.width / image.height > 0.95:
                return True
        except UnidentifiedImageError:
            self.set_error_bar(message="Umbekanntes Icon-Bildformat")
            return False

    @staticmethod
    def is_save_permission(window_name: str) -> bool:
        msg = QMessageBox()
        if BaseWindow.is_ui_icon(BaseWindow()):
            msg.setWindowIcon(QIcon(c.config.get_icon_path()))
        else:
            msg.setWindowIcon(QIcon(c.config.get_default_icon_path()))
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"{window_name} wird geschlossen.")
        msg.setInformativeText("Du hast ungespeicherte Daten. Möchtest du diese Daten vorher speichern?")
        msg.setWindowTitle("Daten Speichern?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    @staticmethod
    def is_open_permission() -> bool:
        msg = QMessageBox()
        if BaseWindow.is_ui_icon(BaseWindow()):
            msg.setWindowIcon(QIcon(c.config.get_icon_path()))
        else:
            msg.setWindowIcon(QIcon(c.config.get_default_icon_path()))
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"Neues PDF öffnen?")
        msg.setInformativeText("Das neue PDF kann geöffnet werden.")
        msg.setWindowTitle("PDF öffnen?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes


def create_application():
    try:
        global app
        app = QApplication(sys.argv)

    except:
        debug.error(item=debug_str, keyword=f"create_application", error_=sys.exc_info())
        debug.export_error()
        raise e.QuitException()


def run_application():
    try:
        global app
        app.exec_()

    except:
        debug.error(item=debug_str, keyword=f"create_application", error_=sys.exc_info())
        debug.export_error()
        raise e.QuitException()
