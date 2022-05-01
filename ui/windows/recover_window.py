# Purpur Tentakel
# 22.02.2022
# VereinsManager / Recover Members Window

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from ui import window_manager as w
from ui.windows import user_window
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListFrame, ListItem
from ui.windows.member_windows import members_window

import transition


class RecoverWindow(BaseWindow):
    def __init__(self, type_: str, is_start_window: bool = False) -> None:
        super().__init__()
        self._type: str = type_
        self._is_start_window: bool = is_start_window

        self._set_type()
        self._set_window_information()
        self._create_ui()
        self._create_layout()

        self.set_recover_enabled()

    def _create_ui(self) -> None:
        self.recover_list: ListFrame = ListFrame(self, get_names_method=self._get_names_method,
                                                 list_method=self.null_method, active=False)
        self.recover_list.list.setToolTip("Rote hinterlegte Einträge sollten gelöscht werden.")

        self._recover_btn: QPushButton = QPushButton()
        self._recover_btn.setText(self._recover_btn_name)
        self._recover_btn.clicked.connect(self._recover)

        self._delete_btn: QPushButton = QPushButton()
        self._delete_btn.setText(self._delete_btn_name)
        self._delete_btn.clicked.connect(self._delete)

    def _create_layout(self):
        button: QHBoxLayout = QHBoxLayout()
        button.addStretch()
        button.addWidget(self._delete_btn)
        button.addWidget(self._recover_btn)

        global_: QVBoxLayout = QVBoxLayout()
        global_.addWidget(self.recover_list)
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
                self._delete_btn_name: str = "Mitglied löschen"

                self._update_activity_method = transition.update_member_activity
                self._valid_parent_window_method = w.window_manger.is_valid_member_window
                self._get_names_method = transition.get_all_member_name
                self.delete_method = transition.delete_member

            case "user":
                self._window_name: str = "ehmalige Benutzer - Vereinsmanager"
                self._recover_btn_name: str = "Benutzer wieder herstellen"
                self._delete_btn_name: str = "Benutzer löschen"

                self._update_activity_method = transition.update_user_activity
                self._valid_parent_window_method = w.window_manger.is_valid_user_window
                self._get_names_method = transition.get_all_user_name
                self.delete_method = transition.delete_user

    def set_recover_enabled(self) -> None:
        current_member = self.recover_list.list.currentItem()
        if current_member:
            self._delete_btn.setEnabled(True)
            self._recover_btn.setEnabled(True)
        else:
            self._delete_btn.setEnabled(False)
            self._recover_btn.setEnabled(False)

    def _delete(self) -> None:
        current_member = self.recover_list.list.currentItem()
        message, result = self.delete_method(ID=current_member.ID)

        if not result:
            self.set_error_bar(message=message)
            return

        self.recover_list.load_list_data()
        self.set_recover_enabled()
        self.set_info_bar(message="saved")

    def _recover(self) -> None:
        current_member: ListItem = self.recover_list.list.currentItem()
        result, valid = self._update_activity_method(ID=current_member.ID, active=True)
        if not valid:
            self.set_error_bar(message=result)
            return
        self.recover_list.load_list_data()
        self.set_recover_enabled()
        self.set_info_bar(message="saved")

    def closeEvent(self, event) -> None:
        event.ignore()
        result, valid = self._valid_parent_window_method(True)
        if not valid or self._is_start_window:
            match self._type:
                case "member":
                    w.window_manger.recover_member_window = None
                case "user":
                    w.window_manger.recover_user_window = None
            event.accept()
        else:
            match self._type:
                case "member":
                    w.window_manger.members_window = members_window.MembersWindow()
                    w.window_manger.recover_member_window = None

                case "user":
                    w.window_manger.user_window = user_window.UserWindow()
                    w.window_manger.recover_user_window = None

            event.accept()

    def null_method(self) -> None:
        pass


def create_recover_window(type_: str) -> None:
    match type_:
        case "member":
            w.window_manger.recover_member_window = RecoverWindow(type_=type_, is_start_window=True)
        case "user":
            w.window_manger.recover_user_window = RecoverWindow(type_=type_, is_start_window=True)
