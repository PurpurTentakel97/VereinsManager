# Purpur Tentakel
# 16.03.2022
# VereinsManager / User Verify Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

import transition
from ui.frames.list_frame import ListItem, ListFrame
from ui.windows.base_window import BaseWindow
import debug

debug_str: str = "UserVerifyWindow"

user_verify_window: "UserVerifyWindow"


class UserVerifyWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
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
        self._user_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_user_name,
                                               list_method=self._set_focus, active=True)

    def _create_layout(self) -> None:
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

    def _set_window_information(self) -> None:
        self.setWindowTitle("Benutzer Identifikation")

    def _set_focus(self) -> None:
        self._password_le.setFocus()

    def _verify(self) -> None:
        current_user: ListItem = self._user_list.list.currentItem()
        result, valid = transition.compare_password(current_user.ID, self._password_le.text().strip())

        if not valid:
            self.set_error_bar(message=result)
            return

        if not result:
            self.set_info_bar(message="Falsches Passwort")
            return

        self.close()


def create() -> None:
    global user_verify_window
    user_verify_window = UserVerifyWindow()
