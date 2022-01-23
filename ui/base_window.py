# Purpur Tentakel
# 21.01.2022
# VereinsManager / Base Window

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

app: QApplication | None = None


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_base_window_information()
        self._set_menu()
        self.user: str = "Traijan__"

    def _set_base_window_information(self) -> None:
        pass

    def _set_menu(self) -> None:
        pass

    def set_widget(self, widget) -> None:
        self.setCentralWidget(widget)

    def set_status_bar(self, massage: str) -> None:
        self.statusBar().showMessage("Info: " + massage, 5000)


def create_application():
    global app
    app = QApplication(sys.argv)


def run_application():
    global app
    app.exec_()
