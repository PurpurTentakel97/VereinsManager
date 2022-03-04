# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main Window

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget

from ui.base_window import BaseWindow
from ui import members_window as m_w, types_window as t_w
from ui import window_manager as w

import debug

debug_str: str = "Main Window"


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

        self._old_members_btn: QPushButton = QPushButton()
        self._old_members_btn.setText("Ehmalige Mitglieder")
        self._old_members_btn.clicked.connect(self._open_old_members)

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
        self._user_data_btn.setText("Deine Daten")
        self._user_data_btn.clicked.connect(self._open_user_data)

        self._export_pdf_btn: QPushButton = QPushButton()
        self._export_pdf_btn.setText("Schreiben exportieren")
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
        grid.addWidget(self._old_members_btn, row, 1)
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
        result = w.window_manger.is_valid_member_window()
        if isinstance(result, str):
            self.set_info_bar(message=result)
        else:
            w.window_manger.members_window = m_w.MembersWindow()

    def _open_old_members(self) -> None:
        debug.info(item=debug_str, keyword="_open_old_members", message=f"old member clicked")

    def _open_my_jobs(self) -> None:
        debug.info(item=debug_str, keyword="_open_my_jobs", message=f"my jobs open")

    def _open_jobs(self) -> None:
        debug.info(item=debug_str, keyword="_open_jobs", message=f"open jobs")

    def _open_performances(self) -> None:
        debug.info(item=debug_str, keyword="_open_performances", message=f"performances open")

    def _open_edit_types(self) -> None:
        result = w.window_manger.is_valid_types_window()
        if isinstance(result, str):
            self.set_info_bar(message=result)
        else:
            w.window_manger.types_window = t_w.TypesWindow()

    def _open_user_data(self):
        debug.info(item=debug_str, keyword="_open_user_data", message=f"user data open")

    def _open_export_pdf(self):
        debug.info(item=debug_str, keyword="_open_export_pdf", message=f"pdf open")

    def _open_chance_user(self):
        debug.info(item=debug_str, keyword="_open_chance_user", message=f"chance user")

    def _open_chance_organization(self):
        debug.info(item=debug_str, keyword="_open_chance_organization", message=f"chance database")
