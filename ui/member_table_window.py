# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Table Window

from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, \
    QPushButton, QFileDialog

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w
from config import config_sheet as c
import transition

import debug

debug_str: str = "MemberTableWindow"


class MemberTableWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._data: dict = dict()
        self._widgets: list = list()
        self._type_id_name: list = list()

        self._set_window_information()
        self._set_ui()
        self._set_layout()
        self._get_member_data()
        self._get_type_names()
        self._set_tabs()
        self._set_tables()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitglieder Tabelle - Vereinsmanager")

    def _set_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)
        self._tabs_widget: QTabWidget = QTabWidget()

    def _set_layout(self) -> None:
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

    def _set_tabs(self) -> None:
        for ID, name in self._type_id_name:
            widget: QWidget = QWidget()
            self._widgets.append(widget)
            self._tabs_widget.addTab(widget, name)

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
                columns: int = len(first_member["member"]) + len(first_member["phone"]) + len(
                    first_member["mail"])
                new_table.setColumnCount(columns)
                headers: list = [
                    "Vorname",
                    "Nachname",
                    "Straße",
                    "PLZ",
                    "Stadt",
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
                for row_id, row in enumerate(data):
                    column_id: int = 0
                    member_data = row["member"]
                    phone_data = row["phone"]
                    mail_data = row["mail"]
                    for entry in member_data:
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_id, column_id, new_item)
                        column_id += 1
                    for _, entry in phone_data:
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_id, column_id, new_item)
                        column_id += 1
                    for _, entry in mail_data:
                        new_item = QTableWidgetItem(entry if entry else "")
                        new_table.setItem(row_id, column_id, new_item)
                        column_id += 1
            else:
                new_table.setRowCount(1)
                new_table.setColumnCount(1)
                new_item: QTableWidgetItem = QTableWidgetItem("Keine Mitglieder vorhanden")
                new_table.setItem(0, 0, new_item)
            new_table.setEditTriggers(QTableWidget.NoEditTriggers)
            widget = self._widgets[table_id]
            widget.setLayout(hbox)

    def _get_member_data(self) -> None:
        result = transition.get_member_data_for_table()
        if isinstance(result, str):
            self.set_error_bar(message=result)
        else:
            self._data = result

    def _get_type_names(self) -> None:
        for ID, _ in self._data.items():
            result = transition.get_type_name_by_ID(ID=ID)
            if isinstance(result, str):
                self.set_error_bar(message=result)
            else:
                self._type_id_name.append([ID, result[0]])

    def _export(self) -> None:
        transition.create_default_dir("export")
        file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                                  f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/Mitglieder.pdf",
                                                  "PDF (*.pdf);;All Files (*)")
        if check:
            result = transition.get_member_pdf(file)
            if isinstance(result, str):
                self.set_error_bar(message=result)
            else:
                self.set_info_bar(message="Export abgeschlossen")
        else:
            self.set_info_bar(message="Export abgebrochen")

    def closeEvent(self, event) -> None:
        event.ignore()
        result = w.window_manger.is_valid_member_window(active_member_table_window=True)
        if isinstance(result, str):
            w.window_manger.member_table_window = None
            event.accept()
        elif result:
            w.window_manger.members_window = m_w.MembersWindow()
            w.window_manger.member_table_window = None
            event.accept()
