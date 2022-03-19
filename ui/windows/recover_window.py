# Purpur Tentakel
# 22.02.2022
# VereinsManager / Recover Members Window

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from ui.windows.base_window import BaseWindow
from ui.windows import members_window as m_w, window_manager as w, user_window as u_w

import transition


class MemberListItem(QListWidgetItem):
    def __init__(self, id_: int, first_name: str, last_name: str):
        super().__init__()
        self.id_: int = id_
        self.first_name: str = first_name
        self.last_name: str = last_name
        self._set_name()

    def _set_name(self) -> None:
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


class RecoverWindow(BaseWindow):
    def __init__(self, type_: str) -> None:
        super().__init__()
        self._type: str = type_

        self._set_type()
        self._set_window_information()
        self._set_ui()
        self._set_layout()

        self._load_member_names()

    def _set_type(self) -> None:
        match self._type:
            case "member":
                self._window_name: str = "ehmalige Mitglieder - Vereinsmanager"
                self._recover_btn_name: str = "Mitglied wieder herstellen"
                self._names_method = transition.get_all_member_name
                self._update_activity_method = transition.update_member_activity
                self._valid_parent_window_method = w.window_manger.is_valid_member_window
            case "user":
                self._window_name: str = "ehmalige Benutzer - Vereinsmanager"
                self._recover_btn_name: str = "Benutzer wieder herstellen"
                self._names_method = transition.get_all_user_name
                self._update_activity_method = transition.update_user_activity
                self._valid_parent_window_method = w.window_manger.is_valid_user_window

    def _set_window_information(self) -> None:
        self.setWindowTitle(self._window_name)

    def _set_ui(self) -> None:
        self.member_list: QListWidget = QListWidget()
        self.member_list.itemClicked.connect(self._set_recover_enabled)

        self._recover_btn: QPushButton = QPushButton()
        self._recover_btn.setText(self._recover_btn_name)
        self._recover_btn.clicked.connect(self._recover)

    def _set_layout(self):
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

    def _set_recover_enabled(self) -> None:
        current_member: MemberListItem = self.member_list.currentItem()
        if current_member:
            self._recover_btn.setEnabled(True)
        else:
            self._recover_btn.setEnabled(False)

    def _load_member_names(self) -> None:
        self.member_list.clear()
        data = self._names_method(active=False)
        if isinstance(data, str):
            self.set_error_bar(data)
        for ID, first_name, last_name in data:
            new_member: MemberListItem = MemberListItem(id_=ID, first_name=first_name, last_name=last_name)
            self.member_list.addItem(new_member)
            self.member_list.setCurrentItem(None)
        self._set_recover_enabled()

    def _recover(self) -> None:
        current_member: MemberListItem = self.member_list.currentItem()
        result = self._update_activity_method(ID=current_member.id_, active=True)
        if isinstance(result, str):
            self.set_error_bar(message=result)
            return
        self._load_member_names()
        self.set_info_bar(message="saved")

    def closeEvent(self, event) -> None:
        event.ignore()
        result = self._valid_parent_window_method(active_recover_window=True)
        if isinstance(result, str):
            w.window_manger.recover_window = None
            event.accept()
        else:
            match self._type:
                case "member":
                    w.window_manger.members_window = m_w.MembersWindow()
                case "user":
                    w.window_manger.user_window = u_w.UserWindow()
            w.window_manger.recover_window = None
            event.accept()

