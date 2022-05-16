# Purpur Tentakel
# 06.05.2022L
# VereinsManager / Schedule Window

from datetime import datetime
import locale

from PyQt5.QtCore import Qt, QDateTime, QTime
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QDateEdit, \
    QComboBox, QLineEdit, QTextEdit, QTimeEdit

import transition
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListItem, ListFrame
from ui import window_manager as w_m
from ui.windows import recover_window
from config import config_sheet as c
import debug

debug_str: str = "ScheduleWindow"

locale.setlocale(locale.LC_ALL, '')


class ScheduleWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._is_edit_mode: bool = bool()
        self._locations_ids: list = list()
        self._entry_type_ids: list = list()

        self._create_ui()
        self._create_layout()
        self._set_window_information()
        self._load_locations()
        self._load_entry_types()

        self._load_single_day()

    # global
    def _create_ui(self) -> None:
        self._open_list_btn: QPushButton = QPushButton("Zeitplan öffnen")

        # day
        self._day_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_schedule_days_dates,
                                              list_method=self._load_single_day, active=True)
        self._add_day_btn: QPushButton = QPushButton("Tag hinzufügen")
        self._add_day_btn.clicked.connect(self._add_day)
        self._remove_day_btn: QPushButton = QPushButton("Tag löschen")
        self._remove_day_btn.clicked.connect(self._save_day_activity)
        self._recover_day_btn: QPushButton = QPushButton("Tag wieder herstellen")
        self._recover_day_btn.clicked.connect(self._recover_day)

        self._save_btn: QPushButton = QPushButton("Speichern")
        self._save_btn.clicked.connect(self._save)
        self._break_btn: QPushButton = QPushButton("Zurücksetzten")
        self._break_btn.clicked.connect(self._break)

        self._date: QDateEdit = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.dateChanged.connect(lambda x: self._set_day_date_edit())
        self._meeting_time: QTimeEdit = QTimeEdit()
        self._meeting_time.setCalendarPopup(True)
        self._meeting_time.timeChanged.connect(lambda x: self._set_day_edit_mode())
        self._meeting_location_box: QComboBox = QComboBox()
        self._meeting_location_box.currentTextChanged.connect(lambda x: self._set_day_edit_mode())
        self._uniform_le: QLineEdit = QLineEdit()
        self._uniform_le.textChanged.connect(lambda x: self._set_day_edit_mode())
        self._day_comment_text: QTextEdit = QTextEdit()
        self._day_comment_text.textChanged.connect(self._set_day_comment_edit)

        # entry
        self.entry_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_schedule_entry_names,
                                               list_method=self._entry_list_method, active=True)
        self._add_entry_btn: QPushButton = QPushButton("Eintrag hinzufügen")
        self._add_entry_btn.clicked.connect(self._add_entry)
        self._remove_entry_btn: QPushButton = QPushButton("Eintrag löschen")
        self._recover_entry_btn: QPushButton = QPushButton("Eintrag wieder herstellen")

        self._entry_title_le: QLineEdit = QLineEdit()
        self._entry_title_le.textChanged.connect(self._set_entry_name)
        self._entry_time: QTimeEdit = QTimeEdit()
        self._entry_time.timeChanged.connect(self._set_entry_edit_mode)
        self._entry_time.setCalendarPopup(True)
        self._entry_type_box: QComboBox = QComboBox()
        self._entry_type_box.currentTextChanged.connect(self._set_entry_edit_mode)
        self._entry_location_box: QComboBox = QComboBox()
        self._entry_location_box.currentTextChanged.connect(self._set_entry_edit_mode)
        self._entry_comment_text: QTextEdit = QTextEdit()
        self._entry_comment_text.textChanged.connect(self._set_entry_edit_mode)

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
        footer_hbox.addWidget(self._recover_entry_btn)
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

    def _set_window_information(self) -> None:
        self.setWindowTitle("Zeitplan")

    def _set_global_edit_mode(self) -> None:
        edit: bool = False
        invert_edit: bool = not edit

        self._save_btn.setEnabled(edit)
        self._break_btn.setEnabled(edit)

        self._day_list.list.setEnabled(invert_edit)
        self._add_day_btn.setEnabled(invert_edit)
        self._remove_day_btn.setEnabled(invert_edit)
        self._recover_day_btn.setEnabled(invert_edit)

        self.entry_list.setEnabled(invert_edit)
        self._add_entry_btn.setEnabled(invert_edit)
        self._remove_entry_btn.setEnabled(invert_edit)
        self._recover_entry_btn.setEnabled(invert_edit)

        self._open_list_btn.setEnabled(invert_edit)

        self._is_edit_mode = edit

    def _load_locations(self) -> None:
        locations, valid = transition.get_all_location_name()
        if not valid:
            self.set_error_bar(message=locations)
            return

        for ID, name, _ in locations:
            self._locations_ids.append((ID, name))
            self._meeting_location_box.addItem(name)
            self._entry_location_box.addItem(name)

    def _load_entry_types(self) -> None:
        entry_types, valid = transition.get_single_type(raw_type_id=c.config.raw_type_id['schedule_entry'], active=True)

        if not valid:
            self.set_error_bar(message=entry_types)
            return

        for ID, name, *_ in entry_types:
            self._entry_type_ids.append((ID, name))
            self._entry_type_box.addItem(name)

    def _save(self) -> None:
        message, valid = self._save_day()
        if not valid:
            self.set_error_bar(message=message)
            return

        message, valid = self._save_entry()
        if not valid:
            self.set_error_bar(message=message)
            return

        self._set_global_edit_mode()

        self.set_info_bar(message="saved")

    def _break(self) -> None:
        self._load_single_day()

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.schedule_window = None
        event.accept()  # TODO

    # day
    def _add_day(self) -> None:
        new_day: ListItem = ListItem(ID=None)
        self._day_list.list.addItem(new_day)
        self._day_list.list_items.append(new_day)

        self._day_list.list.setCurrentItem(new_day)
        self._set_day_None()
        self._set_day_name_in_day_list()

        self._set_day_edit_mode()

    def _set_day_edit_mode(self) -> None:
        edit: bool = True
        invert_edit: bool = not edit

        self._save_btn.setEnabled(edit)
        self._break_btn.setEnabled(edit)

        self._day_list.list.setEnabled(invert_edit)
        self._add_day_btn.setEnabled(invert_edit)
        self._remove_day_btn.setEnabled(invert_edit)
        self._recover_day_btn.setEnabled(invert_edit)

        self._open_list_btn.setEnabled(invert_edit)

        self._is_edit_mode = edit

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

    def _set_day_comment_edit(self) -> None:
        self._set_day_edit_mode()

    def _set_day_date_edit(self) -> None:
        self._set_day_name_in_day_list()
        self._set_day_edit_mode()

    def _load_single_day(self):
        current_day: ListItem = self._day_list.list.currentItem()
        if current_day is None:
            self._add_day()
            return

        data, valid = transition.get_schedule_day_by_ID(ID=current_day.ID, active=True)
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

        self._set_global_edit_mode()

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

    def _save_day_activity(self) -> None:
        current_day: ListItem = self._day_list.list.currentItem()

        message, valid = transition.save_schedule_day_activity(ID=current_day.ID, active=False)

        if not valid:
            self.set_error_bar(message=message)
            return

        self._day_list.load_list_data()
        self._load_single_day()
        self.set_info_bar(message="saved...")

    def _recover_day(self) -> None:
        message, valid = w_m.window_manger.is_valid_recover_window("schedule", ignore_schedule_window=True)
        if not valid:
            self.set_error_bar(message=message)
            return

        self.close()
        if w_m.window_manger.schedule_window is not None:
            self.set_error_bar(message="Fenster konnte nicht geschlossen werden.")
            return

        w_m.window_manger.recover_schedule_day_window = recover_window.RecoverWindow("schedule_day")

    # entry
    def _add_entry(self) -> None:
        new_entry: ListItem = ListItem(ID=None)
        self.entry_list.list.addItem(new_entry)
        self.entry_list.list_items.append(new_entry)

        self.entry_list.list.setCurrentItem(new_entry)
        self._set_entry_None()

        self._set_entry_edit_mode()

    def _set_entry_edit_mode(self, edit: bool = True) -> None:
        edit: bool = edit
        invert_edit: bool = not edit

        self.entry_list.setEnabled(invert_edit)
        self._add_entry_btn.setEnabled(invert_edit)
        self._remove_entry_btn.setEnabled(invert_edit)
        self._recover_entry_btn.setEnabled(invert_edit)

        if edit:
            self._set_day_edit_mode()

    def _set_entry_name(self) -> None:
        current_entry: ListItem = self.entry_list.list.currentItem()

        current_entry.first_name = self._entry_title_le.text().strip().title()
        current_entry.set_name()

        self._set_entry_edit_mode()

    def _set_entry_None(self) -> None:
        self._entry_title_le.setText("")
        self._entry_time.setTime(QTime(0, 0, 0))
        self._entry_comment_text.setText("")

    def _entry_list_method(self):
        pass  # TODO

    def _save_entry(self) -> tuple[str, bool]:
        current_entry: ListItem = self.entry_list.list.currentItem()
        if current_entry is None:
            return "Kein Eintrag vorhanden", False

        location: str = self._entry_location_box.currentText()
        for ID, name in self._locations_ids:
            if name == location:
                location: int = ID
                break

        entry_type: str = self._entry_type_box.currentText()
        for ID, name in self._entry_type_ids:
            if name == entry_type:
                entry_type: int = ID
                break

        output: dict = {
            "ID": current_entry.ID,
            "title": None if self._entry_title_le.text().strip() == "" else self._entry_title_le.text().strip().title(),
            "hour": self._entry_time.time().hour(),
            "minute": self._entry_time.time().minute(),
            "entry_type": entry_type,
            "location": location,
            "comment": None if self._entry_comment_text.toPlainText().strip() == "" \
                else self._entry_comment_text.toPlainText().strip(),
        }

        ID, valid = transition.save_schedule_entry(data=output)
        if not valid:
            return ID, False

        if isinstance(ID, int):
            current_entry.ID = ID

        return "", True
