# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main Window

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget, QMessageBox

from ui.windows.base_window import BaseWindow
from ui.windows import members_window as m_w, window_manager as w_m, types_window as t_w, user_window as u_w, \
    user_verify_window as u_v_w

import debug

debug_str: str = "Main Window"

main_window: "MainWindow"


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._set_window_information()
        self._set_ui()
        self._set_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Hauptfenster - Vereinsmanager")

    def _set_ui(self) -> None:
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

    def _set_layout(self) -> None:
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

        widget: QWidget = QWidget()
        widget.setLayout(grid)

        self.set_widget(widget)
        self.show()

    def _open_members(self) -> None:
        result, valid = w_m.window_manger.is_valid_member_window()
        if not valid:
            self.set_info_bar(message=result)
            return

        w_m.window_manger.members_window = m_w.MembersWindow()

    def _open_my_jobs(self) -> None:
        debug.info(item=debug_str, keyword="_open_my_jobs", message=f"my jobs open")

    def _open_jobs(self) -> None:
        debug.info(item=debug_str, keyword="_open_jobs", message=f"open jobs")

    def _open_performances(self) -> None:
        debug.info(item=debug_str, keyword="_open_performances", message=f"performances open")

    def _open_edit_types(self) -> None:
        result, valid = w_m.window_manger.is_valid_types_window()
        if not valid:
            self.set_info_bar(message=result)
            return

        w_m.window_manger.types_window = t_w.TypesWindow()

    def _open_user_data(self):
        result, valid = w_m.window_manger.is_valid_user_window()
        if not valid:
            self.set_error_bar(message=result)
            return

        w_m.window_manger.user_window = u_w.UserWindow()

    def _open_export_pdf(self):
        debug.info(item=debug_str, keyword="_open_export_pdf", message=f"pdf open")

    def _open_chance_user(self):
        u_v_w.create_user_verify_window()
        self.close()

    def _open_chance_organization(self):
        debug.info(item=debug_str, keyword="_open_chance_organization", message=f"chance database")

    def closeEvent(self, event) -> None:
        event.ignore()
        if not w_m.window_manger.is_valid_close_main_window():
            if self._get_close_permission():
                w_m.window_manger.close_all_window()
                event.accept()
        else:
            w_m.window_manger.close_all_window()
            event.accept()

    @staticmethod
    def _get_close_permission() -> bool:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Alle Fenster Schließen?")
        msg.setInformativeText("Du hast möglicherweise ungespeicherte Daten. Die Daten können verloren gehen.")
        msg.setWindowTitle("Trotzdem Schließen?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes


def create_main_window() -> None:
    global main_window
    main_window = MainWindow()
