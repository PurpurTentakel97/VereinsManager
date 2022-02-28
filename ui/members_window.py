# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from PyQt5.QtCore import QDate, Qt, QDateTime
from PyQt5.QtGui import QIntValidator, QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit, QMessageBox
from enum import Enum

import transition
from ui.base_window import BaseWindow
from ui import window_manager as w, recover_member_window as r_m_w
from config import config_sheet as c

import debug


class LineEditType(Enum):
    FIRSTNAME = 0
    LASTNAME = 1
    STREET = 2
    NUMBER = 3
    ZIP_CODE = 4
    CITY = 5
    COMMENT = 6


class DateType(Enum):
    ENTRY = 0
    B_DAY = 1


class MemberListItem(QListWidgetItem):
    def __init__(self, id_: int | None = None, first_name: str | None = None, last_name: str | None = None):
        super().__init__()
        self.member_id_: int = id_
        self.first_name: str = first_name
        self.last_name: str = last_name

        self.street: str | None = None
        self.number: str | None = None
        self.zip_code: str = ""
        self.city: str | None = None

        self.birth_date: QDate = QDate()
        self.entry_date: QDate = QDate()

        self.phone_numbers: list[list[int, int, str, str]] = list()  # [ID, raw_id, Type, number]
        self.mail_addresses: list[list[int, int, str, str]] = list()  # [ID, raw_id, Type, mail]

        self.membership_type: str | None = None
        self.special_member: bool = False
        self.positions: list[[int, int, PositionListItem, None]] = list()

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
            self.setBackground(QColor("Grey"))
        else:
            self.setBackground(QColor("White"))


# noinspection PyArgumentList
class MembersWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.member_counter: int = int()

        self.membership_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.phone_number_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.mail_ids: list[tuple[int, str]] = list()  # [ID, Name]
        self.position_ids: list[tuple[int, PositionListItem]] = list()  # [ID, Name]

        self._set_ui()
        self._set_layout()
        self._set_types()

        self._is_edit: bool = False
        self._set_edit_mode()
        self._load_all_member_names()

    def __str__(self) -> str:
        return "MEMBERS WINDOW"

    def _set_ui(self) -> None:
        # Left
        self._members_lb: QLabel = QLabel()
        self._members_lb.setText("Mitglieder:")

        self._members_list: QListWidget = QListWidget()
        self._members_list.itemClicked.connect(self._load_single_member)

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
        data = transition.get_active_member_type()
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        else:
            for ID, name, type_id, type_name in data:
                match type_id:
                    case 1:  # member_type
                        self.membership_ids.append((ID, name))
                        self._membership_type_box.addItem(name)

                    case 2:  # mail
                        self.mail_ids.append((ID, name))
                        self._mail_address_type_box.addItem(name)

                    case 3:  # phone
                        self.phone_number_ids.append((ID, name))
                        self._phone_number_type_box.addItem(name)

                    case 4:  # position
                        new_position: PositionListItem = PositionListItem(name=name, raw_id=ID)
                        self.position_ids.append((ID, new_position))
                        self._positions_list.addItem(new_position)

            if len(self.phone_number_ids) == 0:
                self._phone_number_le.setEnabled(False)
            if len(self.mail_ids) == 0:
                self._mail_address_le.setEnabled(False)
            if len(self.membership_ids) == 0:
                self._special_member_cb.setEnabled(False)

    def _set_edit_mode(self) -> None:
        invert_edit = not self._is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._members_list.setEnabled(invert_edit)
        self._add_member_btn.setEnabled(invert_edit)
        self._remove_member_btn.setEnabled(invert_edit)

    def _set_current_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()

        self._first_name_le.setText(current_member.first_name)
        self._last_name_le.setText(current_member.last_name)
        self._street_le.setText(current_member.street)
        self._number_le.setText(current_member.number)
        self._zip_code_le.setText(current_member.zip_code)
        self._city_le.setText(current_member.city)
        self._comment_text.setText(current_member.comment_text)

        self._b_day_date.setDate(current_member.birth_date)
        self._entry_date.setDate(current_member.entry_date)

        self._membership_type_box.setCurrentText(current_member.membership_type)

        self._special_member_cb.setChecked(current_member.special_member)

        self._is_edit = False
        self._set_edit_mode()

    def _set_el_input(self, type_: LineEditType) -> None:
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

        if not self._is_edit:
            self._is_edit = True
            self._set_edit_mode()

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
        pass

    def _set_phone_number_input(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if current_member is not None:
            for item in current_member.phone_numbers:
                _, _, Type, phone = item
                if Type == self._phone_number_type_box.currentText():
                    current_member.phone_numbers[current_member.phone_numbers.index(item)][3] = \
                        self._phone_number_le.text().strip()
                    print(current_member.phone_numbers)
                    break

    def _set_mail_type(self) -> None:
        pass

    def _set_mail_input(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if current_member is not None:
            for item in current_member.mail_addresses:
                _, _, Type, mail = item
                if Type == self._mail_address_type_box.currentText():
                    current_member.mail_addresses[current_member.mail_addresses.index(item)][3] = \
                        self._mail_address_le.text().strip()
                    print(current_member.mail_addresses)
                    break

    def _set_membership_type(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        if current_member:
            current_member.membership_type = self._membership_type_box.currentText()

            if not self._is_edit:
                self._is_edit = True
                self._set_edit_mode()

    def _set_special_member(self) -> None:
        self._members_list.currentItem().special_member = self._special_member_cb.isChecked()

    def _set_position(self) -> None:
        current_position: PositionListItem = self._positions_list.currentItem()
        current_member: MemberListItem = self._members_list.currentItem()
        for _, _, item, _ in current_member.positions:
            if current_position.name == item.name:
                if item.active:
                    item.set_active(active=False)
                else:
                    item.set_active(active=True)
                break
        self._positions_list.setCurrentItem(None)

    def _add_member(self) -> None:
        new_member: MemberListItem = MemberListItem()
        new_member.membership_type = self._membership_type_box.currentText()
        new_member.birth_date = QDateTime().fromSecsSinceEpoch(c.config.date_format["None_date"]).date()
        new_member.entry_date = QDateTime().fromSecsSinceEpoch(c.config.date_format["None_date"]).date()
        new_member.membership_type = self._membership_type_box.currentText()
        self._members_list.addItem(new_member)
        self._members_list.setCurrentItem(new_member)
        self._set_current_member()
        self._is_edit = True
        self._set_edit_mode()
        self.member_counter += 1

    def _load_all_member_names(self) -> None:
        data = transition.get_all_member_name()
        self._members_list.clear()
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        elif len(data) == 0:
            self._add_member()
        else:
            self._members_list.setCurrentItem(None)
            for ID, first_name, last_name in data:
                new_member: MemberListItem = MemberListItem(id_=ID, first_name=first_name, last_name=last_name)
                self._load_nexus_types(member=new_member, type_="phone")
                self._load_nexus_types(member=new_member, type_="mail")
                self._load_nexus_types(member=new_member, type_="position")
                self._members_list.addItem(new_member)
                self.member_counter += 1
            self._members_list.setCurrentRow(0)
            self._load_single_member()

    def _load_nexus_types(self, member: MemberListItem, type_: str) -> None:
        dummy: list = list()
        member_dummy: list = list()
        match type_:
            case "phone":
                dummy = self.phone_number_ids
                member_dummy = member.phone_numbers
            case "mail":
                dummy = self.mail_ids
                member_dummy = member.mail_addresses
            case "position":
                dummy = self.position_ids
                member_dummy = member.positions

        member_dummy.clear()
        for ID, name_item in dummy:
            member_dummy.append([None, ID, name_item, ""])

    def _load_single_member(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()

        # member
        data = transition.get_member_data_by_id(id_=current_member.member_id_)
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        else:
            member_data = data["member_data"]
            current_member.first_name = "" if member_data["first_name"] is None else member_data["first_name"]
            current_member.last_name = "" if member_data["last_name"] is None else member_data["last_name"]
            current_member.street = "" if member_data["street"] is None else member_data["street"]
            current_member.number = "" if member_data["number"] is None else member_data["number"]
            current_member.zip_code = "" if member_data["zip_code"] is None else str(member_data["zip_code"])
            current_member.city = "" if member_data["city"] is None else member_data["city"]
            current_member.birth_date = QDateTime().fromSecsSinceEpoch(member_data["birth_date"]).date()
            current_member.entry_date = QDateTime().fromSecsSinceEpoch(member_data["entry_date"]).date()
            current_member.membership_type = member_data["membership_type"]
            current_member.special_member = True if member_data["special_member"] else False
            current_member.comment_text = "" if member_data["comment_text"] is None else member_data["comment_text"]

        # member nexus
        data = transition.get_member_nexus_by_id(id_=current_member.member_id_, type_="phone")
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        else:
            debug.info(item=self, keyword="Phonenumbers", message=data)

        data = transition.get_member_nexus_by_id(id_=current_member.member_id_, type_="mail")
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        else:
            for ID_n, type_id_n, number_n in data:
                for ID, type_id, _, number in current_member.phone_numbers:
                    if type_id_n == type_id:
                        ID, number = ID_n, number_n
            debug.info(item=self, keyword="Mails", message=data)

        data = transition.get_member_nexus_by_id(id_=current_member.member_id_, type_="position")
        if isinstance(data, str):
            self.set_status_bar(massage=data)
        else:
            debug.info(item=self, keyword="Positions", message=data)

        self._set_current_member()

    def _save(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        member_data: dict = {
            "first_name": None if current_member.first_name == "" else current_member.first_name,
            "last_name": None if current_member.last_name == "" else current_member.last_name,
            "street": None if current_member.street == "" else current_member.street,
            "number": None if current_member.number == "" else current_member.number,
            "zip_code": None if current_member.zip_code == "" else int(current_member.zip_code),
            "birth_date": QDateTime.toSecsSinceEpoch(QDateTime(current_member.birth_date)),
            "entry_date": QDateTime.toSecsSinceEpoch(QDateTime(current_member.entry_date)),
            "city": None if current_member.city == "" else current_member.city,
            "membership_type": None if current_member.membership_type == "" else current_member.membership_type,
            "special_member": current_member.special_member,
            "comment_text": None if current_member.comment_text == "" else current_member.comment_text,
        }

        data: dict = {
            "member_data": member_data,
        }

        result = transition.update_member_data(id_=current_member.member_id_, data=data)
        if isinstance(result, str):
            self.set_status_bar(massage=result)
        else:
            current_member.member_id_ = result
            self._is_edit = False
            self._set_edit_mode()

    def _recover(self) -> None:
        result = w.window_manger.is_valid_recover_member_window(member_window=True)
        if isinstance(result, str):
            self.set_status_bar(massage=result)
        else:
            w.window_manger.recover_member_window = r_m_w.RecoverMemberWindow()
            if self._is_edit:
                if self._save_permission():
                    self._save()
            w.window_manger.members_window = None
            self.close()

    @staticmethod
    def _save_permission() -> bool:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Fenster wird geschlossen.")
        msg.setInformativeText("Du hast ungespeicherte Daten. Möchtest du diese Daten vorher speichern?")
        msg.setWindowTitle("Daten Speichern?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    def _set_inactive(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        result = transition.update_member_activity(id_=current_member.member_id_, active=False)
        if isinstance(result, str):
            self.set_status_bar(massage=result)
            return
        self._load_all_member_names()

    def closeEvent(self, event) -> None:
        event.ignore()
        if self._is_edit:
            if self._save_permission():
                self._save()
        w.window_manger.members_window = None
        event.accept()
