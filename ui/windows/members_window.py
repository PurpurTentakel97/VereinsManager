# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIntValidator, QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit, QFileDialog
from enum import Enum
import webbrowser

import transition
from ui.dialog.date_dialog import DateInput
from ui.windows.base_window import BaseWindow
from ui.windows import recover_window as r_w, member_table_window as m_t_w, window_manager as w, \
    member_anniversary_window as m_a_w
from ui.frames.list_frame import ListItem, ListFrame
from config import config_sheet as c
import debug

debug_str: str = "MembersWindow"


class LineEditType(Enum):
    FIRSTNAME = 0
    LASTNAME = 1
    ADDRESS = 2
    MAPS = 3
    OTHER = 4


class DateType(Enum):
    ENTRY = 0
    B_DAY = 1


class PositionListItem(QListWidgetItem):
    def __init__(self, name: str, raw_id: int, id_: int or None = None):
        super().__init__()
        self.name: str = name
        self.ID: int = id_
        self.raw_id: int = raw_id
        self.active: bool = bool()

        self._set_name()
        self.set_active()

    def _set_name(self):
        self.setText(self.name)

    def set_active(self, active: bool = False) -> None:
        self.active = active
        if self.active:
            self.setBackground(QColor("Light Grey"))
        else:
            self.setBackground(QColor("White"))


# noinspection PyArgumentList
class MembersWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.member_counter: int = int()

        self.raw_membership_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.raw_phone_number_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.raw_mail_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.raw_position_ids: list[tuple[int, PositionListItem]] = list()  # [ID, Name]

        self.phone_numbers: list[list[int, int, str, str]] = list()  # [ID, type_id, Type, number]
        self.mail_addresses: list[list[int, int, str, str]] = list()  # [ID, type_id, Type, mail]
        self.positions: list[list[int, int, PositionListItem, None]] = list()

        self._set_window_information()
        self._set_ui()
        self._set_layout()
        self._set_types()
        self._set_first_member()

        self._is_edit: bool = bool()
        self._set_edit_mode(active=False)
        self._set_maps()
        self._first_name_le.setFocus()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitglieder - Vereinsmanager")

    def _set_ui(self) -> None:
        # Left
        self._members_lb: QLabel = QLabel()
        self._members_lb.setText("Mitglieder:")
        self._table_btn: QPushButton = QPushButton()
        self._table_btn.setText("Tabelle")
        self._table_btn.clicked.connect(self._table)
        self._anniversary_btn: QPushButton = QPushButton()
        self._anniversary_btn.setText("Jubiläen")
        self._anniversary_btn.clicked.connect(self._anniversary)
        self._letter_btn: QPushButton = QPushButton()
        self._letter_btn.setText("Scheiben")
        self._letter_btn.clicked.connect(self._letter)
        self._member_card_btn: QPushButton = QPushButton()
        self._member_card_btn.setText("Mitliederkarte")
        self._member_card_btn.clicked.connect(self._member_card)

        self._members_list: ListFrame = ListFrame(window=self, type_="member", active=True)

        self._add_member_btn: QPushButton = QPushButton()
        self._add_member_btn.setText("Mitglied hinzufügen")
        self._add_member_btn.clicked.connect(self._add_member)
        self._remove_member_btn: QPushButton = QPushButton()
        self._remove_member_btn.setText("Mitglied löschen")
        self._remove_member_btn.clicked.connect(self._set_inactive)
        self._recover_member_btn: QPushButton = QPushButton()
        self._recover_member_btn.setText("Mitglied wieder herstellen")
        self._recover_member_btn.clicked.connect(self._recover)

        self._break_btn: QPushButton = QPushButton()
        self._break_btn.setText("Zurücksetzten")
        self._break_btn.setEnabled(False)
        self._break_btn.clicked.connect(self.load_single_member)
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
        self._first_name_le.returnPressed.connect(self._save)
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda: self._set_el_input(LineEditType.LASTNAME))
        self._last_name_le.returnPressed.connect(self._save)

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda: self._set_el_input(LineEditType.MAPS))
        self._street_le.returnPressed.connect(self._save)
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_el_input(LineEditType.MAPS))
        self._number_le.returnPressed.connect(self._save)
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda: self._set_el_input(LineEditType.MAPS))
        self._zip_code_le.returnPressed.connect(self._save)
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_el_input(LineEditType.MAPS))
        self._city_le.returnPressed.connect(self._save)

        self._maps_le: QLineEdit = QLineEdit()
        self._maps_le.setPlaceholderText("Google Maps URL (falls nötig // nicht empfohlen)")
        self._maps_le.textChanged.connect(lambda: self._set_el_input(LineEditType.MAPS))
        self._maps_le.returnPressed.connect(self._save)
        self._maps_btn: QPushButton = QPushButton()
        self._maps_btn.setText("Google Maps")
        self._maps_btn.clicked.connect(self._open_maps)

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._b_day_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._b_day_date.dateChanged.connect(self._set_date)
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._entry_date.dateChanged.connect(self._set_date)

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_type_box.currentTextChanged.connect(self._set_phone_type)
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")
        self._phone_number_le.textChanged.connect(self._set_phone_number_input)
        self._phone_number_le.returnPressed.connect(self._save)

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_type_box.currentTextChanged.connect(self._set_mail_type)
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")
        self._mail_address_le.textChanged.connect(self._set_mail_input)
        self._mail_address_le.returnPressed.connect(self._save)

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._membership_type_box.currentTextChanged.connect(self._set_membership_type)
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.setText(c.config.user['easter_egg'] if c.config.user['easter_egg'] else "Ehrenmitglied")
        self._special_member_cb.toggled.connect(self._set_special_member)
        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()
        self._positions_list.itemClicked.connect(self._set_position)

        self._comment_lb: QLabel = QLabel()
        self._comment_lb.setText("Kommentar:")
        self._comment_text: QTextEdit = QTextEdit()
        self._comment_text.textChanged.connect(lambda: self._set_el_input(LineEditType.OTHER))

    def _set_layout(self) -> None:
        # Top
        label_members_hbox: QHBoxLayout = QHBoxLayout()
        label_members_hbox.addWidget(self._members_lb)
        label_members_hbox.addStretch()
        label_members_hbox.addWidget(self._member_card_btn)
        label_members_hbox.addWidget(self._letter_btn)
        label_members_hbox.addWidget(self._anniversary_btn)
        label_members_hbox.addWidget(self._table_btn)

        # Bottom
        button_members_hbox: QHBoxLayout = QHBoxLayout()
        button_members_hbox.addWidget(self._add_member_btn)
        button_members_hbox.addWidget(self._remove_member_btn)
        button_members_hbox.addWidget(self._recover_member_btn)
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
        grid.addWidget(self._maps_le, row, 1, 1, 2)
        grid.addWidget(self._maps_btn, row, 3)

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
        data, valid = transition.get_active_member_type()
        if not valid:
            self.set_error_bar(message=data)
            return

        for ID, name, type_id, type_name in data:
            if type_id == c.config.raw_type_id["membership"]:
                self.raw_membership_ids.append((ID, name))
                self._membership_type_box.addItem(name)

            elif type_id == c.config.raw_type_id["mail"]:
                self.raw_mail_ids.append((ID, name))
                self._mail_address_type_box.addItem(name)
                self.mail_addresses.append([None, ID, name, None])

            elif type_id == c.config.raw_type_id["phone"]:
                self.raw_phone_number_ids.append((ID, name))
                self._phone_number_type_box.addItem(name)
                self.phone_numbers.append([None, ID, name, None])

            elif type_id == c.config.raw_type_id["position"]:
                new_position: PositionListItem = PositionListItem(name=name, raw_id=ID)
                self.raw_position_ids.append((ID, new_position))
                self._positions_list.addItem(new_position)
                self.positions.append([None, ID, new_position, None])

        if len(self.raw_phone_number_ids) == 0:
            self._phone_number_le.setEnabled(False)
        if len(self.raw_mail_ids) == 0:
            self._mail_address_le.setEnabled(False)
        if len(self.raw_membership_ids) == 0:
            self._special_member_cb.setEnabled(False)

    def _set_edit_mode(self, active: bool) -> None:
        self._is_edit = active
        invert_edit = not self._is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._members_list.list.setEnabled(invert_edit)
        self._add_member_btn.setEnabled(invert_edit)
        self._remove_member_btn.setEnabled(invert_edit)
        self._recover_member_btn.setEnabled(invert_edit)

    def _set_el_input(self, type_: LineEditType) -> None:
        current_member: ListItem = self._members_list.list.currentItem()
        match type_:
            case LineEditType.FIRSTNAME:
                current_member.first_name = self._first_name_le.text().strip().title()
                current_member.set_name()
            case LineEditType.LASTNAME:
                current_member.last_name = self._last_name_le.text().strip().title()
                current_member.set_name()
            case LineEditType.MAPS:
                self._set_maps()
            case LineEditType.OTHER:
                pass  # To trigger edit mode

        self._set_edit_mode(active=True)

    def _set_date(self) -> None:
        self._set_edit_mode(active=True)

    def _set_phone_type(self) -> None:
        current_type: str = self._phone_number_type_box.currentText()

        temp_is_edit: bool = self._is_edit
        for _, _, Type, phone in self.phone_numbers:
            if current_type == Type:
                self._phone_number_le.setText(phone)
                self._set_edit_mode(active=temp_is_edit)
                break

    def _set_phone_number_input(self) -> None:
        for item in self.phone_numbers:
            _, _, Type, phone = item
            if Type == self._phone_number_type_box.currentText():
                self.phone_numbers[self.phone_numbers.index(item)][3] = self._phone_number_le.text().strip()
                break

        self._set_edit_mode(active=True)

    def _set_mail_type(self) -> None:
        current_type: str = self._mail_address_type_box.currentText()

        temp_is_edit: bool = self._is_edit
        for _, _, Type, mail in self.mail_addresses:
            if current_type == Type:
                self._mail_address_le.setText(mail)
                self._set_edit_mode(active=temp_is_edit)
                break

    def _set_mail_input(self) -> None:
        for item in self.mail_addresses:
            _, _, Type, mail = item
            if Type == self._mail_address_type_box.currentText():
                self.mail_addresses[self.mail_addresses.index(item)][3] = self._mail_address_le.text().strip()
                break

        self._set_edit_mode(active=True)

    def _set_membership_type(self) -> None:
        self._set_edit_mode(active=True)

    def _set_special_member(self) -> None:
        self._set_edit_mode(active=True)

    def _set_position(self) -> None:
        current_position: PositionListItem = self._positions_list.currentItem()
        for _, _, item, _ in self.positions:
            if current_position.name == item.name:
                if item.active:
                    item.set_active(active=False)
                else:
                    item.set_active(active=True)
                break
        self._positions_list.setCurrentItem(None)
        self._set_edit_mode(active=True)

    def _set_first_member(self) -> None:
        try:
            self._members_list.list.setCurrentRow(0)
            self.load_single_member()
        except AttributeError:
            self._add_member()

    def _add_member(self) -> None:
        new_member: ListItem = ListItem(ID=None)
        self._load_nexus_types(type_="phone")
        self._load_nexus_types(type_="mail")
        self._load_nexus_types(type_="position")
        self._members_list.list.addItem(new_member)
        self._members_list.list.setCurrentItem(new_member)
        self._set_new_member()
        self.member_counter += 1
        self._set_edit_mode(active=True)

    def _set_new_member(self) -> None:
        self._set_phone_type()
        self._set_mail_type()

        self._first_name_le.setText("")
        self._last_name_le.setText("")
        self._street_le.setText("")
        self._number_le.setText("")
        self._zip_code_le.setText("")
        self._city_le.setText("")
        self._maps_le.setText("")
        self._comment_text.setText("")
        self._special_member_cb.setChecked(False)

        self._b_day_date.setDate(QDateTime().fromSecsSinceEpoch(c.config.date_format["None_date"]).date())
        self._entry_date.setDate(QDateTime().fromSecsSinceEpoch(c.config.date_format["None_date"]).date())

        for _, _, position, _ in self.positions:
            position.set_active(active=False)

        self._set_edit_mode(active=False)

    def _load_nexus_types(self, type_: str) -> None:
        dummy: list = list()
        member_dummy: list = list()
        match type_:
            case "phone":
                dummy = self.raw_phone_number_ids
                member_dummy = self.phone_numbers
            case "mail":
                dummy = self.raw_mail_ids
                member_dummy = self.mail_addresses
            case "position":
                dummy = self.raw_position_ids
                member_dummy = self.positions

        member_dummy.clear()
        for ID, name_item in dummy:
            member_dummy.append([None, ID, name_item, ""])

    def load_single_member(self) -> None:
        current_member: ListItem = self._members_list.list.currentItem()
        data, valid = transition.get_member_data_by_id(id_=current_member.ID)
        if not valid:
            self.set_error_bar(message=data)
            return

        member_data = data["member_data"]
        self._first_name_le.setText("" if member_data["first_name"] is None else member_data["first_name"])
        self._last_name_le.setText("" if member_data["last_name"] is None else member_data["last_name"])
        self._street_le.setText("" if member_data["street"] is None else member_data["street"])
        self._number_le.setText("" if member_data["number"] is None else member_data["number"])
        self._zip_code_le.setText("" if member_data["zip_code"] is None else member_data["zip_code"])
        self._city_le.setText("" if member_data["city"] is None else member_data["city"])
        self._b_day_date.setDate(QDateTime().fromSecsSinceEpoch(member_data["birth_date"]).date())
        self._entry_date.setDate(QDateTime().fromSecsSinceEpoch(member_data["entry_date"]).date())
        self._membership_type_box.setCurrentText(member_data["membership_type"])
        self._special_member_cb.setChecked(True if member_data["special_member"] else False)
        self._comment_text.setText("" if member_data["comment_text"] is None else member_data["comment_text"])
        self._maps_le.setText("" if member_data["maps"] is None else member_data["maps"])

        self._load_phone_data(data["phone"])
        self._load_mail_data(data["mail"])
        self._load_position_data(data["position"])

        self._set_maps()
        self._set_edit_mode(active=False)

    def _load_phone_data(self, phone_data) -> None:
        current_type = self._phone_number_type_box.currentText()
        if len(phone_data) == 0:
            self._phone_number_le.setText("")
            for entry in self.phone_numbers:
                self.phone_numbers[self.phone_numbers.index(entry)][3] = ""
            return

        for ID, new_type_id, new_phone in phone_data:
            for entry in self.phone_numbers:
                _, old_type_id, old_type, old_phone = entry
                if not old_type_id == new_type_id:
                    continue
                self.phone_numbers[self.phone_numbers.index(entry)][0] = ID
                self.phone_numbers[self.phone_numbers.index(entry)][3] = "" if new_phone is None else new_phone
                if old_type == current_type:
                    self._phone_number_le.setText("" if new_phone is None else new_phone)

    def _load_mail_data(self, mail_data) -> None:
        current_type = self._mail_address_type_box.currentText()
        if len(mail_data) == 0:
            for entry in self.mail_addresses:
                self.mail_addresses[self.mail_addresses.index(entry)][3] = ""
            return

        for ID, new_type_id, new_mail in mail_data:
            for entry in self.mail_addresses:
                _, old_type_id, old_type, old_mail = entry
                if not old_type_id == new_type_id:
                    continue
                self.mail_addresses[self.mail_addresses.index(entry)][0] = ID
                self.mail_addresses[self.mail_addresses.index(entry)][3] = \
                    "" if new_mail is None else new_mail
                if old_type == current_type:
                    self._mail_address_le.setText("" if new_mail is None else new_mail)

    def _load_position_data(self, position_data) -> None:
        if len(position_data) == 0:
            for _, _, item, _ in self.positions:
                item.set_active(active=False)
            return

        for ID, new_type_id, new_active in position_data:
            for item in self.positions:
                _, old_type_id, position, _ = item
                if not old_type_id == new_type_id:
                    continue
                self.positions[self.positions.index(item)][0] = ID
                position.ID = ID
                position.set_active(active=new_active)

    def _save(self) -> None | bool:
        member_data: dict = {
            "first_name": None if self._first_name_le.text().strip() == "" else self._first_name_le.text().strip().title(),
            "last_name": None if self._last_name_le.text().strip() == "" else self._last_name_le.text().strip().title(),
            "street": None if self._street_le.text().strip() == "" else self._street_le.text().strip().title(),
            "number": None if self._number_le.text().strip() == "" else self._number_le.text().strip().title(),
            "zip_code": None if self._zip_code_le.text().strip() == "" else self._zip_code_le.text().strip().title(),
            "birth_date": QDateTime.toSecsSinceEpoch(QDateTime(self._b_day_date.date())),
            "entry_date": QDateTime.toSecsSinceEpoch(QDateTime(self._entry_date.date())),
            "city": None if self._city_le.text().strip().title() == "" else self._city_le.text().strip().title(),
            "membership_type": self._membership_type_box.currentText(),
            "special_member": self._special_member_cb.isChecked(),
            "comment_text": None if self._comment_text.toPlainText().strip() == "" else self._comment_text.toPlainText().strip(),
            "maps": None if self._maps_le.text().strip() == "" else self._maps_le.text().strip(),
        }

        phone_list: list = list()
        for ID, type_id, Type, phone in self.phone_numbers:
            phone_entry: list = [
                ID,
                type_id,
                Type,
                None if phone == "" else phone,
            ]
            phone_list.append(phone_entry)

        mail_list: list = list()
        for ID, type_id, Type, mail in self.mail_addresses:
            mail_entry: list = [
                ID,
                type_id,
                Type,
                None if mail == "" else mail,
            ]
            mail_list.append(mail_entry)

        position_list: list = list()
        for ID, type_id, item, _ in self.positions:
            position_entry: list = [
                ID,
                type_id,
                item.name,
                item.active,
            ]
            position_list.append(position_entry)

        member_nexus_data: dict = {
            "phone": phone_list,
            "mail": mail_list,
            "position": position_list,
        }

        data: dict = {
            "member_data": member_data,
            "member_nexus_data": member_nexus_data,
        }

        result, valid = transition.update_member_data(id_=self._members_list.list.currentItem().ID, data=data,
                                                      log_date=self._get_log_date())
        if not valid:
            self.set_error_bar(message=result)
            return False

        self.set_info_bar(message="saved")
        self._set_save_ids(ids=result)
        return True

    def _get_log_date(self) -> int:
        dlg = DateInput(self)
        if dlg.exec():
            return QDateTime.toSecsSinceEpoch(QDateTime(dlg.get_date()))

    def _set_save_ids(self, ids: dict) -> None:
        current_member: ListItem = self._members_list.list.currentItem()

        new_member_id: int = ids["member_id"]
        new_phone_ids: list = ids["phone"]
        new_mail_ids: list = ids["mail"]
        new_position_ids: list = ids["position"]

        current_member.ID = new_member_id

        for id_ in new_phone_ids:
            if id_ is None:
                continue
            self.phone_numbers[new_phone_ids.index(id_)][0] = id_

        for id_ in new_mail_ids:
            if id_ is None:
                continue
            self.mail_addresses[new_mail_ids.index(id_)][0] = id_

        for id_ in new_position_ids:
            if id_ is None:
                continue
            self.positions[new_position_ids.index(id_)][0] = id_
            self.positions[new_position_ids.index(id_)][2].ID = id_

        self._set_edit_mode(active=False)

    def _recover(self) -> None:
        result, valid = w.window_manger.is_valid_recover_window(type_="member", ignore_member_window=True)
        if not valid:
            self.set_error_bar(message=result)
            return

        w.window_manger.recover_window = r_w.RecoverWindow(type_="member")
        w.window_manger.members_window = None
        self.close()

    def _table(self) -> None:
        result = w.window_manger.is_valid_member_table_window(ignore_member_window=True)
        if isinstance(result, str):
            self.set_info_bar(message=result)
        elif result:
            self.close()
            w.window_manger.member_table_window = m_t_w.MemberTableWindow()

    def _anniversary(self) -> None:
        result = w.window_manger.is_valid_member_anniversary_window(ignore_member_window=True)
        if isinstance(result, str):
            self.set_info_bar(message=result)
        elif result:
            self.close()
            w.window_manger.member_anniversary_window = m_a_w.MemberAnniversaryWindow()

    def _letter(self) -> None:
        pass

    def _member_card(self) -> None:
        current_member: ListItem = self._members_list.list.currentItem()
        transition.create_default_dir("member_card")
        file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                                  f"{c.config.dirs['save']}/{c.config.dirs['organisation']}/{c.config.dirs['export']}/{c.config.dirs['member']}/{c.config.dirs['member_card']}/{current_member.first_name}_{current_member.last_name}.pdf",
                                                  "PDF (*.pdf);;All Files (*)")
        if not check:
            self.set_info_bar("Export abgebrochen")
            return

        transition.get_member_card_pdf(current_member.ID, path=file)

        if self._open_permission():
            transition.open_latest_export()

        self.set_info_bar("export abgeschlossen")

    def _set_inactive(self) -> None:
        current_member: ListItem = self._members_list.list.currentItem()
        result, valid = transition.update_member_activity(ID=current_member.ID, active=False)
        if not valid:
            self.set_error_bar(message=result)
            return
        self._members_list.load_list_data()
        self._set_first_member()
        self.set_info_bar(message="saved")

    def _is_maps(self) -> bool:
        if self._maps_le.text().strip():
            return True
        elif self._street_le.text().strip() or \
                self._zip_code_le.text().strip() or \
                self._city_le.text().strip():
            return True
        else:
            return False

    def _set_maps(self) -> None:
        self._maps_btn.setEnabled(self._is_maps())

    def _open_maps(self) -> None:
        if self._is_maps():
            if self._maps_le.text().strip():
                webbrowser.open(self._maps_le.text().strip())
            else:
                webbrowser.open(
                    f"""http://www.google.de/maps/place/{self._street_le.text().strip()}+{self._number_le.text().strip()}
                    ,+{self._zip_code_le.text().strip()}+{self._city_le.text().strip()}""")

    def closeEvent(self, event) -> None:
        event.ignore()
        if self._is_edit and self.save_permission(window_name="Mitgliederfenster"):
            if self._save():
                w.window_manger.members_window = None
                event.accept()
        else:
            w.window_manger.members_window = None
            event.accept()
