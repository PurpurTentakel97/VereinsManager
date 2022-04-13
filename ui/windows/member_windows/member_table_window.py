# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Table Window

import os
from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, \
    QPushButton, QFileDialog

import transition
from config import config_sheet as c
from ui.windows import window_manager as w
from ui.windows.base_window import BaseWindow
from ui.windows.member_windows import members_window

debug_str: str = "MemberTableWindow"


class MemberTableWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._data: dict = dict()
        self._widgets: list = list()
        self._type_id_name: list = list()

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._get_member_data()
        self._get_type_names()
        self._create_tabs()
        self._set_tables()

    def _create_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)
        self._tabs_widget: QTabWidget = QTabWidget()

    def _create_layout(self) -> None:
        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self._export_btn)

        vbox: QVBoxLayout = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self._tabs_widget)

        widget: QWidget = QWidget()
        widget.setLayout(vbox)
        self.set_widget(widget=widget)

        self.showMaximized()

    def _create_tabs(self) -> None:
        for ID, name in self._type_id_name:
            widget: QWidget = QWidget()
            self._widgets.append(widget)
            self._tabs_widget.addTab(widget, name)

    def _get_member_data(self) -> None:
        result, valid = transition.get_member_data_for_table()
        if not valid:
            self.set_error_bar(message=result)
        else:
            self._data = result

    def _get_type_names(self) -> None:
        for ID, _ in self._data.items():
            result, valid = transition.get_type_name_by_ID(ID=ID)
            if not valid:
                self.set_error_bar(message=result)
            else:
                self._type_id_name.append([ID, result[0]])

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitglieder Tabelle - Vereinsmanager")

    def _set_tables(self) -> None:
        # table
        for table_id, (_, data) in enumerate(self._data.items()):
            new_table: QTableWidget = QTableWidget()
            hbox = QHBoxLayout()
            hbox.addWidget(new_table)
            if data:
                # headline
                new_table.setRowCount(len(data))
                first_member = data[0]
                columns: int = len(first_member["member"]) - 2 + len(first_member["phone"]) + len(
                    first_member["mail"])
                new_table.setColumnCount(columns)
                headers: list = [
                    "Vorname",
                    "Nachname",
                    "Straße",
                    "PLZ",
                    "Stadt",
                    "Land",
                    "Geburstag",
                    "Alter",
                    "Eintritt",
                    "Jahre",
                    "Ehrenmitglied",
                ]
                headers.extend([x[0] for x in first_member["phone"]])
                headers.extend([x[0] for x in first_member["mail"]])
                new_table.setHorizontalHeaderLabels(headers)

                # member
                for row_index, row in enumerate(data):
                    column_index: int = 0
                    member_data: dict = row["member"]
                    phone_data: list = row["phone"]
                    mail_data: list = row["mail"]
                    keys: list = [
                        "first_name",
                        "last_name",
                        "street",
                        "zip_code",
                        "city",
                        "country",
                        "b_date",
                        "age",
                        "entry_date",
                        "membership_years",
                        "special_member",
                    ]
                    for key in keys:
                        entry = member_data[key]
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_index, column_index, new_item)
                        column_index += 1
                    for _, entry in phone_data:
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_index, column_index, new_item)
                        column_index += 1
                    for _, entry in mail_data:
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_index, column_index, new_item)
                        column_index += 1
            else:
                new_table.setRowCount(1)
                new_table.setColumnCount(1)
                new_item: QTableWidgetItem = QTableWidgetItem("Keine Mitglieder vorhanden")
                new_table.setItem(0, 0, new_item)
            new_table.setEditTriggers(QTableWidget.NoEditTriggers)
            widget = self._widgets[table_id]
            widget.setLayout(hbox)

    def _export(self) -> None:
        transition.create_default_dir("member_list")
        file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                                  os.path.join(os.getcwd(), c.config.dirs['save'],
                                                               c.config.dirs['organisation'],
                                                               c.config.dirs['export'], c.config.dirs['member'],
                                                               c.config.dirs['member_list'], "Mitglieder.pdf"),
                                                  "PDF (*.pdf);;All Files (*)")
        if not check:
            self.set_info_bar(message="Export abgebrochen")
            return

        message, result = transition.get_member_table_pdf(file)

        if not result:
            self.set_error_bar(message=message)
            return

        if self.is_open_permission():
            transition.open_latest_export()

        self.set_info_bar(message="Export abgeschlossen")

    def closeEvent(self, event) -> None:
        event.ignore()
        result, valid = w.window_manger.is_valid_member_window(ignore_member_table_window=True)
        if not valid:
            w.window_manger.member_table_window = None
            event.accept()
            return

        w.window_manger.members_window = members_window.MembersWindow()
        w.window_manger.member_table_window = None
        event.accept()
