# Purpur Tentakel
# 26.04.2022
# VereinsManager / Member Export Frame

from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTableWidgetItem, \
    QTableWidget, QTableView

import transition
from ui import export_manager
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListFrame, ListItem

debug_str: str = "MemberExportFrame"


class MemberExportFrame(QFrame):
    def __init__(self, window: BaseWindow):
        super().__init__()
        self.window: BaseWindow = window
        self.entries: list = list()

        self._create_ui()
        self._create_layout()
        self._set_enable_complete_UI()
        self._set_enable_export_letter_btn()
        self.set_current_member()

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
        self._export_other_anniversary_le.textChanged.connect(self._set_enable_other_anniversary_btn)
        self._export_other_anniversary_le.returnPressed.connect(self._export_other_anniversary)

        self._member_log_table: QTableWidget = QTableWidget()
        self._member_log_table.setSelectionBehavior(QTableView.SelectRows)
        self._member_log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._member_log_table.itemClicked.connect(self._set_enable_export_letter_btn)

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

    def _get_log_data(self, ID: int) -> list | None:
        data, valid = transition.get_log_member_data(target_id=ID)
        if not valid:
            self.window.set_error_bar(message=data)
            return

        new_data: list = list()
        target_columns: list = [
            "active",
            "membership_type"
        ]

        for entry in data:
            if entry['target_column'] in target_columns:
                new_data.append(entry)

        return new_data

    def _get_current_log_item(self) -> dict | None:
        current_item: QTableWidgetItem = self._member_log_table.currentItem()
        if current_item is None:
            return
        return self.entries[current_item.row()]

    def set_current_member(self) -> None:
        current_member: ListItem = self.member_list.list.currentItem()
        if not current_member:
            return

        data = self._get_log_data(ID=current_member.ID)
        if not data:
            return

        self._set_log_table(data=data)

    def _set_enable_other_anniversary_btn(self) -> None:
        self._export_other_anniversary_btn.setEnabled(self._is_export_other_anniversary())

    def _set_enable_complete_UI(self) -> None:
        is_member: bool = self._is_member()
        elements: tuple = (
            self._export_member_table_btn,
            self._export_member_card_btn,
            self._export_member_log_btn,
            self._export_current_anniversary_btn,
            self._export_other_anniversary_btn,
            self._export_other_anniversary_le,
            self._member_log_table,
            self._export_member_letter_btn,
        )

        for element in elements:
            element.setEnabled(is_member)

    def _set_enable_export_letter_btn(self) -> None:
        self._export_member_letter_btn.setEnabled(self._is_export_letter())

    def _set_log_table(self, data: list) -> None:
        self._member_log_table.clear()
        self._member_log_table.setColumnCount(4)
        self._member_log_table.setRowCount(len(data))

        headers: tuple = (
            "Datum",
            "Art",
            "Alte Daten",
            "Neue Daten",
        )
        self._member_log_table.setHorizontalHeaderLabels(headers)

        keys: tuple = (
            "log_date",
            "display_name",
            "old_data",
            "new_data",
        )

        for row_index, single_data in enumerate(data):
            self.entries.append(single_data)
            for column_index, key in enumerate(keys):
                entry = single_data[key]
                new_item: QTableWidgetItem = QTableWidgetItem(entry)
                self._member_log_table.setItem(row_index, column_index, new_item)

    def _is_export_other_anniversary(self) -> bool:
        number = self._export_other_anniversary_le.text().strip()

        if len(number) < 1:
            return False

        elif number in ("+", "-"):
            return False

        elif len(number) > 4:
            return False

        return True

    def _is_member(self) -> bool:
        first_member: ListItem = self.member_list.list.item(0)
        return first_member is not None

    def _is_export_letter(self) -> bool:
        current_item = self._get_current_log_item()
        if not current_item:
            return False
        return True

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
        current_member: ListItem = self.member_list.list.currentItem()

        name: str = current_member.set_name('get')
        name = name.replace(" ", "_")

        message, valid = export_manager.export_member_letter(name=name, ID=current_member.ID,
                                                             active=True,log_id=self._get_current_log_item()['ID'])

        if not valid:
            self.window.set_error_bar(message=message)
            return

        self.window.set_info_bar(message=message)
