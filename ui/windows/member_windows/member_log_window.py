# Purpur Tentakel
# 11.04.2022
# VereinsManager / Member Log Window

from PyQt5.QtWidgets import QTableWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem, QTableView, \
    QTabWidget, QLabel

import transition
from ui.windows.base_window import BaseWindow
from ui import window_manager as w_m, export_manager
from ui.frames.list_frame import ListItem, ListFrame
from ui.windows.member_windows import members_window

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

        self._export_letter_btn: QPushButton = QPushButton("Eintrag exportieren")
        self._export_letter_btn.clicked.connect(self._export_letter)
        self._export_log_btn: QPushButton = QPushButton("Tabelle exportieren")
        self._export_log_btn.clicked.connect(self._export_log)

        self._member_lb: QLabel = QLabel("Mitgliedsname")
        self._members_list_active: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_member_name,
                                                         list_method=self.load_single_member, active=True)
        self._members_list_inactive: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_member_name,
                                                           list_method=self.load_single_member, active=False)

        self._tabs: QTabWidget = QTabWidget()
        self._create_tabs()

        self._log_table: QTableWidget = QTableWidget()
        self._log_table.setSelectionBehavior(QTableView.SelectRows)
        self._log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._log_table.itemClicked.connect(self._set_export_entry_btn)

    def _create_layout(self) -> None:
        buttons: QHBoxLayout = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._export_letter_btn)
        buttons.addWidget(self._export_log_btn)

        table_vbox: QVBoxLayout = QVBoxLayout()
        table_vbox.addWidget(self._member_lb)
        table_vbox.addWidget(self._log_table)

        table_list_hbox: QHBoxLayout = QHBoxLayout()
        table_list_hbox.addWidget(self._tabs)
        table_list_hbox.addLayout(table_vbox)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(buttons)
        global_vbox.addLayout(table_list_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.resize(900, 600)
        self.show()

    def _create_tabs(self) -> None:
        tab_data: tuple = (
            ("Aktiv", self._members_list_active),
            ("Inaktiv", self._members_list_inactive),
        )

        for name, list_ in tab_data:
            layout: QHBoxLayout = QHBoxLayout()
            layout.addWidget(list_)

            widget: QWidget = QWidget()
            widget.setLayout(layout)

            self._tabs.addTab(widget, name)

    def _get_current_member(self) -> ListItem:
        current_tab: int = self._tabs.currentIndex()
        match current_tab:
            case 0:
                return self._members_list_active.list.currentItem()
            case 1:
                return self._members_list_inactive.list.currentItem()

    def _get_current_entry(self) -> dict | bool:
        current_cell = self._log_table.currentItem()
        if current_cell is None:
            return False
        return self.entries[current_cell.row()]

    def _get_letter_data(self) -> dict | bool:
        current_entry: dict = self._get_current_entry()
        if not current_entry:
            return False
        return current_entry

    def _set_first_member(self, row_index: int) -> None:
        self._members_list_active.list.setCurrentRow(row_index)
        self.load_single_member()

    def _set_table(self, data: tuple) -> None:
        self.entries.clear()
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

    def _set_member_name(self) -> None:
        current_member: ListItem = self._get_current_member()
        text = current_member.set_name(type_='get')

        if self._tabs.currentIndex() == 1:
            text += " (inaktiv) "

        text += ":"

        self._member_lb.setText(text)

    def _set_export_entry_btn(self) -> None:
        self._export_letter_btn.setEnabled(self._is_export_entry())

    def load_single_member(self) -> None:
        current_member: ListItem = self._get_current_member()
        if not current_member:
            self.set_error_bar(message="Keine Mitglieder vorhanden.")
            self._export_log_btn.setEnabled(False)
            return
        data, valid = transition.get_log_member_data(target_id=current_member.ID)
        if not valid:
            self.set_error_bar(message=data)
            return

        self._set_member_name()
        self._set_table(data=data)

    def _is_export_entry(self) -> bool:
        current_entry = self._get_current_entry()
        if not current_entry:
            return False

        match current_entry['target_table']:
            case "member":
                match current_entry['target_column']:
                    case "active":
                        return True
                    case "membership_type":
                        return True

        return False

    def _export_log(self) -> None:
        current_member: ListItem = self._get_current_member()
        name = current_member.set_name(type_='get')

        message, valid = export_manager.export_member_log(name=name, ID=current_member.ID,
                                                          active=self._tabs.currentIndex() == 0)

        if not valid:
            self.set_error_bar(message=message)
            return

        self.set_info_bar(message=message)

    def _export_letter(self) -> None:
        current_member: ListItem = self._get_current_member()

        name: str = current_member.set_name('get')
        name = name.replace(" ", "_")

        message, valid = export_manager.export_member_letter(name=name, ID=current_member.ID,
                                                             active=self._tabs.currentIndex() == 0,
                                                             log_id=self._get_letter_data()['ID'])

        if not valid:
            self.set_error_bar(message=message)
            return

        self.set_info_bar(message=message)

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.member_log_window = None
        message, valid = w_m.window_manger.is_valid_member_window(ignore_member_log_window=True)
        if valid:
            w_m.window_manger.members_window = members_window.MembersWindow()
        event.accept()
