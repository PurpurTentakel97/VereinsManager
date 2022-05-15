# Purpur Tentakel
# 06.05.2022L
# VereinsManager / Schedule Window

from datetime import datetime
import locale

from PyQt5.QtCore import Qt, QDateTime, QTime
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QDateEdit, \
    QComboBox, QLineEdit, QTextEdit, QTimeEdit

import debug
import transition
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListItem, ListFrame
from ui import window_manager as w_m
from config import config_sheet as c
from helpers import helper

debug_str: str = "ScheduleWindow"

locale.setlocale(locale.LC_ALL, '')


class ScheduleWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._is_edit_mode: bool = bool()
        self._locations_ids: list = list()

        self._create_ui()
        self._create_layout()
        self._set_window_information()
        self._load_locations()
        self._load_single_day()

        self._set_edit_mode(set_edit=False)

    def _create_ui(self) -> None:
        self._open_list_btn: QPushButton = QPushButton("Zeitplan öffnen")
        self._day_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_schedule_days_dates,
                                              list_method=self._load_single_day, active=True)
        self._add_day_btn: QPushButton = QPushButton("Tag hinzufügen")
        self._add_day_btn.clicked.connect(self._add_day)
        self._remove_day_btn: QPushButton = QPushButton("Tag löschen")
        self._recover_day_btn: QPushButton = QPushButton("Tag wieder herstellen")

        self._save_btn: QPushButton = QPushButton("Speichern")
        self._save_btn.clicked.connect(self._save)
        self._break_btn: QPushButton = QPushButton("Zurücksetzten")
        self._break_btn.clicked.connect(lambda x: self._set_edit_mode(set_edit=False))

        self._date: QDateEdit = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.dateChanged.connect(lambda x: self._set_date_edit())
        self._meeting_time: QTimeEdit = QTimeEdit()
        self._meeting_time.setCalendarPopup(True)
        self._meeting_time.timeChanged.connect(lambda x: self._set_edit_mode())
        self._meeting_location_box: QComboBox = QComboBox()
        self._meeting_location_box.currentTextChanged.connect(lambda x: self._set_edit_mode())
        self._uniform_le: QLineEdit = QLineEdit()
        self._uniform_le.textChanged.connect(lambda x: self._set_edit_mode())
        self._day_comment_text: QTextEdit = QTextEdit()
        self._day_comment_text.textChanged.connect(self._set_comment_edit)

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

        buttons_hbox: QHBoxLayout = QHBoxLayout()
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
        global_vbox.addLayout(bottom_hbox)
        global_vbox.addLayout(footer_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.show()

    def _add_day(self) -> None:
        new_day: ListItem = ListItem(ID=None)
        self._day_list.list.addItem(new_day)
        self._day_list.list_items.append(new_day)

        self._day_list.list.setCurrentItem(new_day)
        self._set_day_None()
        self._set_day_name_in_day_list()

        self._set_edit_mode()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Zeitplan")

    def _set_edit_mode(self, set_edit: bool = True) -> None:
        edit: bool = set_edit
        invert_edit: bool = not edit

        self._save_btn.setEnabled(edit)
        self._break_btn.setEnabled(edit)

        self._day_list.list.setEnabled(invert_edit)
        self._add_day_btn.setEnabled(invert_edit)
        self._remove_day_btn.setEnabled(invert_edit)
        self._recover_day_btn.setEnabled(invert_edit)
        self.entry_list.list.setEnabled(invert_edit)
        self._add_entry_btn.setEnabled(invert_edit)
        self._remove_entry_btn.setEnabled(invert_edit)
        self._open_list_btn.setEnabled(invert_edit)

    def _set_day_None(self) -> None:
        self._date.setDate(QDateTime().fromSecsSinceEpoch(c.config.date_format["None_date"]).date())
        self._meeting_time.setTime(QTime(0, 0, 0))
        self._uniform_le.setText("")
        self._day_comment_text.setText("")

    def _set_day_name_in_day_list(self) -> None:
        current_day: ListItem = self._day_list.list.currentItem()
        current_date: datetime = self._date.dateTime().toPyDateTime()
        current_timestamp: int = QDateTime.toSecsSinceEpoch(QDateTime(self._date.date()))

        current_day.first_name = None
        if current_timestamp != c.config.date_format['None_date']:
            day: str = datetime.strftime(current_date, '%A')
            first_name: str = f"{day}, {datetime.strftime(current_date, c.config.date_format['short'])}"
            current_day.first_name = first_name

        current_day.set_name()

    def _set_comment_edit(self) -> None:
        self._set_edit_mode()

    def _set_date_edit(self) -> None:
        self._set_day_name_in_day_list()
        self._set_edit_mode()

    def _load_locations(self) -> None:
        locations, valid = transition.get_all_location_name()
        if not valid:
            self.set_error_bar(message=locations)
            return

        for ID, name, _ in locations:
            self._locations_ids.append([ID, name])
            self._meeting_location_box.addItem(name)
            self._entry_location_box.addItem(name)

    def _load_single_day(self):
        current_day: ListItem = self._day_list.list.currentItem()
        if current_day is None:
            self.set_error_bar(message="Kein Tag vorhanden")
            return

        data, valid = transition.get_schedule_name_by_ID(ID=current_day.ID, active=True)
        if not valid:
            self.set_error_bar(message=data)
            return

        date = QDateTime.fromSecsSinceEpoch(data['date']).date()
        self._date.setDate(date)
        self._meeting_time.setTime(QTime(data['hour'], data['minute']))
        self._uniform_le.setText(data['uniform'] if data['uniform'] else "")
        self._day_comment_text.setText(data['comment'] if data['comment'] else "")

        for ID, name in self._locations_ids:
            if ID == data['location']:
                self._meeting_location_box.setCurrentText(name)
                break

        self._set_edit_mode(set_edit=False)

    def _entry_list_method(self):
        pass  # TODO

    def _save(self) -> None:
        message, valid = self._save_day()
        if not valid:
            self.set_error_bar(message=message)
            return

        message, valid = self._save_entry()
        if not valid:
            self.set_error_bar(message=message)
            return

        self._set_edit_mode(set_edit=False)

        self.set_info_bar(message="saved")

    def _save_day(self) -> tuple[str, bool]:
        current_day: ListItem = self._day_list.list.currentItem()
        if current_day is None:
            return "Kein Tag vorhanden", False

        location = self._meeting_location_box.currentText()
        for ID, name in self._locations_ids:
            if name == location:
                location = ID
                break

        data: dict = {
            "ID": current_day.ID,
            "date": QDateTime.toSecsSinceEpoch(QDateTime(self._date.date())),
            "hour": self._meeting_time.time().hour(),
            "minute": self._meeting_time.time().minute(),
            "location": location,
            "uniform": self._uniform_le.text().strip().title() if self._uniform_le.text().strip() != "" else None,
            "comment": self._day_comment_text.toPlainText().strip() \
                if self._day_comment_text.toPlainText().strip() != "" else None,
        }

        ID, valid = transition.save_schedule_day(data=data)
        if not valid:
            return ID, False

        if isinstance(ID, int):
            current_day.ID = ID

        return "", True

    def _save_entry(self) -> tuple[str, bool]:
        return "", True

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.schedule_window = None
        event.accept()  # TODO
