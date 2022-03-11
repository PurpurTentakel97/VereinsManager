# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

import datetime
from enum import Enum
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QLabel

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w
import transition
import debug

debug_str: str = "Member Anniversary Window"


class DataType(Enum):
    CURRENT = 1
    OTHER = 2


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()
        self._current_b_day_data: list = list()
        self._current_entry_day_data: list = list()
        self._other_b_day_data: list = list()
        self._other_entry_day_data: list = list()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

        self._other_year_le.setText(str(datetime.datetime.now().year))
        self._get_current_data()
        self._get_other_data()
        self._set_table(DataType.CURRENT)
        self._set_table(DataType.OTHER)

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _set_ui(self) -> None:
        b_day_lb: str = "Geburtstage:"
        self._current_b_day_lb: QLabel = QLabel()
        self._current_b_day_lb.setText(b_day_lb)
        self._other_b_day_lb: QLabel = QLabel()
        self._other_b_day_lb.setText(b_day_lb)

        entry_day_lb: str = "Mitgliedsjahre:"
        self._current_entry_lb: QLabel = QLabel()
        self._current_entry_lb.setText(entry_day_lb)
        self._other_entry_lb: QLabel = QLabel()
        self._other_entry_lb.setText(entry_day_lb)

        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)

        self._tabs: QTabWidget = QTabWidget()

        self._current_widget: QWidget = QWidget()
        self._tabs.addTab(self._current_widget, "Aktuell")
        self._current_b_day_table: QTableWidget = QTableWidget()
        self._current_b_day_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._current_entry_day_table: QTableWidget = QTableWidget()
        self._current_entry_day_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self._other_widget: QWidget = QWidget()
        self._tabs.addTab(self._other_widget, "Andere")
        self._other_b_day_table: QTableWidget = QTableWidget()
        self._other_b_day_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._other_entry_day_table: QTableWidget = QTableWidget()
        self._other_entry_day_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self._other_year_le: QLineEdit = QLineEdit()
        self._other_year_le.returnPressed.connect(self._get_other_data)
        self._other_year_le.textChanged.connect(self._set_year_btn_enabled)
        self._other_year_le.setValidator(QIntValidator())
        self._other_year_le.setPlaceholderText("Jahr eingeben")
        self._set_year_btn: QPushButton = QPushButton()
        self._set_year_btn.setText("Jahr auswählen")
        self._set_year_btn.clicked.connect(self._get_other_data)

    def _set_layout(self) -> None:
        # Label
        current_b_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        current_b_day_lb_hbox.addWidget(self._current_b_day_lb)
        current_b_day_lb_hbox.addStretch()

        other_b_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        other_b_day_lb_hbox.addWidget(self._other_b_day_lb)
        other_b_day_lb_hbox.addStretch()

        current_entry_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        current_entry_day_lb_hbox.addWidget(self._current_entry_lb)
        current_entry_day_lb_hbox.addStretch()

        other_entry_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        other_entry_day_lb_hbox.addWidget(self._other_entry_lb)
        other_entry_day_lb_hbox.addStretch()

        # current widget
        b_day_vbox: QVBoxLayout = QVBoxLayout()
        b_day_vbox.addLayout(current_b_day_lb_hbox)
        b_day_vbox.addWidget(self._current_b_day_table)

        entry_day_vbox: QVBoxLayout = QVBoxLayout()
        entry_day_vbox.addLayout(current_entry_day_lb_hbox)
        entry_day_vbox.addWidget(self._current_entry_day_table)

        current_h_box: QHBoxLayout = QHBoxLayout()
        current_h_box.addLayout(b_day_vbox)
        current_h_box.addLayout(entry_day_vbox)
        self._current_widget.setLayout(current_h_box)

        # other widget
        year_hbox: QHBoxLayout = QHBoxLayout()
        year_hbox.addWidget(self._other_year_le)
        year_hbox.addWidget(self._set_year_btn)

        b_day_vbox: QVBoxLayout = QVBoxLayout()
        b_day_vbox.addLayout(other_b_day_lb_hbox)
        b_day_vbox.addWidget(self._other_b_day_table)

        entry_day_vbox: QVBoxLayout = QVBoxLayout()
        entry_day_vbox.addLayout(other_entry_day_lb_hbox)
        entry_day_vbox.addWidget(self._other_entry_day_table)

        other_h_box: QHBoxLayout = QHBoxLayout()
        other_h_box.addLayout(b_day_vbox)
        other_h_box.addLayout(entry_day_vbox)

        other_v_box: QVBoxLayout = QVBoxLayout()
        other_v_box.addLayout(year_hbox)
        other_v_box.addLayout(other_h_box)
        self._other_widget.setLayout(other_v_box)

        # global widget
        global_h_box: QHBoxLayout = QHBoxLayout()
        global_h_box.addStretch()
        global_h_box.addWidget(self._export_btn)

        global_v_box: QVBoxLayout = QVBoxLayout()
        global_v_box.addLayout(global_h_box)
        global_v_box.addWidget(self._tabs)

        widget: QWidget = QWidget()
        widget.setLayout(global_v_box)

        self.set_widget(widget)
        self.show()

    def _set_table(self, data_type: DataType) -> None:
        dummy_b_day_table: QTableWidget = QTableWidget()
        dummy_b_day_data: list = list()
        dummy_entry_day_table: QTableWidget = QTableWidget()
        dummy_entry_day_data: list = list()

        match data_type:
            case DataType.CURRENT:
                dummy_b_day_table = self._current_b_day_table
                dummy_b_day_data = self._current_b_day_data

                dummy_entry_day_table = self._current_entry_day_table
                dummy_entry_day_data = self._current_entry_day_data

                debug.info(item=debug_str, keyword="_set_table", message=f"current_b_day = {self._current_b_day_data}")
                debug.info(item=debug_str, keyword="_set_table",
                           message=f"current_entry_day = {self._current_entry_day_data}")

            case DataType.OTHER:
                dummy_b_day_table = self._other_b_day_table
                dummy_b_day_data = self._other_b_day_data

                dummy_entry_day_table = self._other_entry_day_table
                dummy_entry_day_data = self._other_entry_day_data

                debug.info(item=debug_str, keyword="_set_table", message=f"other_b_day = {self._other_b_day_data}")
                debug.info(item=debug_str, keyword="_set_table",
                           message=f"other_entry_day = {self._other_entry_day_data}")

        dummys: list = [
            [dummy_b_day_data, dummy_b_day_table, ["Name", "Datum", "Alter"]],
            [dummy_entry_day_data, dummy_entry_day_table, ["Name", "Datum", "Jubiläum"]],
        ]
        # dummy_b_day_table.setItem()

        for data, table, headers in dummys:
            table.clear()
            if not data:
                table.setRowCount(1)
                table.setColumnCount(1)
                item: QTableWidgetItem = QTableWidgetItem("Keine Einträge vorhanden")
                table.setItem(0, 0, item)
                table.update()
            else:
                table.setRowCount(len(data) + 1)
                table.setColumnCount(3)
                for entry in headers:
                    item: QTableWidgetItem = QTableWidgetItem(entry)
                    table.setItem(0, headers.index(entry), item)
                for index, entry in enumerate(data, start=1):
                    item: QTableWidgetItem = QTableWidgetItem(
                        self._transform_member_name(entry["firstname"], entry["lastname"]))
                    table.setItem(index, 0, item)
                    item: QTableWidgetItem = QTableWidgetItem(entry['date'])
                    table.setItem(index, 1, item)
                    item: QTableWidgetItem = QTableWidgetItem(str(entry['year']))
                    table.setItem(index, 2, item)

    def _set_year_btn_enabled(self) -> None:
        self._set_year_btn.setEnabled(self._is_year())

    def _get_current_data(self) -> None:
        data = transition.get_anniversary_member_data(type_="current")
        if isinstance(data, str):
            self.set_error_bar(message=data)

        self._current_b_day_data = data["b_day"]
        self._current_entry_day_data = data["entry_day"]

    def _get_other_data(self) -> None:
        debug.info(item=debug_str, keyword="_get_other_data", message=f"clicked")

    @staticmethod
    def _transform_member_name(firstname: str, lastname: str) -> str:
        if firstname and lastname:
            return f"{firstname} {lastname}"
        elif firstname:
            return f"{firstname} // Nachname"
        elif lastname:
            return f"Vorname // {lastname}"
        else:
            return "Vorname // Nachname"

    def _is_year(self) -> bool:
        return self._other_year_le.text().strip() != ""

    def _export(self) -> None:
        debug.info(item=debug_str, keyword="_export", message=f"export")

    def closeEvent(self, event) -> None:
        event.ignore()
        result = w.window_manger.is_valid_member_window(active_member_anniversary_window=True)
        if isinstance(result, str):
            w.window_manger.member_anniversary_window = None
            event.accept()
        elif result:
            w.window_manger.members_window = m_w.MembersWindow()
            w.window_manger.member_anniversary_window = None
            event.accept()
