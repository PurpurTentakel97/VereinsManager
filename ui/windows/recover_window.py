# Purpur Tentakel
# 22.02.2022
# VereinsManager / Recover Members Window

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from ui.frames.list_frame import ListFrame, ListItem
from ui.windows.base_window import BaseWindow
from ui.windows.member_windows import members_window
from ui.windows import window_manager as w, user_window

import transition


class RecoverWindow(BaseWindow):
    def __init__(self, type_: str) -> None:
        super().__init__()
        self._type: str = type_

        self._set_type()
        self._set_window_information()
        self._create_ui()
        self._create_layout()

        self.set_recover_enabled()

    def _create_ui(self) -> None:
        self.member_list: ListFrame = ListFrame(self, get_names_method=self._get_names_method,
                                                list_method=self._recover, active=False)

        self._recover_btn: QPushButton = QPushButton()
        self._recover_btn.setText(self._recover_btn_name)
        self._recover_btn.clicked.connect(self._recover)

    def _create_layout(self):
        button: QHBoxLayout = QHBoxLayout()
        button.addStretch()
        button.addWidget(self._recover_btn)

        global_: QVBoxLayout = QVBoxLayout()
        global_.addWidget(self.member_list)
        global_.addLayout(button)

        widget: QWidget = QWidget()
        widget.setLayout(global_)
        self.set_widget(widget=widget)
        self.show()

    def _set_window_information(self) -> None:
        self.setWindowTitle(self._window_name)

    def _set_type(self) -> None:
        match self._type:
            case "member":
                self._window_name: str = "ehmalige Mitglieder - Vereinsmanager"
                self._recover_btn_name: str = "Mitglied wieder herstellen"
                self._update_activity_method = transition.update_member_activity
                self._valid_parent_window_method = w.window_manger.is_valid_member_window
                self._get_names_method = transition.get_all_member_name
            case "user":
                self._window_name: str = "ehmalige Benutzer - Vereinsmanager"
                self._recover_btn_name: str = "Benutzer wieder herstellen"
                self._update_activity_method = transition.update_user_activity
                self._valid_parent_window_method = w.window_manger.is_valid_user_window
                self._get_names_method = transition.get_all_user_name

    def set_recover_enabled(self) -> None:
        current_member = self.member_list.list.currentItem()
        if current_member:
            self._recover_btn.setEnabled(True)
        else:
            self._recover_btn.setEnabled(False)

    def _recover(self) -> None:
        current_member: ListItem = self.member_list.list.currentItem()
        result, valid = self._update_activity_method(ID=current_member.ID, active=True)
        if not valid:
            self.set_error_bar(message=result)
            return
        self.member_list.load_list_data()
        self.set_info_bar(message="saved")

    def closeEvent(self, event) -> None:
        event.ignore()
        result, valid = self._valid_parent_window_method(ignore_recover_window=True)
        if not valid:
            w.window_manger.recover_window = None
            event.accept()
        else:
            match self._type:
                case "member":
                    w.window_manger.members_window = members_window.MembersWindow()
                case "user":
                    w.window_manger.user_window = user_window.UserWindow()
            w.window_manger.recover_window = None
            event.accept()
