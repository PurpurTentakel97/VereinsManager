# Purpur Tentakel
# 06.05.2022L
# VereinsManager / Schedule Window

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QDateEdit, \
    QComboBox, QLineEdit, QTextEdit, QTimeEdit

import transition
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListItem, ListFrame
from ui import window_manager as w_m


class ScheduleWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._create_ui()
        self._create_layout()
        self._set_window_information()

    def _create_ui(self) -> None:
        self._open_list_btn: QPushButton = QPushButton("Zeitplan öffnen")
        self._day_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_schedule_days_names,
                                              list_method=self._day_list_method, active=True)
        self._add_day_btn: QPushButton = QPushButton("Tag hinzufügen")
        self._remove_day_btn: QPushButton = QPushButton("Tag löschen")
        self._recover_day_btn: QPushButton = QPushButton("Tag wieder herstellen")

        self._save_btn: QPushButton = QPushButton("Speichern")
        self._break_btn: QPushButton = QPushButton("Zurücksetzten")

        self._date: QDateEdit = QDateEdit()
        self._date.setCalendarPopup(True)
        self._meeting_time: QTimeEdit = QTimeEdit()
        self._meeting_time.setCalendarPopup(True)
        self._meeting_location_box: QComboBox = QComboBox()
        self._uniform_le: QLineEdit = QLineEdit()
        self._day_comment_text: QTextEdit = QTextEdit()

        self.entry_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_schedule_entry_names,
                                               list_method=self._entry_list_method, active=True)
        self._add_entry_btn: QPushButton = QPushButton("Eintrag hinzufügen")
        self._remove_entry_btn: QPushButton = QPushButton("Eintrag löschen")

        self._entry_title_le: QLineEdit = QLineEdit()
        self._entry_time: QTimeEdit = QTimeEdit()
        self._entry_time.setCalendarPopup(True)
        self._entry_type_box: QComboBox = QComboBox()  # TODO
        self._entry_location_box: QComboBox = QComboBox()
        self._entry_comment_text: QTextEdit = QTextEdit()

    def _create_layout(self) -> None:
        header_hbox: QHBoxLayout = QHBoxLayout()
        header_hbox.addWidget(QLabel("Tage:"))
        header_hbox.addStretch()
        header_hbox.addWidget(self._open_list_btn)

        row: int = 0
        left_top_grid: QGridLayout = QGridLayout()
        left_top_grid.addWidget(self._day_list, row, 0, 1, 4)

        buttons_hbox:QHBoxLayout = QHBoxLayout()
        buttons_hbox.addWidget(self._add_day_btn)
        buttons_hbox.addWidget(self._remove_day_btn)
        buttons_hbox.addWidget(self._recover_day_btn)
        buttons_hbox.addStretch()

        row: int = 0
        right_top_grid: QGridLayout = QGridLayout()
        right_top_grid.addWidget(QLabel("Datum"))
        right_top_grid.addWidget(self._date, row, 1, 1, -1)
        row += 1
        right_top_grid.addWidget(QLabel("Uhrzeit:"), row, 0, 1, 1)
        right_top_grid.addWidget(self._meeting_time, row, 1, 1, -1)
        row += 1
        right_top_grid.addWidget(QLabel("Ort:"), row, 0, 1, 1)
        right_top_grid.addWidget(self._meeting_location_box, row, 1, 1, -1)
        row += 1
        right_top_grid.addWidget(QLabel("Uniform:"), row, 0, 1, 1)
        right_top_grid.addWidget(self._uniform_le, row, 1, 1, -1)
        row += 1
        right_top_grid.addWidget(QLabel("Kommentar:"), row, 0, 1, 1, alignment=Qt.AlignTop)
        right_top_grid.addWidget(self._day_comment_text, row, 1, 1, 3)

        top_hbox: QHBoxLayout = QHBoxLayout()
        top_hbox.addLayout(left_top_grid)
        top_hbox.addLayout(right_top_grid)

        left_bottom_grid: QGridLayout = QGridLayout()
        left_bottom_grid.addWidget(QLabel("Einträge:"), 0, 0, 1, -1)
        left_bottom_grid.addWidget(self.entry_list, 1, 0, 1, 4)

        row: int = 0
        right_bottom_grid: QGridLayout = QGridLayout()
        right_bottom_grid.addWidget(QLabel("Titel:"), row, 0, 1, 1)
        right_bottom_grid.addWidget(self._entry_title_le, row, 1, 1, -1)
        row += 1
        right_bottom_grid.addWidget(QLabel("Uhrzeit:"), row, 0, 1, 1)
        right_bottom_grid.addWidget(self._entry_time, row, 1, 1, -1)
        row += 1
        right_bottom_grid.addWidget(QLabel("Eintragsart:"), row, 0, 1, 1)
        right_bottom_grid.addWidget(self._entry_type_box, row, 1, 1, -1)
        row += 1
        right_bottom_grid.addWidget(QLabel("Ort:"), row, 0, 1, 1)
        right_bottom_grid.addWidget(self._entry_location_box, row, 1, 1, -1)
        row += 1
        right_bottom_grid.addWidget(QLabel("Kommentar:"), row, 0, 1, 1, alignment=Qt.AlignTop)
        right_bottom_grid.addWidget(self._entry_comment_text, row, 1, 1, 3)

        bottom_hbox: QHBoxLayout = QHBoxLayout()
        bottom_hbox.addLayout(left_bottom_grid)
        bottom_hbox.addLayout(right_bottom_grid)

        footer_hbox: QHBoxLayout = QHBoxLayout()
        footer_hbox.addWidget(self._add_entry_btn)
        footer_hbox.addWidget(self._remove_entry_btn)
        footer_hbox.addStretch()
        footer_hbox.addWidget(self._break_btn)
        footer_hbox.addWidget(self._save_btn)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(header_hbox)
        global_vbox.addLayout(top_hbox)
        global_vbox.addLayout(buttons_hbox)
        global_vbox.addWidget(QLabel(""))
        global_vbox.addLayout(bottom_hbox)
        global_vbox.addLayout(footer_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.show()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Zeitplan")

    def _day_list_method(self):
        pass  # TODO

    def _entry_list_method(self):
        pass  # TODO

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.schedule_window = None
        event.accept()  # TODO
