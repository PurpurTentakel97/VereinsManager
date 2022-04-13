# Purpur Tentakel
# 25.03.2022
# VereinsManager / List Frame

from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QFrame, QVBoxLayout

import transition


class ListItem(QListWidgetItem):
    def __init__(self, ID: int or None, first_name: str or None = None, last_name: str or None = None):
        super().__init__()

        self.ID: int = ID
        self.first_name: str or None = first_name
        self.last_name: str or None = last_name

        self.set_name(type_='set')

    def set_name(self, type_: str = 'set') -> None | str:
        text: str = str()
        if self.first_name or self.last_name:
            if self.first_name:
                text += self.first_name.strip()
            if self.first_name and self.last_name:
                text += " "
            if self.last_name:
                text += self.last_name.strip()
        else:
            text = "Kein Name vorhanden"

        match type_:
            case 'get':
                return text
            case 'set':
                self.setText(text)


class ListFrame(QFrame):
    def __init__(self, window, type_: str, active: bool):
        super().__init__()
        self._type: str = type_
        self._active: bool = active
        self._window = window

        self._set_type()
        self._set_ui()
        self._set_layout()
        self.load_list_data()

    def _set_type(self) -> None:
        match self._type:
            case "member":
                match self._active:
                    case True:
                        self._get_names_method = transition.get_all_member_name
                        self._list_method = self._window.load_single_member
                    case False:
                        self._get_names_method = transition.get_all_member_name
                        self._list_method = self._window.set_recover_enabled
            case "member_log":
                self._get_names_method = transition.get_all_member_name
                self._list_method = self._window.load_single_member

            case "user":
                match self._active:
                    case True:
                        self._get_names_method = transition.get_all_user_name
                        self._list_method = self._window.load_user_data
                    case False:
                        self._get_names_method = transition.get_all_user_name
                        self._list_method = self._window.set_recover_enabled

    def _set_ui(self) -> None:
        self.list: QListWidget = QListWidget()
        self.list.itemClicked.connect(self._list_method)

    def _set_layout(self) -> None:
        list_: QVBoxLayout = QVBoxLayout()
        list_.addWidget(self.list)

        self.setLayout(list_)

    def load_list_data(self) -> None:
        self.list.clear()
        data, valid = self._get_names_method(active=self._active)
        if not valid:
            self._window.set_error_bar(data)
            return
        for ID, first_name, last_name in data:
            new_member: ListItem = ListItem(ID=ID, first_name=first_name, last_name=last_name)
            self.list.addItem(new_member)
            self.list.setCurrentItem(None)
        try:
            self._list_method()
        except AttributeError:
            pass
