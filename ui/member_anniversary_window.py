# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

import datetime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w
import transition
import debug

debug_str: str = "Member Anniversary Window"


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()
        self._current_b_day_data: list = list()
        self._current_entry_data: list = list()
        self._other_b_day_data: list = list()
        self._other_entry_data: list = list()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

        self._other_year_le.setText(str(datetime.datetime.now().year))
        self._get_current_data()
        self._set_current_table()
        self._get_other_data()
        self._set_other_table()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _set_ui(self) -> None:
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
        h_box: QHBoxLayout = QHBoxLayout()
        h_box.addWidget(self._current_b_day_table)
        h_box.addWidget(self._current_entry_day_table)
        self._current_widget.setLayout(h_box)

        h_box_1: QHBoxLayout = QHBoxLayout()
        h_box_1.addWidget(self._other_year_le)
        h_box_1.addWidget(self._set_year_btn)

        h_box: QHBoxLayout = QHBoxLayout()
        h_box.addWidget(self._other_b_day_table)
        h_box.addWidget(self._other_entry_day_table)

        v_box: QVBoxLayout = QVBoxLayout()
        v_box.addLayout(h_box_1)
        v_box.addLayout(h_box)
        self._other_widget.setLayout(v_box)

        h_box: QHBoxLayout = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self._export_btn)

        v_box: QVBoxLayout = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self._tabs)

        widget: QWidget = QWidget()
        widget.setLayout(v_box)

        self.set_widget(widget)
        self.show()

    def _set_current_table(self) -> None:
        debug.info(item=debug_str, keyword="_set_current_layout", message=f"current_b_day = {self._current_b_day_data}")
        debug.info(item=debug_str, keyword="_set_current_layout",
                   message=f"current_entry_day = {self._current_entry_data}")
        self._current_b_day_table.clear()
        self._current_entry_day_table.clear()
        self._current_entry_data = list()
        self._current_b_day_data = list()

        if not self._current_b_day_data:
            self._current_b_day_table.setRowCount(1)
            self._current_b_day_table.setColumnCount(1)
            item: QTableWidgetItem = QTableWidgetItem("Keine Jubiläen vorhanden")
            self._current_b_day_table.setItem(0, 0, item)
            self._current_b_day_table.update()
        else:
            pass

        if not self._current_entry_data:
            self._current_entry_day_table.setRowCount(1)
            self._current_entry_day_table.setColumnCount(1)
            item: QTableWidgetItem = QTableWidgetItem("Keine Jubiläen vorhanden")
            self._current_entry_day_table.setItem(0, 0, item)
            self._current_entry_day_table.update()
        else:
            pass

    def _set_other_table(self) -> None:
        self._other_b_day_table.clear()
        self._other_entry_day_table.clear()

        if not self._other_b_day_data:
            self._other_b_day_table.setRowCount(1)
            self._other_b_day_table.setColumnCount(1)
            item: QTableWidgetItem = QTableWidgetItem("Keine Jubiläen vorhanden")
            self._other_b_day_table.setItem(0, 0, item)
            self._other_b_day_table.update()
        else:
            pass

        if not self._other_entry_data:
            self._other_entry_day_table.setRowCount(1)
            self._other_entry_day_table.setColumnCount(1)
            item: QTableWidgetItem = QTableWidgetItem("Keine Jubiläen vorhanden")
            self._other_entry_day_table.setItem(0, 0, item)
            self._other_entry_day_table.update()
        else:
            pass

    def _set_year_btn_enabled(self) -> None:
        self._set_year_btn.setEnabled(self._is_year())

    def _get_current_data(self) -> None:
        data = transition.get_anniversary_member_data(type_="current")
        if isinstance(data, str):
            self.set_error_bar(message=data)

        self._current_b_day_data = data["b_day"]
        self._current_entry_data = data["entry_day"]

    def _get_other_data(self) -> None:
        debug.info(item=debug_str, keyword="_get_other_data", message=f"clicked")

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
