# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

import datetime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QLabel, QFileDialog, QFrame

from ui.windows.base_window import BaseWindow
from ui.windows import members_window as m_w, window_manager as w
from config import config_sheet as c
from ui.frames.current_anniversary_frame import CurrentAnniversaryFrame
import transition

debug_str: str = "Member Anniversary Window"


class OtherAnniversaryFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()

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
            self.set_error_bar(message=" Keine Zahl eingegeben")
            return

        data = transition.get_anniversary_member_data(type_="other", year=year)
        if isinstance(data, str):
            self.set_error_bar(message=data)
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


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._current_frame: CurrentAnniversaryFrame = CurrentAnniversaryFrame()
        self._other_frame: OtherAnniversaryFrame = OtherAnniversaryFrame()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _set_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)

        self._tabs: QTabWidget = QTabWidget()
        self._tabs.addTab(self._current_frame, "Aktuell")
        self._tabs.addTab(self._other_frame, "Andere")

    def _set_layout(self) -> None:

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
        self.resize(700, 500)

    def _export(self) -> None:
        transition.create_default_dir("export")
        file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                                  f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/Geburtstage-Jubilaen.pdf",
                                                  "PDF (*.pdf);;All Files (*)")
        if check:
            result = 1
            match self._tabs.currentIndex():
                case 0:
                    result = transition.get_member_anniversary_pdf(path=file)
                case 1:
                    result = transition.get_member_anniversary_pdf(path=file, year=self._other_frame.other_year)

            if isinstance(result, str):
                self.set_error_bar(message=result)
            else:
                self.set_info_bar(message="Export abgeschlossen")
        else:
            self.set_info_bar(message="Export abgebrochen")

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
