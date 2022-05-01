# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main Window

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QMessageBox

from ui import window_manager as w
from ui.windows.base_window import BaseWindow
from ui.windows.member_windows import members_window as m_w
from ui.windows import types_window, user_window, user_verify_window, organisation_data_window, \
    export_window

import debug

debug_str: str = "Main Window"


class MainWindow(BaseWindow):
    def __init__(self, default_user: bool):
        super().__init__()
        self.default_user: bool = not default_user

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._set_default_user()

    def _create_ui(self) -> None:
        self._members_btn: QPushButton = QPushButton()
        self._members_btn.setText("Mitglieder")
        self._members_btn.clicked.connect(self._open_members)

        self._performance_btn: QPushButton = QPushButton()
        self._performance_btn.setText("Auftritte")
        self._performance_btn.clicked.connect(self._open_performances)

        self._my_job_btn: QPushButton = QPushButton()
        self._my_job_btn.setText("Meine Aufgaben")
        self._my_job_btn.clicked.connect(self._open_my_jobs)

        self._job_btn: QPushButton = QPushButton()
        self._job_btn.setText("Aufgaben")
        self._job_btn.clicked.connect(self._open_jobs)

        self._edit_types_btn: QPushButton = QPushButton()
        self._edit_types_btn.setText("Typen bearbeiten")
        self._edit_types_btn.clicked.connect(self._open_edit_types)

        self._user_data_btn: QPushButton = QPushButton()
        self._user_data_btn.setText("Benutzer Daten")
        self._user_data_btn.clicked.connect(self._open_user_data)

        self._export_pdf_btn: QPushButton = QPushButton()
        self._export_pdf_btn.setText("PDF Export")
        self._export_pdf_btn.clicked.connect(self._open_export_pdf)

        self._chance_user_btn: QPushButton = QPushButton()
        self._chance_user_btn.setText("Benutzer wechseln")
        self._chance_user_btn.clicked.connect(self._open_chance_user)

        self._chance_organization_btn: QPushButton = QPushButton()
        self._chance_organization_btn.setText("Organisation wechseln")
        self._chance_organization_btn.clicked.connect(self._open_chance_organization)

        self._organization_data_btn: QPushButton = QPushButton()
        self._organization_data_btn.setText("Organisations Daten")
        self._organization_data_btn.clicked.connect(self._open_organisation_data)

    def _create_layout(self) -> None:
        row: int = 0
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._members_btn, row, 0)
        row += 1
        grid.addWidget(self._my_job_btn, row, 0)
        grid.addWidget(self._job_btn, row, 1)
        row += 1
        grid.addWidget(self._performance_btn, row, 0)
        grid.addWidget(self._edit_types_btn, row, 1)
        row += 1
        grid.addWidget(self._user_data_btn, row, 0)
        grid.addWidget(self._export_pdf_btn, row, 1)
        row += 1
        grid.addWidget(self._chance_user_btn, row, 0)
        grid.addWidget(self._chance_organization_btn, row, 1)
        row += 1
        grid.addWidget(self._organization_data_btn, row, 0)

        widget: QWidget = QWidget()
        widget.setLayout(grid)

        self.set_widget(widget)
        self.show()

    @staticmethod
    def _get_close_permission() -> bool:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Alle Fenster Schließen?")
        msg.setInformativeText("Du hast möglicherweise ungespeicherte Daten. Die Daten können verloren gehen.")
        msg.setWindowTitle("Trotzdem Schließen?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    def _set_window_information(self) -> None:
        self.setWindowTitle("Hauptfenster - Vereinsmanager")

    def _set_default_user(self) -> None:
        buttons: tuple = (
            self._members_btn,
            self._job_btn,
            self._my_job_btn,
            self._performance_btn,
            self._edit_types_btn,
            self._export_pdf_btn,
            self._organization_data_btn,
        )

        for button in buttons:
            button: QPushButton
            button.setEnabled(self.default_user)

    def _open_members(self) -> None:
        result, valid = w.window_manger.is_valid_member_window()
        if not valid:
            self.set_info_bar(message=result)
            return

        w.window_manger.members_window = m_w.MembersWindow()

    def _open_my_jobs(self) -> None:
        debug.debug(item=debug_str, keyword="_open_my_jobs", message=f"my jobs open")

    def _open_jobs(self) -> None:
        debug.debug(item=debug_str, keyword="_open_jobs", message=f"open jobs")

    def _open_performances(self) -> None:
        debug.debug(item=debug_str, keyword="_open_performances", message=f"performances open")

    def _open_edit_types(self) -> None:
        result, valid = w.window_manger.is_valid_types_window()
        if not valid:
            self.set_info_bar(message=result)
            return

        w.window_manger.types_window = types_window.TypesWindow()

    def _open_user_data(self) -> None:
        result, valid = w.window_manger.is_valid_user_window()
        if not valid:
            self.set_error_bar(message=result)
            return

        w.window_manger.user_window = user_window.UserWindow()

    def _open_export_pdf(self) -> None:
        result, valid = w.window_manger.is_valid_export_window()
        if not valid:
            self.set_error_bar(message=result)
            return

        w.window_manger.export_window = export_window.ExportWindow()

    def _open_chance_user(self) -> None:
        self.close()
        if not w.window_manger.is_main_window():
            user_verify_window.create()

    def _open_chance_organization(self):
        debug.debug(item=debug_str, keyword="_open_chance_organization", message=f"chance database")

    def _open_organisation_data(self) -> None:
        result, valid = w.window_manger.is_valid_organisation_data_window()
        if not valid:
            self.set_error_bar(message=result)
            return

        w.window_manger.organisation_data_window = organisation_data_window.OrganisationDataWindow()

    def closeEvent(self, event) -> None:
        event.ignore()
        if not w.window_manger.is_valid_close_main_window():
            if self._get_close_permission():
                counter: int = 0
                while not w.window_manger.is_valid_close_main_window():
                    w.window_manger.close_all_window()
                    counter += 1
                    if counter >= 3:
                        self.set_error_bar("Programm konnte nicht geschlossen werden.")
                        return
                w.window_manger.main_window = None
                event.accept()
        else:
            w.window_manger.close_all_window()
            w.window_manger.main_window = None
            event.accept()


def create(default_user: bool) -> None:
    w.window_manger.main_window = MainWindow(default_user=default_user)
