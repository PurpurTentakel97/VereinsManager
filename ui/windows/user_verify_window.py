# Purpur Tentakel
# 16.03.2022
# VereinsManager / User Verify Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QListWidgetItem

import transition
from ui.windows.base_window import BaseWindow
from ui.windows import alert_window
import debug

debug_str: str = "UserVerifyWindow"

user_verify_window: "UserVerifyWindow"


class UserListItem(QListWidgetItem):
    def __init__(self, ID: int, first_name: str, last_name: str):
        super().__init__()
        self.ID: int = ID
        self.first_name: str = first_name
        self.last_name: str = last_name

        self.set_name()

    def set_name(self) -> None:
        if self.first_name and self.last_name:
            self.setText(self.first_name + " " + self.last_name)
        elif self.first_name:
            self.setText(self.first_name)
        elif self.last_name:
            self.setText(self.last_name)
        else:
            self.setText("Kein Name vorhanden")


class UserVerifyWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._set_ui()
        self._set_layout()
        self._load_user_names()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Benutzer Identifikation")

    def _set_ui(self) -> None:
        self._password_lb: QLabel = QLabel()
        self._password_lb.setText("Passwort:")

        self._password_le: QLineEdit = QLineEdit()
        self._password_le.setPlaceholderText("Passwort")
        self._password_le.setEchoMode(QLineEdit.Password)
        self._password_le.returnPressed.connect(self._verify)

        self._password_btn: QPushButton = QPushButton()
        self._password_btn.setText("Verifizieren")
        self._password_btn.clicked.connect(self._verify)

        self._user_lb: QLabel = QLabel()
        self._user_lb.setText("Benutzer:")
        self._user_list: QListWidget = QListWidget()
        self._user_list.itemClicked.connect(self._set_focus)

    def _set_layout(self) -> None:
        password_lb_hbox: QHBoxLayout = QHBoxLayout()
        password_lb_hbox.addWidget(self._password_lb)
        password_lb_hbox.addStretch()

        password_hbox: QHBoxLayout = QHBoxLayout()
        password_hbox.addWidget(self._password_le)
        password_hbox.addWidget(self._password_btn)

        user_lb_hbox: QHBoxLayout = QHBoxLayout()
        user_lb_hbox.addWidget(self._user_lb)
        user_lb_hbox.addStretch()

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(password_lb_hbox)
        global_vbox.addLayout(password_hbox)
        global_vbox.addLayout(user_lb_hbox)
        global_vbox.addWidget(self._user_list)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget)
        self.show()

    def _set_focus(self) -> None:
        self._password_le.setFocus()

    def _load_user_names(self) -> None:
        data, valid = transition.get_all_user_name()
        if not valid:
            self.set_error_bar(message=data)
            return

        for entry in data:
            ID, firstname, lastname = entry
            new_item: UserListItem = UserListItem(ID=ID, first_name=firstname, last_name=lastname)
            self._user_list.addItem(new_item)
        self._user_list.setCurrentRow(0)

    def _verify(self) -> None:
        current_user: UserListItem = self._user_list.currentItem()
        result, valid = transition.compare_password(current_user.ID, self._password_le.text().strip())
        if not valid:
            self.set_error_bar(message=result)
            return

        if not result:
            self.set_info_bar(message="Falsches Passwort")
            return

        self.close()


def create_user_verify_window() -> None:
    global user_verify_window
    user_verify_window = UserVerifyWindow()
