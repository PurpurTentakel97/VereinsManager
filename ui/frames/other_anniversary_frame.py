# Purpur Tentakel
# 25.03.2022
# VereinsManager / Other Anniversary Frame

import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFrame, QLabel, QTableWidget,QLineEdit, QPushButton,QHBoxLayout, QVBoxLayout, QTableWidgetItem

import transition
import debug

debug_str:str= "OtherAnniversaryFrame"

class OtherAnniversaryFrame(QFrame):
    def __init__(self, window) -> None:
        super().__init__()

        self.window_ = window

        self.other_year: int = int()

        self._other_b_day_data: list = list()
        self._other_entry_day_data: list = list()

        self._set_ui()
        self._set_layout()

        self._other_year_le.setText(str(datetime.datetime.now().year))

        self._get_other_data()

    def _set_ui(self) -> None:
        self._other_b_day_lb: QLabel = QLabel()
        self._other_b_day_lb.setText("Geburtstage:")

        self._other_entry_lb: QLabel = QLabel()
        self._other_entry_lb.setText("Mitgliedsjahre:")

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
        other_b_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        other_b_day_lb_hbox.addWidget(self._other_b_day_lb)
        other_b_day_lb_hbox.addStretch()

        other_entry_day_lb_hbox: QHBoxLayout = QHBoxLayout()
        other_entry_day_lb_hbox.addWidget(self._other_entry_lb)
        other_entry_day_lb_hbox.addStretch()

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
        self.setLayout(other_v_box)

    def _get_other_data(self) -> None:
        try:
            year: int = int(self._other_year_le.text().strip())
        except ValueError:
            self.window_.set_error_bar(message=" Keine Zahl eingegeben")
            return

        data, valid = transition.get_anniversary_member_data(type_="other", year=year)
        if not valid:
            self.window_.set_error_bar(message=data)
        else:
            self.other_year = year
            self._other_b_day_data = data["b_day"]
            self._other_entry_day_data = data["entry_day"]
            self._set_table()

    def _set_table(self) -> None:

        dummies: list = [
            [self._other_b_day_data, self._other_b_day_table, ["Name", "Datum", "Alter"]],
            [self._other_entry_day_data, self._other_entry_day_table, ["Name", "Datum", "Jubiläum"]],
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
        self.window_.set_info_bar("Daten geladen.")

    def _set_year_btn_enabled(self) -> None:
        self._set_year_btn.setEnabled(self._is_year())

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
