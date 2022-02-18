# Purpur Tentakel
# 21.01.2022
# VereinsManager / Base Window

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from config.error_code import ErrorCode

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

    def set_status_bar(self, massage: str) -> None:
        self.statusBar().showMessage("Info: " + massage, 5000)

    def handle_error_code(self, error_code: ErrorCode, type_: str) -> None:
        match error_code:
            # Success
            case ErrorCode.OK_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Erfolgreich: {type_}")
            case ErrorCode.LOAD_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Erfolgreich geladen: {type_}")
            case ErrorCode.ADD_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Erfolgreich hinzugefügt: {type_}")
            case ErrorCode.UPDATE_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Erfolgreich geupdatet: {type_}")
            case ErrorCode.ACTIVE_SET_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Aktivität erfolgreich gesetzt: {type_}")
            case ErrorCode.DELETE_S:
                self.set_status_bar(massage=f"Error: {error_code.value} // Erfolgreich gelöscht: {type_}")

            # Operational Error
            case ErrorCode.LOAD_E:
                self.set_status_bar(massage=f"Error: {error_code.value} // Laden fehlgeschlagen: {type_}")
            case ErrorCode.ADD_E:
                self.set_status_bar(massage=f"Error: {error_code.value} // Hinzufügen fehlgeschlagen: {type_}")
            case ErrorCode.UPDATE_E:
                self.set_status_bar(massage=f"Error: {error_code.value} // Update fehlgeschlagen: {type_}")
            case ErrorCode.ACTIVE_SET_E:
                self.set_status_bar(
                    massage=f"Error: {error_code.value} // Aktivität konnte nicht geändert werden: {type_}")
            case ErrorCode.DELETE_E:
                self.set_status_bar(massage=f"Error: {error_code.value} // Löschen fehlgeschlagen: {type_}")

            # Database
            case ErrorCode.F_KEY_E:
                self.set_status_bar(
                    massage=f"Error: {error_code.value} // In anderen Datensätzden noch in Verwändung: {type_}")

            # Input Error
            case ErrorCode.NO_CHANCE:
                self.set_status_bar(massage=f"Error: {error_code.value} // Keine Änderung der Daten: {type_}")

            # Default
            case _:
                self.set_status_bar(
                    massage=f"Error: {error_code.value} // Fehlgeschlagen: Unbekannter Fehler (Error Code = {error_code.value})")


def create_application():
    global app
    app = QApplication(sys.argv)


def run_application():
    global app
    app.exec_()
