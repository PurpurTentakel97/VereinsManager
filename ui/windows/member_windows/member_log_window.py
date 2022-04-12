# Purpur Tentakel
# 11.04.2022
# VereinsManager / Member Log Window

from PyQt5.QtWidgets import QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem

from ui.windows.base_window import BaseWindow
from ui.frames.list_frame import ListItem, ListFrame
from ui.windows import window_manager as w_m
from ui.windows.member_windows import members_window as m_w
import transition
import debug

debug_str: str = "MemberLogWindow"


class MemberLogWindow(BaseWindow):
    def __init__(self, row_index: int):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._set_first_member(row_index=row_index)

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitgliedslog")

    def _create_ui(self) -> None:
        self._delete: QPushButton = QPushButton("löschen")
        self._export: QPushButton = QPushButton("exportieren")

        self._members_list: ListFrame = ListFrame(window=self, type_="member", active=True)
        self._log_table: QTableWidget = QTableWidget()

    def _create_layout(self) -> None:
        buttons: QHBoxLayout = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._delete)
        buttons.addWidget(self._export)

        table_list: QHBoxLayout = QHBoxLayout()
        table_list.addWidget(self._members_list)
        table_list.addWidget(self._log_table)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(buttons)
        global_vbox.addLayout(table_list)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.resize(900, 600)
        self.show()

    def _set_first_member(self, row_index: int) -> None:
        self._members_list.list.setCurrentRow(row_index)
        self.load_single_member()

    def _set_table(self, data: tuple) -> None:
        self._log_table.clear()
        self._log_table.setColumnCount(4)
        self._log_table.setRowCount(len(data))

        headers: tuple = (
            "Datum",
            "Art",
            "Alte Daten",
            "Neue Daten",
        )
        self._log_table.setHorizontalHeaderLabels(headers)

        for row_index, single_data in enumerate(data):
            for column_index, entry in enumerate(single_data):
                new_item: QTableWidgetItem = QTableWidgetItem(entry)
                self._log_table.setItem(row_index, column_index, new_item)

    def load_single_member(self) -> None:
        current_member: ListItem = self._members_list.list.currentItem()
        data, valid = transition.get_log_member_data(target_id=current_member.ID)
        if not valid:
            self.set_error_bar(message=data)
            return
        self._set_table(data=data)

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.member_log_window = None
        message, valid = w_m.window_manger.is_valid_member_window(ignore_member_log_window=True)
        if valid:
            w_m.window_manger.members_window = m_w.MembersWindow()
        event.accept()
