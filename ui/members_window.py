# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from datetime import date

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIntValidator, QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit
from enum import Enum

import main
from ui.base_window import BaseWindow
from enum_sheet import TypeType, MemberTypes, TableTypes

members_window_: "MembersWindow" or None = None


class LineEditType(Enum):
    FIRSTNAME = 0
    LASTNAME = 1
    STREET = 2
    NUMBER = 3
    ZIP_CODE = 4
    CITY = 5
    COMMENT = 6


class DateType:
    ENTRY = 0
    B_DAY = 1


class MemberListItem(QListWidgetItem):
    def __init__(self, id_: int | None = None, firstname: str | None = None, lastname: str | None = None):
        super().__init__()
        self.member_id_: int = id_
        self.first_name: str = firstname
        self.last_name: str = lastname

        self.street: str | None = None
        self.number: str | None = None
        self.zip_code: str | None = None
        self.city: str | None = None

        self.birth_date: QDate = QDate()
        self.entry_date: QDate = QDate()

        self.phone_numbers: dict[str, str] = dict()  # {type:number}
        self.phone_member_ids: dict[str, int | None] = dict()  # {type:ID}
        self.mail_addresses: dict[str, str] = dict()  # {type:mail}
        self.mail_member_ids: dict[str, int | None] = dict()  # {type:ID}

        self.membership_type: str | None = None
        self.special_member: bool = False
        self.positions: list[PositionListItem] = list()
        self.position_member_ids: dict[str, int] = dict()  # {position:ID}

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


class PositionListItem(QListWidgetItem):
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
        self._positions_items: list[PositionListItem] = list()
        self._is_edit: bool = False
        self.member_counter: int = int()

        self.phone_number_ids: list[tuple] = list()
        self.mail_ids: list[tuple] = list()
        self.position_ids: list[tuple] = list()

        self._set_ui()
        self._set_layout()

        self._load_all_member_names()
        self._set_types()
        self._set_edit_mode()

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
        self._remove_member_btn.clicked.connect(self._delete)

        self._break_btn: QPushButton = QPushButton()
        self._break_btn.setText("Zurücksetzten")
        self._break_btn.setEnabled(False)
        self._save_btn: QPushButton = QPushButton()
        self._save_btn.setText("Speichern")
        self._save_btn.setEnabled(False)
        self._save_btn.clicked.connect(self._save)

        # Right
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._first_name_le.textChanged.connect(lambda: self._set_el_input(LineEditType.FIRSTNAME))
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda: self._set_el_input(LineEditType.LASTNAME))

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda: self._set_el_input(LineEditType.STREET))
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_el_input(LineEditType.NUMBER))
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda: self._set_el_input(LineEditType.ZIP_CODE))
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_el_input(LineEditType.CITY))

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._b_day_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._b_day_date.dateChanged.connect(lambda: self._set_date(type_=DateType.B_DAY))
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._entry_date.dateChanged.connect(lambda: self._set_date(type_=DateType.ENTRY))

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_type_box.currentTextChanged.connect(self._set_phone_type)
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")
        self._phone_number_le.textChanged.connect(self._set_phone_number_input)

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_type_box.currentTextChanged.connect(self._set_mail_type)
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")
        self._mail_address_le.textChanged.connect(self._set_mail_input)

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._membership_type_box.currentTextChanged.connect(self._set_membership_type)
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.setText("Ehrenmitglied")
        self._special_member_cb.toggled.connect(self._set_special_member)
        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()
        self._positions_list.itemClicked.connect(self._set_position)

        self._comment_lb: QLabel = QLabel()
        self._comment_lb.setText("Kommentar:")
        self._comment_text: QTextEdit = QTextEdit()
        self._comment_text.textChanged.connect(lambda: self._set_el_input(LineEditType.COMMENT))

    def _set_layout(self) -> None:
        # Left
        label_members_hbox: QHBoxLayout = QHBoxLayout()
        label_members_hbox.addWidget(self._members_lb)
        label_members_hbox.addStretch()

        button_members_hbox: QHBoxLayout = QHBoxLayout()
        button_members_hbox.addWidget(self._add_member_btn)
        button_members_hbox.addWidget(self._remove_member_btn)
        button_members_hbox.addStretch()
        button_members_hbox.addWidget(self._break_btn)
        button_members_hbox.addWidget(self._save_btn)

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

        # positions / comment
        row += 1
        grid.addWidget(self._positions_lb, row, 0, 1, 2)
        grid.addWidget(self._comment_lb, row, 2, 1, -1)

        row += 1
        grid.addWidget(self._positions_list, row, 0, 1, 2)
        grid.addWidget(self._comment_text, row, 2, 1, -1)

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

    def _set_types(self) -> None:
        position_, membership_, phone_number_, mail_ = main.get_types(type_=TypeType.MEMBER)

        positions: list = main.get_type_list(display_name=position_)
        for ID, position in positions:
            new_position: PositionListItem = PositionListItem(position)
            self._positions_items.append(new_position)
            self._positions_list.addItem(new_position)
            self.position_ids.append((ID, position))

        memberships: list = main.get_type_list(display_name=membership_)

        for _, membership in memberships:
            self._membership_type_box.addItem(membership)
        if self._membership_type_box.currentText().strip() == "":
            self._membership_type_box.setEnabled(False)
            self._special_member_cb.setEnabled(False)
        self._membership_type_box.addItem("")
        self._membership_type_box.setCurrentText("")

        phone_numbers: list = main.get_type_list(display_name=phone_number_)
        for ID, phone_number in phone_numbers:
            self._phone_number_type_box.addItem(phone_number)
            self.phone_number_ids.append((ID, phone_number))
        if self._phone_number_type_box.currentText().strip() == "":
            self._phone_number_type_box.setEnabled(False)
            self._phone_number_le.setEnabled(False)

        mails: list = main.get_type_list(display_name=mail_)
        for ID, mail in mails:
            self._mail_address_type_box.addItem(mail)
            self.mail_ids.append((ID, mail))
        if self._mail_address_type_box.currentText().strip() == "":
            self._mail_address_type_box.setEnabled(False)
            self._mail_address_le.setEnabled(False)

    def _set_edit_mode(self) -> None:
        invert_edit = not self._is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._members_list.setEnabled(invert_edit)
        self._add_member_btn.setEnabled(invert_edit)
        self._remove_member_btn.setEnabled(invert_edit)

    def _set_current_member(self) -> None:
        self._load_single_member()
        current_member: MemberListItem = self._members_list.currentItem()

        self._first_name_le.setText(current_member.first_name)
        self._last_name_le.setText(current_member.last_name)
        self._street_le.setText(current_member.street)
        self._number_le.setText(current_member.number)
        self._zip_code_le.setText(str(current_member.zip_code))
        self._city_le.setText(current_member.city)
        self._comment_text.setText(current_member.comment_text)
        self._special_member_cb.setChecked(current_member.special_member)

        # membership
        if current_member.membership_type is not None:
            self._membership_type_box.setCurrentText(current_member.membership_type)
        else:
            self._membership_type_box.setCurrentText("")

        # birthday
        if not current_member.birth_date.isNull():
            self._b_day_date.setDate(current_member.birth_date)
        else:
            self._b_day_date.setDate(QDate().currentDate())
            current_member.birth_date = QDate()

        # entry day
        if not current_member.entry_date.isNull():
            self._entry_date.setDate(current_member.entry_date)
        else:
            self._entry_date.setDate(QDate().currentDate())
            current_member.entry_date = QDate()

        # phone number
        try:
            self._phone_number_le.setText(current_member.phone_numbers[self._phone_number_type_box.currentText()])
        except KeyError:
            self._phone_number_le.setText("")

        # mail
        try:
            self._mail_address_le.setText(current_member.mail_addresses[self._mail_address_type_box.currentText()])
        except KeyError:
            self._mail_address_le.setText("")

        # positions
        for position in self._positions_items:
            if position in current_member.positions:
                position.setBackground(QColor("light grey"))
            else:
                position.setBackground(QColor("white"))

        self._is_edit = False
        self._set_edit_mode()

    def _set_el_input(self, type_: LineEditType) -> None:
        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()
        current_member: MemberListItem = self._members_list.currentItem()
        match type_:
            case LineEditType.FIRSTNAME:
                current_member.first_name = self._first_name_le.text().strip().title()
                current_member.set_name()
            case LineEditType.LASTNAME:
                current_member.last_name = self._last_name_le.text().strip().title()
                current_member.set_name()
            case LineEditType.STREET:
                current_member.street = self._street_le.text().strip().title()
            case LineEditType.NUMBER:
                current_member.number = self._number_le.text().strip()
            case LineEditType.ZIP_CODE:
                current_member.zip_code = self._zip_code_le.text().strip()
            case LineEditType.CITY:
                current_member.city = self._city_le.text().strip().title()
            case LineEditType.COMMENT:
                current_member.comment_text = self._comment_text.toPlainText().strip()

    def _set_date(self, type_: DateType) -> None:
        current_member: MemberListItem = self._members_list.currentItem()

        match type_:
            case DateType.B_DAY:
                current_member.birth_date = self._b_day_date.date()
            case DateType.ENTRY:
                current_member.entry_date = self._entry_date.date()

        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _set_phone_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if current_member is not None:
            try:
                self._phone_number_le.setText(current_member.phone_numbers[self._phone_number_type_box.currentText()])
            except KeyError:
                self._phone_number_le.setText(None)

    def _set_phone_number_input(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if len(self._phone_number_le.text().strip()) > 0 or \
                self._phone_number_type_box.currentText() in current_member.phone_numbers:
            current_member.phone_numbers[
                self._phone_number_type_box.currentText()] = self._phone_number_le.text().strip()
        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _set_mail_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if current_member is not None:
            try:
                self._mail_address_le.setText(current_member.mail_addresses[self._mail_address_type_box.currentText()])
            except KeyError:
                self._mail_address_le.setText(None)

    def _set_mail_input(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if len(self._mail_address_le.text().strip()) > 0 or \
                self._mail_address_type_box.currentText() in current_member.mail_addresses:
            current_member.mail_addresses[
                self._mail_address_type_box.currentText()] = self._mail_address_le.text().strip()
        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _set_membership_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if self._membership_type_box.currentText() == "":
            current_member.membership_type = None
        else:
            current_member.membership_type = self._membership_type_box.currentText()

        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _set_special_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_member.special_member = self._special_member_cb.isChecked()
        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _set_position(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_position: PositionListItem = self._positions_list.currentItem()
        if current_position in current_member.positions:
            current_member.positions.remove(current_position)
            current_position.setBackground(QColor("white"))
        else:
            current_member.positions.append(current_position)
            current_position.setBackground(QColor("light grey"))
        self._positions_list.setCurrentItem(None)
        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

    def _add_member(self) -> None:
        new_member: MemberListItem = MemberListItem()
        self._members_list.addItem(new_member)
        self._members_list.setCurrentItem(new_member)
        self._set_current_member()
        self._is_edit = True
        self._set_edit_mode()
        self.member_counter += 1

    def _load_all_member_names(self) -> None:
        member_names: list = main.load_all_member_names(True)
        self.counter = 0
        for member_id, first_name, last_name in member_names:
            new_member: MemberListItem = MemberListItem(id_=member_id, firstname=first_name, lastname=last_name)
            self._members_list.addItem(new_member)
            self.counter += 1
        if self.counter > 0:
            self._members_list.setCurrentRow(0)
            self._set_current_member()
        else:
            self._add_member()

    def _load_single_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        data = main.load_data_from_single_member(current_member.member_id_)
        print(data)
        if len(data) == 0:
            return
        birth_date: date
        entry_date: date
        id_, first_name, last_name, street, number, zip_code, city, \
        birth_date, entry_date, membership_type, special_member, comment_text = data
        current_member.first_name = first_name
        current_member.last_name = last_name
        current_member.street = street
        current_member.number = number
        current_member.zip_code = zip_code
        current_member.city = city
        current_member.birth_date = QDate(birth_date.year, birth_date.month, birth_date.day) \
            if birth_date is not None else QDate()
        current_member.entry_date = QDate(entry_date.year, entry_date.month, entry_date.day) \
            if entry_date is not None else QDate()
        current_member.membership_type = membership_type
        current_member.special_member = special_member
        current_member.comment_text = comment_text

    def _save(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        output, new_ = self._get_member_save_data()

        if new_:
            id_: int = main.save_member(output=output)
            current_member.member_id_ = id_
            output[MemberTypes.ID.value] = id_
        else:
            main.update_member(output=output)

        main.save_member_nexus(member_id=output[MemberTypes.ID.value], table_type=TableTypes.MEMBER_PHONE,
                               output=self._get_member_nexus_save_data(table_type=TableTypes.MEMBER_PHONE))
        main.save_member_nexus(member_id=output[MemberTypes.ID.value], table_type=TableTypes.MEMBER_MAIL,
                               output=self._get_member_nexus_save_data(table_type=TableTypes.MEMBER_MAIL))
        main.save_member_nexus(member_id=output[MemberTypes.ID.value], table_type=TableTypes.MEMBER_POSITION,
                               output=self._get_member_nexus_save_data(table_type=TableTypes.MEMBER_POSITION))

        self._is_edit = False
        self._set_edit_mode()

    def _delete(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_index: int = self._members_list.currentRow()
        main.delete_recover_member([current_member.member_id_, False])
        self._members_list.takeItem(current_index)
        self.member_counter -= 1
        if self.member_counter == 0:
            self._add_member()

    def _get_member_save_data(self) -> [dict, bool]:
        current_member: MemberListItem = self._members_list.currentItem()

        output: dict = {
            MemberTypes.FIRST_NAME.value: current_member.first_name,
            MemberTypes.LAST_NAME.value: current_member.last_name,
            MemberTypes.STREET.value: current_member.street,
            MemberTypes.NUMBER.value: current_member.number,
            MemberTypes.ZIP_CODE.value: current_member.zip_code,
            MemberTypes.CITY.value: current_member.city,
            MemberTypes.B_DAY_DATE.value: current_member.birth_date.toPyDate() \
                if not current_member.birth_date.isNull() else None,
            MemberTypes.ENTRY_DATE.value: current_member.entry_date.toPyDate() \
                if not current_member.entry_date.isNull() else None,
            MemberTypes.MEMBERSHIP_TYPE.value: current_member.membership_type,
            MemberTypes.SPECIAL_MEMBER.value: current_member.special_member,
            MemberTypes.COMMENT.value: current_member.comment_text
        }

        new_: bool = True
        if current_member.member_id_ is not None:
            new_ = False
            output[MemberTypes.ID.value] = current_member.member_id_

        return output, new_

    def _get_member_nexus_save_data(self, table_type: TableTypes) -> tuple:
        current_member: MemberListItem = self._members_list.currentItem()
        dummy_values = list()
        dummy_ids = list()

        match table_type:
            case TableTypes.MEMBER_PHONE:
                dummy_values = current_member.phone_numbers.items()
                dummy_ids = current_member.phone_member_ids.items()
            case TableTypes.MEMBER_MAIL:
                dummy_values = current_member.mail_addresses.items()
                dummy_ids = current_member.mail_member_ids.items()
            case TableTypes.MEMBER_POSITION:
                dummy_values = list()
                for position in current_member.positions:
                    dummy_values.append([position.name, position.name])
                dummy_ids = current_member.position_member_ids.items()

        output: list = list()  # [ID,value]
        for value_type, value in dummy_values:  # {type:value}
            inner: list = list()
            for ID_type, ID in dummy_ids:  # {type:ID}
                if value_type == ID_type:
                    inner.append(ID)
            if len(inner) == 0:
                inner.append(None)
            inner.append(self._get_id_from_type(type_=value_type, table_type=table_type))
            inner.append(value_type)
            inner.append(value)
            output.append(tuple(inner))
        return tuple(output)  # (member_id,table_type,((member,phone_id,phone_type_id,number),(next_number))

    def _get_id_from_type(self, type_: str, table_type: TableTypes) -> int:
        dummy: list = list()
        match table_type:
            case TableTypes.MEMBER_PHONE:
                dummy: list = self.phone_number_ids
            case TableTypes.MEMBER_MAIL:
                dummy: list = self.mail_ids
            case TableTypes.MEMBER_POSITION:
                dummy: list = self.position_ids

        for ID, entry in dummy:
            if entry == type_:
                return ID
