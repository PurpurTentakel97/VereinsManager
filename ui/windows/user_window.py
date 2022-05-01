# Purpur Tentakel
# 16.03.2022
# VereinsManager / User Window

from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget

import transition
from ui import window_manager as w
from config import config_sheet as c
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListFrame, ListItem
from ui.windows import recover_window, user_verify_window

debug_str: str = "UserWindow"


class LineEditType(Enum):
    FIRSTNAME = 0
    LASTNAME = 1
    OTHER = 2


class UserWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

        self._is_edit: bool = bool()
        self._set_first_user()
        self._set_edit_mode(active=False)

    def _create_ui(self) -> None:
        # Left
        self._user_lb: QLabel = QLabel()
        self._user_lb.setText("Benutzer:")
        self._user_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_user_name,
                                               list_method=self.get_user_data, active=True)

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
        self._break_btn.clicked.connect(self.get_user_data)
        self._save_btn: QPushButton = QPushButton()
        self._save_btn.setText("Speichern")
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
        self._street_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._street_le.returnPressed.connect(self._save)
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_el_input(LineEditType.OTHER))
        self._number_le.returnPressed.connect(self._save)
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._zip_code_le.textChanged.connect(lambda: self._set_el_input(LineEditType.OTHER))
        self._zip_code_le.returnPressed.connect(self._save)
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_el_input(LineEditType.OTHER))
        self._city_le.returnPressed.connect(self._save)
        self._county_le: QLineEdit = QLineEdit()
        self._county_le.setPlaceholderText("Land")
        self._county_le.textChanged.connect(lambda: self._set_el_input(LineEditType.OTHER))
        self._county_le.returnPressed.connect(self._save)

        self._phone_number_lb: QLabel = QLabel()
        self._phone_number_lb.setText("Telefon:")
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Telefonnummer")
        self._phone_number_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._phone_number_le.returnPressed.connect(self._save)
        self._mail_lb: QLabel = QLabel()
        self._mail_lb.setText("Mail:")
        self._mail_le: QLineEdit = QLineEdit()
        self._mail_le.setPlaceholderText("Mail")
        self._mail_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._mail_le.returnPressed.connect(self._save)
        self._position_lb: QLabel = QLabel()
        self._position_lb.setText("Position:")
        self._position_le: QLineEdit = QLineEdit()
        self._position_le.setPlaceholderText("Position")
        self._position_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._position_le.returnPressed.connect(self._save)

        self._password_lb: QLabel = QLabel()
        self._password_lb.setText("Passwort:")
        self._password_1_le: QLineEdit = QLineEdit()
        self._password_1_le.setPlaceholderText("Neues Passwort")
        self._password_1_le.setEchoMode(QLineEdit.Password)
        self._password_1_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._password_1_le.returnPressed.connect(self._save)
        self._password_2_le: QLineEdit = QLineEdit()
        self._password_2_le.setPlaceholderText("Passwort wiederholen")
        self._password_2_le.setEchoMode(QLineEdit.Password)
        self._password_2_le.textChanged.connect(lambda: self._set_el_input(type_=LineEditType.OTHER))
        self._password_2_le.returnPressed.connect(self._save)

    def _create_layout(self) -> None:
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
        grid.addWidget(self._county_le, row, 3)
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
        grid.addWidget(self._position_le, row, 1, 1, 2)
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

    def _add_user(self) -> None:
        new_user: ListItem = ListItem(ID=None)
        self._user_list.list.addItem(new_user)
        self._user_list.list.setCurrentItem(new_user)
        self._set_user_None()
        self._set_edit_mode(True)

    def get_user_data(self) -> None:
        current_user: ListItem = self._user_list.list.currentItem()
        data, valid = transition.get_user_data_by_id(ID=current_user.ID, active=True)
        if not valid:
            self.set_error_bar(message=data)
            return

        self._first_name_le.setText("" if data['firstname'] is None else data['firstname'])
        self._last_name_le.setText("" if data['lastname'] is None else data['lastname'])
        self._street_le.setText("" if data["street"] is None else data["street"])
        self._number_le.setText("" if data["number"] is None else data["number"])
        self._zip_code_le.setText("" if data["zip_code"] is None else data["zip_code"])
        self._city_le.setText("" if data["city"] is None else data["city"])
        self._county_le.setText("" if data["country"] is None else data["country"])
        self._phone_number_le.setText("" if data["phone"] is None else data["phone"])
        self._mail_le.setText("" if data["mail"] is None else data["mail"])
        self._position_le.setText("" if data["position"] is None else data["position"])

        self._set_edit_mode(active=False)

    def _set_window_information(self) -> None:
        self.setWindowTitle("Benutzer bearbeiten")

    def _set_edit_mode(self, active: bool) -> None:
        self._is_edit = active
        invert_edit = not self._is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._user_list.list.setEnabled(invert_edit)
        self._add_user_btn.setEnabled(invert_edit)
        self._remove_user_btn.setEnabled(invert_edit)
        self._recover_user_btn.setEnabled(invert_edit)

    def _set_el_input(self, type_: LineEditType) -> None:
        current_user: ListItem = self._user_list.list.currentItem()
        match type_:
            case LineEditType.FIRSTNAME:
                current_user.first_name = self._first_name_le.text().strip().title()
                current_user.set_name()
            case LineEditType.LASTNAME:
                current_user.last_name = self._last_name_le.text().strip().title()
                current_user.set_name()
            case LineEditType.OTHER:
                pass  # To trigger EditMode

        self._set_edit_mode(True)

    def _set_user_None(self) -> None:
        self._first_name_le.setText("")
        self._last_name_le.setText("")
        self._street_le.setText("")
        self._number_le.setText("")
        self._zip_code_le.setText("")
        self._city_le.setText("")
        self._county_le.setText("")
        self._phone_number_le.setText("")
        self._mail_le.setText("")
        self._position_le.setText("")
        self._password_1_le.setText("")
        self._password_2_le.setText("")

        self._set_edit_mode(active=False)

    def _set_first_user(self) -> None:
        try:
            index: int = 0
            for item in self._user_list.list_items:
                item: ListItem
                if item.ID == c.config.user['ID']:
                    index = self._user_list.list.indexFromItem(item).row()  # QModelIndex
                    break

            self._user_list.list.setCurrentRow(index)
            self.get_user_data()
        except AttributeError:
            self._add_user()

    def _set_current_user_id(self, user_id: int) -> None:
        current_user: ListItem = self._user_list.list.currentItem()
        current_user.ID = user_id

    def _save(self) -> None | bool:
        current_user: ListItem = self._user_list.list.currentItem()

        data: dict = {
            "ID": current_user.ID,
            "firstname": None if self._first_name_le.text().strip() == "" else self._first_name_le.text().strip().title(),
            "lastname": None if self._last_name_le.text().strip() == "" else self._last_name_le.text().strip().title(),
            "street": None if self._street_le.text().strip() == "" else self._street_le.text().strip().title(),
            "number": None if self._number_le.text().strip() == "" else self._number_le.text().strip().title(),
            "zip_code": None if self._zip_code_le.text().strip() == "" else self._zip_code_le.text().strip().title(),
            "city": None if self._city_le.text().strip() == "" else self._city_le.text().strip().title(),
            "country": None if self._county_le.text().strip() == "" else self._county_le.text().strip().title(),
            "phone": None if self._phone_number_le.text().strip() == "" else self._phone_number_le.text().strip(),
            "mail": None if self._mail_le.text().strip() == "" else self._mail_le.text().strip().lower(),
            "position": None if self._position_le.text().strip() == "" else self._position_le.text().strip().title(),
            "password_1": None if self._password_1_le.text().strip() == "" else self._password_1_le.text().strip(),
            "password_2": None if self._password_2_le.text().strip() == "" else self._password_2_le.text().strip(),
        }

        result, valid = transition.save_update_user(data=data)
        if not valid:
            self.set_error_bar(message=result)
            return

        self.set_info_bar(message="saved")
        self._password_1_le.clear()
        self._password_2_le.clear()
        self._set_edit_mode(False)
        if isinstance(result, int):
            self._set_current_user_id(user_id=result)
        return True

    def _delete(self) -> None:
        current_user: ListItem = self._user_list.list.currentItem()

        if not self.is_save_permission(window_name="Programm"):
            self.set_info_bar(message="User Löschen abgebrochen")
            return

        w.window_manger.close_all_window(close_user_window=False)
        if not w.window_manger.is_valid_delete_user():
            self.set_info_bar(message="User Löschen abgebrochen")
            return

        result, valid = transition.update_user_activity(ID=current_user.ID, active=False)
        if not valid:
            self.set_error_bar(message=result)
            return

        while w.window_manger.is_main_window():
            w.window_manger.close_main_window()
            self.set_error_bar("Programm konnte nicht geschlossen werden.")

        user_verify_window.create()

    def _recover(self) -> None:
        result, valid = w.window_manger.is_valid_recover_window(type_="user", ignore_user_window=True)
        if not valid:
            self.set_error_bar(message=result)
            return

        w.window_manger.recover_user_window = recover_window.RecoverWindow(type_="user")
        w.window_manger.user_window = None
        self.close()

    def closeEvent(self, event) -> None:
        event.ignore()
        if self._is_edit and self.is_save_permission(window_name="Benutzerfenster"):
            if self._save():
                w.window_manger.user_window = None
                event.accept()
        else:
            w.window_manger.user_window = None
            event.accept()
