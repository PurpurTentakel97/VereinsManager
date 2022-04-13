# Purpur Tentakel
# 11.04.2022
# VereinsManager / Member Log Window

from PyQt5.QtWidgets import QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem, QTableView

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
        self.entries: list = list()

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._set_first_member(row_index=row_index)
        self._set_export_entry_btn()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitgliedslog")

    def _create_ui(self) -> None:
        self._export_entry_btn: QPushButton = QPushButton("Eintrag exportieren")
        self._export_btn: QPushButton = QPushButton("Tabelle exportieren")

        self._members_list: ListFrame = ListFrame(window=self, type_="member", active=True)
        self._log_table: QTableWidget = QTableWidget()
        self._log_table.setSelectionBehavior(QTableView.SelectRows)
        self._log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._log_table.itemClicked.connect(self._set_export_entry_btn)

    def _create_layout(self) -> None:
        buttons: QHBoxLayout = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._export_entry_btn)
        buttons.addWidget(self._export_btn)

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
                self._log_table.setItem(row_index, column_index, new_item)

    def _set_export_entry_btn(self) -> None:
        self._export_entry_btn.setEnabled(self._is_export_entry())

    def _is_export_entry(self) -> bool:
        current_row = self._log_table.currentItem()
        if current_row is None:
            return False
        current_entry: dict = self.entries[current_row.row()]
        match current_entry['target_table']:
            case "member":
                match current_entry['target_column']:
                    case "active":
                        return True
                    case "membership_type":
                        return True

        return False

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
