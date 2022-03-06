# Purpur Tentakel
# 22.02.2022
# VereinsManager / Recover Members Window

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w

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


class RecoverMemberWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

        self._load_member_names()

    def _set_window_information(self) -> None:
        self.setWindowTitle("ehmalige Mitglieder - Vereinsmanager")

    def _set_ui(self) -> None:
        self.member_list: QListWidget = QListWidget()
        self.member_list.itemClicked.connect(self._set_recover_enabled)

        self._recover_member_btn: QPushButton = QPushButton()
        self._recover_member_btn.setText("Mitglied wieder herstellen")
        self._recover_member_btn.clicked.connect(self._recover)

    def _set_layout(self):
        button: QHBoxLayout = QHBoxLayout()
        button.addStretch()
        button.addWidget(self._recover_member_btn)

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
            self._recover_member_btn.setEnabled(True)
        else:
            self._recover_member_btn.setEnabled(False)

    def _load_member_names(self) -> None:
        self.member_list.clear()
        data = transition.get_all_member_name(active=False)
        if isinstance(data, str):
            self.set_error_bar(data)
        for ID, first_name, last_name in data:
            new_member: MemberListItem = MemberListItem(id_=ID, first_name=first_name, last_name=last_name)
            self.member_list.addItem(new_member)
            self.member_list.setCurrentItem(None)
        self._set_recover_enabled()

    def _recover(self) -> None:
        current_member: MemberListItem = self.member_list.currentItem()
        result = transition.update_member_activity(id_=current_member.id_, active=True)
        if isinstance(result, str):
            self.set_error_bar(message=result)
            return
        self._load_member_names()
        self.set_info_bar(message="saved")

    def closeEvent(self, event) -> None:
        event.ignore()
        result = w.window_manger.is_valid_member_window(active_recover_member_window=True)
        if isinstance(result, str):
            w.window_manger.recover_member_window = None
            event.accept()
        else:
            w.window_manger.members_window = m_w.MembersWindow()
            w.window_manger.recover_member_window = None
            event.accept()
