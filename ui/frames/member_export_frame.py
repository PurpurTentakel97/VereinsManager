# Purpur Tentakel
# 26.04.2022
# VereinsManager / Member Export Frame

from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTableWidgetItem, \
    QTableWidget

import transition
from ui import export_manager
from ui.windows.base_window import BaseWindow
from ui.frames.list_frame import ListFrame, ListItem
import debug

debug_str: str = "MemberExportFrame"


class MemberExportFrame(QFrame):
    def __init__(self, window: BaseWindow):
        super().__init__()
        self.window: BaseWindow = window

        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        self.member_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_member_name,
                                                list_method=self.set_current_member, active=True)

        self._export_member_table_btn: QPushButton = QPushButton("Mitlieder Tabelle")
        self._export_member_table_btn.clicked.connect(self._export_table)

        self._export_member_card_btn: QPushButton = QPushButton("Mitglieder Karte")
        self._export_member_card_btn.clicked.connect(self._export_card)

        self._export_member_log_btn: QPushButton = QPushButton("Mitglieds Log")
        self._export_member_log_btn.clicked.connect(self._export_log)

        self._export_current_anniversary_btn: QPushButton = QPushButton("Aktuelle Jubiläen")
        self._export_current_anniversary_btn.clicked.connect(self._export_current_anniversary)

        self._export_other_anniversary_btn: QPushButton = QPushButton("Jubiläen im Jahr")
        self._export_other_anniversary_btn.clicked.connect(self._export_other_anniversary)

        self._export_other_anniversary_le: QLineEdit = QLineEdit()
        self._export_other_anniversary_le.setValidator(QIntValidator())
        self._export_other_anniversary_le.setPlaceholderText("zu exportierendes Jahr")
        self._export_other_anniversary_le.setText(str(datetime.now().year))

        self._member_log_table: QTableWidget = QTableWidget()
        self._export_member_letter_btn: QPushButton = QPushButton("Schreiben exportieren")
        self._export_member_letter_btn.clicked.connect(self._export_letter)

    def _create_layout(self) -> None:
        grid: QGridLayout = QGridLayout()
        row: int = 0
        grid.addWidget(self._export_member_table_btn, row, 0, 1, 1)
        grid.addWidget(self._export_member_card_btn, row, 1, 1, 1)
        grid.addWidget(self._export_member_log_btn, row, 2, 1, 1)
        row += 1
        grid.addWidget(self._export_current_anniversary_btn, row, 0, 1, 1)
        grid.addWidget(self._export_other_anniversary_btn, row, 1, 1, 1)
        grid.addWidget(self._export_other_anniversary_le, row, 2, 1, -1)
        row += 1
        grid.addWidget(self._member_log_table, row, 0, 10, -1)
        row += 10
        grid.addWidget(self._export_member_letter_btn, row, 3, 1, -1)

        global_hox: QHBoxLayout = QHBoxLayout()
        global_hox.addWidget(self.member_list)
        global_hox.addLayout(grid)

        self.setLayout(global_hox)

    def set_current_member(self) -> None:
        debug.debug(item=debug_str, keyword="set_current_member", message=f"None Method")

    def _export_table(self) -> None:
        message, valid = export_manager.export_member_table()

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)

    def _export_card(self) -> None:
        current_member: ListItem = self.member_list.list.currentItem()
        message, valid = export_manager.export_member_card(first_name=current_member.first_name,
                                                           last_name=current_member.last_name, ID=current_member.ID)

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)

    def _export_log(self) -> None:
        current_member: ListItem = self.member_list.list.currentItem()
        name: str = current_member.set_name('get')

        message, valid = export_manager.export_member_log(name=name, ID=current_member.ID, active=True)

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)

    def _export_current_anniversary(self) -> None:
        message, valid = export_manager.export_member_anniversary(index=0, year=0)

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)

    def _export_other_anniversary(self) -> None:
        year = self._export_other_anniversary_le.text().strip()
        if year in ("", "-", "+"):
            self.window.set_error_bar(message="Keine Zahl eingegeben")
            return

        message, valid = export_manager.export_member_anniversary(index=1,
                                                                  year=int(year))

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)

    def _export_letter(self) -> None:
        debug.debug(item=debug_str, keyword="_export_letter", message=f"TODO")
