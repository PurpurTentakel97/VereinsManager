# Purpur Tentakel
# 21.01.2022
# VereinsManager / Base Window

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

app: QApplication | None = None


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_base_window_information()
        self._set_menu()

    def _set_base_window_information(self) -> None:
        pass

    def _set_menu(self) -> None:
        pass

    def set_widget(self, widget) -> None:
        self.setCentralWidget(widget)

    def set_error_bar(self, message: str) -> None:
        self.statusBar().showMessage("ERROR: " + message, 10000)

    def set_info_bar(self, message: str) -> None:
        self.statusBar().showMessage("Info: " + message, 2000)

    @staticmethod
    def save_permission(window_name:str) -> bool:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"{window_name} wird geschlossen.")
        msg.setInformativeText("Du hast ungespeicherte Daten. Möchtest du diese Daten vorher speichern?")
        msg.setWindowTitle("Daten Speichern?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes


def create_application():
    global app
    app = QApplication(sys.argv)


def run_application():
    global app
    app.exec_()
