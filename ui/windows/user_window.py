# Purpur Tentakel
# 16.03.2022
# VereinsManager / User Window

from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QWidget, QMessageBox

from ui.windows.base_window import BaseWindow
from ui.windows import window_manager as w_m, recover_window as r_w
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
    POSITION = 8
    PASSWORD_1 = 9
    PASSWORD_2 = 10


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
        self._load_user_names()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Benutzer bearbeiten")

    def _set_ui(self) -> None:
        # Left
        self._user_lb: QLabel = QLabel()
        self._user_lb.setText("Benutzer:")

        self._user_list: QListWidget = QListWidget()
        self._user_list.itemClicked.connect(self._load_user_data)

        self._add_user_btn: QPushButton = QPushButton()
        self._add_user_btn.setText("Benutzer hinzufügen")
        self._add_user_btn.clicked.connect(self._add_user)
        self._remove_user_btn: QPushButton = QPushButton()
        self._remove_user_btn.setText("Benutzer löschen")
        self._remove_user_btn.clicked.connect(self._delete)
        self._recover_user_btn: QPushButton = QPushButton()
        self._recover_user_btn.setText("Benutzer wiederherstellen")
        self._recover_user_btn.clicked.connect(self._recover)

        self._break_btn: QPushButton = QPushButton()
        self._break_btn.setText("Zurücksetzten")
        self._break_btn.setEnabled(False)
        self._break_btn.clicked.connect(self._load_user_data)
        self._save_btn: QPushButton = QPushButton()
        self._save_btn.setText("Speichern")
        self._save_btn.setEnabled(False)
        self._save_btn.clicked.connect(self._save)

        # Right
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._first_name_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.FIRSTNAME))
        self._first_name_le.returnPressed.connect(self._save)
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.LASTNAME))
        self._last_name_le.returnPressed.connect(self._save)

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda: self._set_el_input(LineEditType.STREET))
        self._street_le.returnPressed.connect(self._save)
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_el_input(LineEditType.NUMBER))
        self._number_le.returnPressed.connect(self._save)
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda: self._set_el_input(LineEditType.ZIP_CODE))
        self._zip_code_le.returnPressed.connect(self._save)
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_el_input(LineEditType.CITY))
        self._city_le.returnPressed.connect(self._save)

        self._phone_number_lb: QLabel = QLabel()
        self._phone_number_lb.setText("Telefon:")
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Telefonnummer")
        self._phone_number_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PHONE))
        self._phone_number_le.returnPressed.connect(self._save)
        self._mail_lb: QLabel = QLabel()
        self._mail_lb.setText("Mail:")
        self._mail_le: QLineEdit = QLineEdit()
        self._mail_le.setPlaceholderText("Mail")
        self._mail_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.MAIL))
        self._mail_le.returnPressed.connect(self._save)
        self._position_lb: QLabel = QLabel()
        self._position_lb.setText("Position:")
        self._position_le: QLineEdit = QLineEdit()
        self._position_le.setPlaceholderText("Position")
        self._position_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.POSITION))
        self._position_le.returnPressed.connect(self._save)

        self._password_lb: QLabel = QLabel()
        self._password_lb.setText("Passwort:")
        self._password_1_le: QLineEdit = QLineEdit()
        self._password_1_le.setPlaceholderText("Neues Passwort")
        self._password_1_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PASSWORD_1))
        self._password_1_le.returnPressed.connect(self._save)
        self._password_2_le: QLineEdit = QLineEdit()
        self._password_2_le.setPlaceholderText("Passwort wiederholen")
        self._password_2_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.PASSWORD_2))
        self._password_2_le.returnPressed.connect(self._save)

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

        # Mail / Number / Position / Password
        grid.addWidget(self._mail_lb, row, 0, 1, 1)
        grid.addWidget(self._mail_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._phone_number_lb, row, 0, 1, 1)
        grid.addWidget(self._phone_number_le, row, 1, 1, 1)
        grid.addWidget(self._password_lb, row, 2, 1, 1, alignment=Qt.AlignRight)
        grid.addWidget(self._password_1_le, row, 3, 1, 1)
        row += 1
        grid.addWidget(self._position_lb, row, 0, 1, 1)
        grid.addWidget(self._position_le, row, 1, 1, 1)
        grid.addWidget(self._password_2_le, row, 3, 1, -1)
        row += 1

        grid_vbox: QVBoxLayout = QVBoxLayout()
        grid_vbox.addLayout(grid)
        grid_vbox.addStretch()

        # Global
        sub_global_hbox: QHBoxLayout = QHBoxLayout()
        sub_global_hbox.addWidget(self._user_list)
        sub_global_hbox.addLayout(grid_vbox)

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
            case LineEditType.POSITION:
                current_user.position = self._position_le.text().strip().title()
            case LineEditType.PASSWORD_1:
                current_user.password_1 = self._password_1_le.text().strip()
            case LineEditType.PASSWORD_2:
                current_user.password_2 = self._password_2_le.text().strip()

        self._set_edit_mode(True)

    def _set_current_user(self) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        self._first_name_le.setText(current_user.first_name)
        self._last_name_le.setText(current_user.last_name)
        self._street_le.setText(current_user.street)
        self._number_le.setText(current_user.number)
        self._zip_code_le.setText(current_user.zip_code)
        self._city_le.setText(current_user.city)
        self._phone_number_le.setText(current_user.phone_number)
        self._mail_le.setText(current_user.mail_address)
        self._position_le.setText(current_user.position)
        self._password_1_le.setText("")
        self._password_2_le.setText("")

        self._set_edit_mode(active=False)

    def _add_user(self) -> None:
        new_user = UserListItem()
        self._user_list.addItem(new_user)
        self._user_list.setCurrentItem(new_user)
        self._set_current_user()
        self._set_edit_mode(True)

    def _load_user_names(self) -> None:
        data = transition.get_all_user_name()
        self._user_list.clear()
        if isinstance(data, str):
            self.set_error_bar(message=data)
        elif len(data) == 0:
            self._add_user()
        else:
            for entry in data:
                ID, first_name, last_name = entry
                new_user: UserListItem = UserListItem(id_=ID, first_name=first_name, last_name=last_name)
                self._user_list.addItem(new_user)
            self._user_list.setCurrentRow(0)
            self._load_user_data()

    def _load_user_data(self) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        data = transition.get_user_data_by_id(ID=current_user.user_id_)
        if isinstance(data, str):
            self.set_error_bar(message=data)
        else:
            current_user.street = "" if data["firstname"] is None else data["firstname"]
            current_user.number = "" if data["number"] is None else data["number"]
            current_user.zip_code = "" if data["zip_code"] is None else data["zip_code"]
            current_user.city = "" if data["city"] is None else data["city"]
            current_user.phone_number = "" if data["phone"] is None else data["phone"]
            current_user.mail_address = "" if data["mail"] is None else data["mail"]
            current_user.position = "" if data["position"] is None else data["position"]
            self._set_current_user()

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
            self._password_1_le.clear()
            self._password_2_le.clear()
            self._set_edit_mode(False)
            current_user.password_1 = str()
            current_user.password_2 = str()
            if isinstance(result, int):
                self._set_current_user_id(user_id=result)

    def _recover(self) -> None:
        result = w_m.window_manger.is_valid_recover_window(type_="user", active_user_window=True)
        if isinstance(result, str):
            self.set_error_bar(message=result)
        else:
            w_m.window_manger.recover_window = r_w.RecoverWindow(type_="user")
            w_m.window_manger.user_window = None
            self.close()

    def _delete(self) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        result = transition.update_user_activity(ID=current_user.user_id_, active=False)
        if isinstance(result, str):
            self.set_error_bar(message=result)
        else:
            self._load_user_names()
            self.set_info_bar(message="gelöscht")

    def _set_current_user_id(self, user_id: int) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        current_user.user_id_ = user_id

    def closeEvent(self, event) -> None:
        event.ignore()
        if self._is_edit and self.save_permission():
            self._save()
        w_m.window_manger.user_window = None
        event.accept()
