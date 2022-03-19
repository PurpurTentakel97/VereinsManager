# Purpur Tentakel
# 16.03.2022
# VereinsManager / User Window

from enum import Enum
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QWidget

from ui.windows.base_window import BaseWindow
import transition
import debug

debug_str: str = "UserWindow"


class LineEditType(Enum):
    FIRSTNAME = 0
    LASTNAME = 1
    STREET = 2
    NUMBER = 3
    ZIP_CODE = 4
    CITY = 5
    PHONE = 6
    MAIL = 7
    PASSWORD_1 = 8
    PASSWORD_2 = 9


class UserListItem(QListWidgetItem):
    def __init__(self, id_: int | None = None, first_name: str = str(), last_name: str = str()):
        super().__init__()
        self.user_id_: int = id_
        self.first_name: str = first_name
        self.last_name: str = last_name

        self.street: str = str()
        self.number: str = str()
        self.zip_code: str = str()
        self.city: str = str()

        self.phone_number: str = str()
        self.mail_address: str = str()

        self.position: str = str()

        self.password_1: str = str()
        self.password_2: str = str()

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


class UserWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

        self._is_edit: bool = bool()
        self._set_edit_mode(active=False)
        self._add_user()
        # self._load_all_user_names()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Benutzer bearbeiten")

    def _set_ui(self) -> None:
        # Left
        self._user_lb: QLabel = QLabel()
        self._user_lb.setText("Benutzer:")

        self._user_list: QListWidget = QListWidget()
        # self._user_list.itemClicked.connect()

        self._add_user_btn: QPushButton = QPushButton()
        self._add_user_btn.setText("Benutzer hinzufügen")
        self._add_user_btn.clicked.connect(self._add_user)
        self._remove_user_btn: QPushButton = QPushButton()
        self._remove_user_btn.setText("Benutzer löschen")
        # self._remove_user_btn.clicked.connect()
        self._recover_user_btn: QPushButton = QPushButton()
        self._recover_user_btn.setText("Benutzer wiederherstellen")
        # self._recover_user_btn.clicked.connect()

        self._break_btn: QPushButton = QPushButton()
        self._break_btn.setText("Zurücksetzten")
        self._break_btn.setEnabled(False)
        # self._break_btn.clicked.connect()
        self._save_btn: QPushButton = QPushButton()
        self._save_btn.setText("Speichern")
        self._save_btn.setEnabled(False)
        self._save_btn.clicked.connect(self._save)

        # Rhight
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._first_name_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.FIRSTNAME))
        # self._first_name_le.returnPressed.connect(self._save)
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.LASTNAME))
        # self._last_name_le.returnPressed.connect(self._save)

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda: self._set_el_input(LineEditType.STREET))
        # self._street_le.returnPressed.connect(self._save)
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_el_input(LineEditType.NUMBER))
        # self._number_le.returnPressed.connect(self._save)
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda: self._set_el_input(LineEditType.ZIP_CODE))
        # self._zip_code_le.returnPressed.connect(self._save)
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_el_input(LineEditType.CITY))
        # self._city_le.returnPressed.connect(self._save)

        self._phone_number_lb: QLabel = QLabel()
        self._phone_number_lb.setText("Telefon:")
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Telefonnummer")
        self._phone_number_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PHONE))
        # self._phone_number_le.returnPressed.connect(self._save)
        self._mail_lb: QLabel = QLabel()
        self._mail_lb.setText("Mail:")
        self._mail_le: QLineEdit = QLineEdit()
        self._mail_le.setPlaceholderText("Mail")
        self._mail_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.MAIL))
        # self._mail_le.returnPressed.connect(self._save)

        self._password_1_lb: QLabel = QLabel()
        self._password_1_lb.setText("Neues Passwort")
        self._password_1_le: QLineEdit = QLineEdit()
        self._password_1_le.setPlaceholderText("Neues Passwort")
        self._password_1_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PASSWORD_1))
        # self._password_1_le.returnPressed.connect(self._save)
        self._password_2_lb: QLabel = QLabel()
        self._password_2_lb.setText("Neues Passwort")
        self._password_2_le: QLineEdit = QLineEdit()
        self._password_2_le.setPlaceholderText("Neues Passwort")
        self._password_2_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PASSWORD_2))
        # self._password_2_le.returnPressed.connect(self._save)

    def _set_layout(self) -> None:
        # Top
        top_hbox: QHBoxLayout = QHBoxLayout()
        top_hbox.addWidget(self._user_lb)
        top_hbox.addStretch()

        # Bottom
        bottom_hbox: QHBoxLayout = QHBoxLayout()
        bottom_hbox.addWidget(self._add_user_btn)
        bottom_hbox.addWidget(self._remove_user_btn)
        bottom_hbox.addWidget(self._recover_user_btn)
        bottom_hbox.addStretch()
        bottom_hbox.addWidget(self._break_btn)
        bottom_hbox.addWidget(self._save_btn)

        # Right
        row: int = 0
        grid: QGridLayout = QGridLayout()
        # name
        grid.addWidget(self._first_name_lb, row, 0, 1, 1)
        grid.addWidget(self._first_name_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._last_name_lb, row, 0, 1, 1)
        grid.addWidget(self._last_name_le, row, 1, 1, -1)
        row += 1

        # Address
        grid.addWidget(self._address_lb, row, 0, 1, 1)
        grid.addWidget(self._street_le, row, 1, 1, 2)
        grid.addWidget(self._number_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._zip_code_le, row, 1)
        grid.addWidget(self._city_le, row, 2)
        row += 1

        # Mail / Number
        grid.addWidget(self._phone_number_lb, row, 0, 1, 1)
        grid.addWidget(self._phone_number_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._mail_lb, row, 0, 1, 1)
        grid.addWidget(self._mail_le, row, 1, 1, -1)
        row += 1

        # Password
        grid.addWidget(self._password_1_lb, row, 0, 1, 1)
        grid.addWidget(self._password_1_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._password_2_lb, row, 0, 1, 1)
        grid.addWidget(self._password_2_le, row, 1, 1, -1)
        row += 1

        # Global
        sub_global_hbox: QHBoxLayout = QHBoxLayout()
        sub_global_hbox.addWidget(self._user_list)
        sub_global_hbox.addLayout(grid)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(top_hbox)
        global_vbox.addLayout(sub_global_hbox)
        global_vbox.addLayout(bottom_hbox)

        #  set Layout
        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget)
        self.show()

    def _set_edit_mode(self, active: bool) -> None:
        self._is_edit = active
        invert_edit = not self._is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._user_list.setEnabled(invert_edit)
        self._add_user_btn.setEnabled(invert_edit)
        self._remove_user_btn.setEnabled(invert_edit)
        self._recover_user_btn.setEnabled(invert_edit)

    def _set_el_input(self, type_: LineEditType) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        match type_:
            case LineEditType.FIRSTNAME:
                current_user.first_name = self._first_name_le.text().strip().title()
                current_user.set_name()
            case LineEditType.LASTNAME:
                current_user.last_name = self._last_name_le.text().strip().title()
                current_user.set_name()
            case LineEditType.STREET:
                current_user.street = self._street_le.text().strip().title()
            case LineEditType.NUMBER:
                current_user.number = self._number_le.text().strip()
            case LineEditType.ZIP_CODE:
                current_user.zip_code = self._zip_code_le.text().strip()
            case LineEditType.CITY:
                current_user.city = self._city_le.text().strip().title()
            case LineEditType.PHONE:
                current_user.phone_number = self._phone_number_le.text().strip()
            case LineEditType.MAIL:
                current_user.mail_address = self._mail_le.text().strip().lower()
            case LineEditType.PASSWORD_1:
                current_user.password_1 = self._password_1_le.text().strip()
            case LineEditType.PASSWORD_2:
                current_user.password_2 = self._password_2_le.text().strip()

        self._set_edit_mode(True)

    def _add_user(self) -> None:
        new_user = UserListItem()
        self._user_list.addItem(new_user)
        self._user_list.setCurrentItem(new_user)
        self._set_edit_mode(True)

    def _save(self) -> None:
        current_user: UserListItem = self._user_list.currentItem()

        data: dict = {
            "ID": current_user.user_id_,
            "firstname": None if current_user.first_name == "" else current_user.first_name,
            "lastname": None if current_user.last_name == "" else current_user.last_name,
            "street": None if current_user.street == "" else current_user.street,
            "number": None if current_user.number == "" else current_user.number,
            "zip_code": None if current_user.zip_code == "" else current_user.zip_code,
            "city": None if current_user.city == "" else current_user.city,
            "phone": None if current_user.phone_number == "" else current_user.phone_number,
            "mail": None if current_user.mail_address == "" else current_user.mail_address,
            "position": None if current_user.position == "" else current_user.position,
            "password_1": None if current_user.password_1 == "" else current_user.password_1,
            "password_2": None if current_user.password_2 == "" else current_user.password_2,
        }

        result = transition.save_update_user(data=data)
        if isinstance(result, str):
            self.set_error_bar(message=result)
        else:
            self.set_info_bar(message="saved")
            self._set_edit_mode(False)
            self._password_1_le.clear()
            self._password_2_le.clear()
            current_user.password_1 = str()
            current_user.password_2 = str()
            if isinstance(result, int):
                self._set_current_user_id(user_id=result)
                debug.debug(item=debug_str, keyword="_save", message=f" ID = {result} // {current_user.user_id_}")

    def _set_current_user_id(self, user_id: int) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        current_user.user_id_ = user_id
