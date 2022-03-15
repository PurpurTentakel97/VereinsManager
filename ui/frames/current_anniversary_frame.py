# Purpur Tentakel
# 21.01.2022
# VereinsManager / Current Anniversary Frame

from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout

import transition
import debug

debug_str: str = "CurrentAnniversaryFrame"


class CurrentAnniversaryFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self._current_b_day_data: list = list()
        self._current_entry_day_data: list = list()

        self._set_ui()
        self._set_layout()

        self._get_current_data()

    def _set_ui(self) -> None:
        # Label
        self._current_b_day_lb: QLabel = QLabel()
        self._current_b_day_lb.setText("Geburtstage:")

        self._current_entry_lb: QLabel = QLabel()
        self._current_entry_lb.setText("Mitgliedsjahre:")

        self._current_b_day_table: QTableWidget = QTableWidget()
        self._current_b_day_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._current_entry_day_table: QTableWidget = QTableWidget()
        self._current_entry_day_table.setEditTriggers(QTableWidget.NoEditTriggers)

    def _set_layout(self) -> None:
        # Label
        current_b_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        current_b_day_lb_hbox.addWidget(self._current_b_day_lb)
        current_b_day_lb_hbox.addStretch()

        current_entry_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        current_entry_day_lb_hbox.addWidget(self._current_entry_lb)
        current_entry_day_lb_hbox.addStretch()

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
        self.setLayout(current_h_box)

    def _set_table(self) -> None:
        dummies: list = [
            [self._current_b_day_data, self._current_b_day_table, ["Name", "Datum", "Alter"]],
            [self._current_entry_day_data, self._current_entry_day_table, ["Name", "Datum", "Jubiläum"]],
        ]

        for data, table, headers in dummies:
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

    def _get_current_data(self) -> None:
        data = transition.get_anniversary_member_data(type_="current")
        if isinstance(data, str):
            self.set_error_bar(message=data)
        else:
            self._current_b_day_data = data["b_day"]
            self._current_entry_day_data = data["entry_day"]
            self._set_table()

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
