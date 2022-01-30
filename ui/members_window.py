# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from PyQt5.QtCore import QDate, Qt, QDateTime
from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit

from ui.base_window import BaseWindow
from ui.enum_sheet import EditLineType, DateType
from ui import enum_sheet
import transition
from logic.enum_sheet import MemberEntries, SQLite_Table

members_window_: "MembersWindow" or None = None


class MemberListItem(QListWidgetItem):
    def __init__(self, id_: int | None = None):
        super().__init__()
        self.id_: int | None = id_
        self.first_name: str | None = None
        self.last_name: str | None = None

        self.street: str | None = None
        self.number: str | None = None
        self.zip_code: str | None = None
        self.city: str | None = None

        self.birth_date: QDate = QDate()
        self.entry_date: QDate = QDate()

        self.phone_numbers: dict[str, str] = dict()
        self.mail_addresses: dict[str, str] = dict()

        self.membership_type: str | None = None
        self.special_member: bool = False
        self.positions: list[PositionInstrumentListItem] = list()
        self.instruments: list[PositionInstrumentListItem] = list()

        self.comment_text: str | None = None

        self.set_name()

    def set_name(self) -> None:
        if self.first_name or self.last_name:
            text_: str = str()
            if self.first_name:
                text_ += self.first_name.strip()
            if self.first_name and self.last_name:
                text_ += " "
            if self.last_name:
                text_ += self.last_name.strip()
            self.setText(text_)
        else:
            self.setText("Kein Name vorhanden")


class PositionInstrumentListItem(QListWidgetItem):
    def __init__(self, name_str):
        super().__init__()
        self.name: str = name_str
        self._set_name()

    def _set_name(self):
        self.setText(self.name)


# noinspection PyArgumentList
class MembersWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._member_counter: int = int()
        self._positions: list[PositionInstrumentListItem] = list()
        self._instruments: list[PositionInstrumentListItem] = list()

        self._set_ui()
        self._set_layout()
        self._add_member()
        self._create_positions()
        self._create_instruments()
        self._create_phone_number_types()
        self._create_mail_address_types()
        self._create_member_types()
        self._load_data()

    def _set_ui(self) -> None:
        # Left
        self._members_lb: QLabel = QLabel()
        self._members_lb.setText("Mitglieder:")

        self._members_list: QListWidget = QListWidget()
        self._members_list.itemClicked.connect(self._set_current_member)

        self._add_member_btn: QPushButton = QPushButton()
        self._add_member_btn.setText("Mitglied hinzufügen")
        self._add_member_btn.clicked.connect(self._add_member)
        self._remove_member_btn: QPushButton = QPushButton()
        self._remove_member_btn.setText("Mitglied löschen")
        self._remove_member_btn.clicked.connect(self._remove_member)

        self._save_single_btn: QPushButton = QPushButton()
        self._save_single_btn.setText("Mitglied speichern")
        self._save_single_btn.clicked.connect(self._save_member)
        self._save_all_btn: QPushButton = QPushButton()
        self._save_all_btn.setText("Alles speichern")
        self._save_all_btn.clicked.connect(self._save_all)

        # Right
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._first_name_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.FIRST_NAME))
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.LAST_NAME))

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.STREET))
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.HOUSE_NUMBER))
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.ZIP_CODE))
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.CITY))

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._b_day_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._b_day_date.dateChanged.connect(lambda x: self._current_date_chanced(DateType.B_DAY))
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._entry_date.dateChanged.connect(lambda x: self._current_date_chanced(DateType.ENTRY))

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_type_box.currentTextChanged.connect(self._set_phone_number_type)
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")
        self._phone_number_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.PHONE_NUMBER))

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_type_box.currentTextChanged.connect(self._set_mail_address_type)
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")
        self._mail_address_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.MAIL_ADDRESS))

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._membership_type_box.currentTextChanged.connect(self._set_membership_type)
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.toggled.connect(self._set_special_member)
        self._special_member_cb.setText("Ehrenmitglied" if enum_sheet.user.lower() not in enum_sheet.special_user
                                        else enum_sheet.special_user[enum_sheet.user.lower()])

        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()
        self._positions_list.itemClicked.connect(self._set_position)

        self._instruments_lb: QLabel = QLabel()
        self._instruments_lb.setText("Instrumente:")
        self._instruments_list: QListWidget = QListWidget()
        self._instruments_list.itemClicked.connect(self._set_instruments)

        self._comment_lb: QLabel = QLabel()
        self._comment_lb.setText("Kommentar:")
        self._comment_text: QTextEdit = QTextEdit()
        self._comment_text.textChanged.connect(self._comment_chanced)

    def _set_layout(self) -> None:
        # Left
        label_members_hbox: QHBoxLayout = QHBoxLayout()
        label_members_hbox.addWidget(self._members_lb)
        label_members_hbox.addStretch()

        button_members_hbox: QHBoxLayout = QHBoxLayout()
        button_members_hbox.addWidget(self._add_member_btn)
        button_members_hbox.addWidget(self._remove_member_btn)
        button_members_hbox.addStretch()
        button_members_hbox.addWidget(self._save_single_btn)
        button_members_hbox.addWidget(self._save_all_btn)

        row: int = 0
        # Right
        # name
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._first_name_lb, row, 0, 1, 1)
        grid.addWidget(self._first_name_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._last_name_lb, row, 0, 1, 1)
        grid.addWidget(self._last_name_le, row, 1, 1, -1)

        # address
        row += 1
        grid.addWidget(self._address_lb, row, 0)
        grid.addWidget(self._street_le, row, 1, 1, 2)
        grid.addWidget(self._number_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._zip_code_le, row, 1)
        grid.addWidget(self._city_le, row, 2)

        row += 1
        grid.addWidget(self._birth_lb, row, 0)
        grid.addWidget(self._b_day_date, row, 1)
        grid.addWidget(self._entry_lb, row, 2, alignment=Qt.AlignRight)
        grid.addWidget(self._entry_date, row, 3, 1, -1)

        # phone
        row += 1
        grid.addWidget(self._phone_numbers_lb, row, 0)
        grid.addWidget(self._phone_number_type_box, row, 1)
        grid.addWidget(self._phone_number_le, row, 2, 1, -1)

        # mail
        row += 1
        grid.addWidget(self._mail_address_lb, row, 0)
        grid.addWidget(self._mail_address_type_box, row, 1)
        grid.addWidget(self._mail_address_le, row, 2, 1, -1)

        # member_type
        row += 1
        grid.addWidget(self._member_lb, row, 0)
        grid.addWidget(self._membership_type_box, row, 1)
        grid.addWidget(self._special_member_cb, row, 2)

        # positions / instruments
        row += 1
        grid.addWidget(self._positions_lb, row, 0, 1, 2)
        grid.addWidget(self._instruments_lb, row, 2, 1, -1)

        row += 1
        grid.addWidget(self._positions_list, row, 0, 1, 2)
        grid.addWidget(self._instruments_list, row, 2, 1, -1)

        # comment
        row += 1
        grid.addWidget(self._comment_lb, 10, 0, 1, -1)
        row += 1
        grid.addWidget(self._comment_text, 11, 0, 1, -1)

        right_vbox: QVBoxLayout = QVBoxLayout()
        right_vbox.addLayout(grid)
        right_vbox.addStretch()

        # Global
        sub_global_hbox: QHBoxLayout = QHBoxLayout()
        sub_global_hbox.addWidget(self._members_list)
        sub_global_hbox.addLayout(right_vbox)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(label_members_hbox)
        global_vbox.addLayout(sub_global_hbox)
        global_vbox.addLayout(button_members_hbox)

        # set Layout
        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget)
        self.show()

    def _create_positions(self) -> None:
        for position_name in enum_sheet.position_types:
            new_position: PositionInstrumentListItem = PositionInstrumentListItem(position_name)
            self._positions.append(new_position)
            self._positions_list.addItem(new_position)

    def _create_instruments(self) -> None:
        for instrument_name in enum_sheet.instrument_types:
            new_instrument: PositionInstrumentListItem = PositionInstrumentListItem(instrument_name)
            self._instruments.append(new_instrument)
            self._instruments_list.addItem(new_instrument)

    def _create_phone_number_types(self) -> None:
        for phone_number_type in enum_sheet.phone_number_types:
            self._phone_number_type_box.addItem(phone_number_type)

    def _create_mail_address_types(self) -> None:
        for mail_type in enum_sheet.mail_types:
            self._mail_address_type_box.addItem(mail_type)

    def _create_member_types(self) -> None:
        for membership_type in enum_sheet.membership_type:
            self._membership_type_box.addItem(membership_type)

    def _set_current_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        # name
        self._first_name_le.setText(current_member.first_name)
        self._last_name_le.setText(current_member.last_name)

        # address
        self._street_le.setText(current_member.street)
        self._number_le.setText(current_member.number)
        self._zip_code_le.setText(current_member.zip_code)
        self._city_le.setText(current_member.city)

        # date
        if not current_member.birth_date.isNull():
            self._b_day_date.setDate(current_member.birth_date)
        if not current_member.entry_date.isNull():
            self._entry_date.setDate(current_member.entry_date)

        # phone number
        self._set_phone_number_type()

        # mail address
        self._set_mail_address_type()

        # membership type
        self._membership_type_box.setCurrentText(current_member.membership_type)

        # special member
        self._special_member_cb.setChecked(current_member.special_member)

        # position list
        for position in self._positions:
            if position in current_member.positions:
                position.setBackground(QColor("Light Grey"))
            else:
                position.setBackground(QColor("White"))

        # instrument list
        for instrument in self._instruments:
            if instrument in current_member.instruments:
                instrument.setBackground(QColor("Light Grey"))
            else:
                instrument.setBackground(QColor("White"))

        # comment
        self._comment_text.setText(current_member.comment_text)

    def _set_position(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_position: PositionInstrumentListItem = self._positions_list.currentItem()

        if current_position not in current_member.positions:
            current_member.positions.append(current_position)
            current_position.setBackground(QColor("Light Grey"))

        else:
            current_member.positions.remove(current_position)
            current_position.setBackground(QColor("White"))

        self._positions_list.setCurrentItem(None)

    def _set_instruments(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_instrument: PositionInstrumentListItem = self._instruments_list.currentItem()

        if current_instrument not in current_member.instruments:
            current_member.instruments.append(current_instrument)
            current_instrument.setBackground(QColor("Light Grey"))

        else:
            current_member.instruments.remove(current_instrument)
            current_instrument.setBackground(QColor("White"))

        self._instruments_list.setCurrentItem(None)

    def _set_special_member(self) -> None:
        current_item: MemberListItem = self._members_list.currentItem()
        current_item.special_member = (self._special_member_cb.isChecked())

    def _set_membership_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_member.membership_type = self._membership_type_box.currentText()

    def _set_phone_number_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_type: str = self._phone_number_type_box.currentText()
        if current_type in current_member.phone_numbers:
            self._phone_number_le.setText(current_member.phone_numbers[current_type])
        else:
            self._phone_number_le.clear()

    def _set_mail_address_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_type: str = self._mail_address_type_box.currentText()
        if current_type in current_member.mail_addresses:
            self._mail_address_le.setText(current_member.mail_addresses[current_type])
        else:
            self._mail_address_le.clear()

    def _current_le_text_chanced(self, edit_line: EditLineType) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        match edit_line:
            case EditLineType.FIRST_NAME:
                current_member.first_name = self._first_name_le.text().strip() \
                    if self._first_name_le.text().strip() else None
                current_member.set_name()
            case EditLineType.LAST_NAME:
                current_member.last_name = self._last_name_le.text().strip() \
                    if self._last_name_le.text().strip() else None
                current_member.set_name()

            case EditLineType.STREET:
                current_member.street = self._street_le.text().strip() \
                    if self._street_le.text().strip() else None
            case EditLineType.HOUSE_NUMBER:
                current_member.number = self._number_le.text().strip() \
                    if self._number_le.text().strip().lower() else None
            case EditLineType.ZIP_CODE:
                current_member.zip_code = self._zip_code_le.text().strip() \
                    if self._zip_code_le.text().strip() else None
            case EditLineType.CITY:
                current_member.city = self._city_le.text().strip() \
                    if self._city_le.text().strip() else None

            case EditLineType.PHONE_NUMBER:
                current_phone_number_type: str = self._phone_number_type_box.currentText()
                if len(self._phone_number_le.text().strip()) > 0:
                    current_member.phone_numbers[current_phone_number_type] = self._phone_number_le.text().strip()
                elif current_phone_number_type in current_member.phone_numbers:
                    del current_member.phone_numbers[current_phone_number_type]

            case EditLineType.MAIL_ADDRESS:
                current_mail_address_type: str = self._mail_address_type_box.currentText()
                if len(self._mail_address_le.text().strip()) > 0:
                    current_member.mail_addresses[current_mail_address_type] = self._mail_address_le.text().strip()
                elif current_mail_address_type in current_member.mail_addresses:
                    del current_member.mail_addresses[current_mail_address_type]

    def _current_date_chanced(self, date_type: DateType) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        match date_type:
            case DateType.B_DAY:
                if self._b_day_date.date().isValid():
                    current_member.birth_date = self._b_day_date.date()
                else:
                    self.set_status_bar("Invalides Geburtsdatum")

            case DateType.ENTRY:
                if self._entry_date.date().isValid():
                    current_member.entry_date = self._entry_date.date()
                else:
                    self.set_status_bar("Invalides Eintrittsdatum")

    def _comment_chanced(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_member.comment_text = self._comment_text.toPlainText().strip() \
            if self._comment_text.toPlainText().strip() else None

    def _is_valid_input(self) -> bool:
        return True

    def _add_member(self) -> None:
        new_member: MemberListItem = MemberListItem()
        self._members_list.addItem(new_member)
        self._members_list.setCurrentItem(new_member)
        self._set_current_member()
        self._phone_number_type_box.setCurrentText(enum_sheet.phone_number_types[0])
        self._mail_address_type_box.setCurrentText(enum_sheet.mail_types[0])
        self._membership_type_box.setCurrentText(enum_sheet.membership_type[0])
        self._member_counter += 1

    def _remove_member(self) -> None:
        if self._member_counter == 0:
            self.set_status_bar("Keine Mitglieder vorhanden.")
            return
        else:
            current_row: int = self._members_list.currentRow()
            self._members_list.takeItem(current_row)
            self._member_counter -= 1

            if self._member_counter == 0:
                self._add_member()

            self._set_current_member()

    def _load_data(self) -> None:
        load_data: list[dict] = transition.load_data(table=SQLite_Table.MEMBERS)
        print(load_data)
        if len(load_data) > 0:
            self._member_counter: int = len(load_data) + 1
            self._members_list.clear()
            for single_data in load_data:
                new_member: MemberListItem = MemberListItem(id_=single_data[MemberEntries.ID])

                new_member.first_name = single_data[MemberEntries.FIRST_NAME] or None
                new_member.last_name = single_data[MemberEntries.LAST_NAME] or None
                new_member.set_name()

                new_member.street = single_data[MemberEntries.STREET] or None
                new_member.number = single_data[MemberEntries.NUMBER] or None
                new_member.zip_code = single_data[MemberEntries.ZIP_CODE] or None
                new_member.city = single_data[MemberEntries.CITY] or None

                new_member.birth_date = QDateTime(single_data[MemberEntries.BIRTH_DAY]).date() if single_data[MemberEntries.BIRTH_DAY] else QDate()
                new_member.entry_date = QDateTime(single_data[MemberEntries.ENTRY_DATE]).date() if single_data[MemberEntries.ENTRY_DATE] else QDate()

                new_member.phone_numbers = single_data[MemberEntries.PHONE_NUMBERS] or None
                new_member.mail_addresses = single_data[MemberEntries.MAIL_ADDRESSES] or None

                new_member.membership_type = single_data[MemberEntries.MEMBERSHIP_TYPE] or None
                new_member.special_member = single_data[MemberEntries.SPECIAL_MEMBER]
                if len(single_data[MemberEntries.INSTRUMENTS]) >0:
                    for instrument in single_data[MemberEntries.INSTRUMENTS]:
                        if instrument in enum_sheet.instrument_types:
                            for instrument_type in self._instruments:
                                if instrument == instrument_type.name:
                                    new_member.instruments.append(instrument_type)
                    else:
                        pass
                if len(single_data[MemberEntries.POSITIONS]) >0:
                    for position in single_data[MemberEntries.POSITIONS]:
                        if position in enum_sheet.position_types:
                            for position_type in self._positions:
                                if position == position_type.name:
                                    new_member.positions.append(position_type)
                        else:
                            pass

                new_member.comment_text = single_data[MemberEntries.COMMENT_TEXT] or None
                self._members_list.addItem(new_member)
            self._members_list.setCurrentRow(0)

    @staticmethod
    def _get_save_data(current_member: MemberListItem) -> dict:
        positions: list[str] = list()
        for position in current_member.positions:
            positions.append(position.name)

        instruments: list[str] = list()
        for instrument in current_member.instruments:
            instruments.append(instrument.name)

        member_output: dict = {
            MemberEntries.ID: current_member.id_,

            MemberEntries.FIRST_NAME: current_member.first_name,
            MemberEntries.LAST_NAME: current_member.last_name,

            MemberEntries.STREET: current_member.street,
            MemberEntries.NUMBER: current_member.number,
            MemberEntries.ZIP_CODE: current_member.zip_code,
            MemberEntries.CITY: current_member.city,

            MemberEntries.BIRTH_DAY: current_member.birth_date.toPyDate() if not current_member.birth_date.isNull() else None,
            MemberEntries.ENTRY_DATE: current_member.entry_date.toPyDate()if not current_member.entry_date.isNull() else None,

            MemberEntries.PHONE_NUMBERS: current_member.phone_numbers,
            MemberEntries.MAIL_ADDRESSES: current_member.mail_addresses,

            MemberEntries.MEMBERSHIP_TYPE: current_member.membership_type,
            MemberEntries.SPECIAL_MEMBER: current_member.special_member,
            MemberEntries.POSITIONS: positions,
            MemberEntries.INSTRUMENTS: instruments,

            MemberEntries.COMMENT_TEXT: current_member.comment_text}

        return member_output

    def _save_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if self._is_valid_input():
            transition.save_data(data=[self._get_save_data(current_member=current_member)], table=SQLite_Table.MEMBERS)

    def _save_all(self) -> None:
        all_member_output: list[dict] = list()
        for index in range(self._members_list.count()):
            current_member = self._members_list.item(index)
            all_member_output.append(self._get_save_data(current_member=current_member))
        transition.save_data(data=all_member_output, table=SQLite_Table.MEMBERS)
