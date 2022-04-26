# Purpur Tentakel
# 21.01.2022
# VereinsManager /Types Window

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QComboBox, QListWidget, QListWidgetItem, QLineEdit

import transition
from ui import window_manager as w
from config import config_sheet as c
from ui.windows.base_window import BaseWindow

debug_str: str = "TypesWindow"


class TypesListEntry(QListWidgetItem):
    def __init__(self, type_: tuple, active: bool) -> None:
        super().__init__()
        self.ID: int = int()
        self.name: str = str()
        self.extra_entry = None
        self.raw_id: int = int()
        self.raw_name: str = str()

        self.active: bool = active

        self._set_attributes(type_=type_)
        self._set_name()

    def _set_attributes(self, type_: tuple) -> None:
        attributes: list = [
            "ID",
            "name",
            "extra_entry",
            "raw_id",
            "raw_name",
        ]
        for index, attribute in enumerate(attributes):
            setattr(self, attribute, type_[index])

    def _set_name(self) -> None:
        self.setText(self.name) if self.active else self.setText(self.name + " (inaktiv)")


class TypesWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()
        self._types_list_items: list = list()
        self._raw_types: tuple = tuple()

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._set_window_information()

        self._set_raw_types()

    def _create_ui(self) -> None:
        self._types_box: QComboBox = QComboBox()
        self._types_box.currentTextChanged.connect(self._set_current_type)

        self._edit_type_le: QLineEdit = QLineEdit()
        self._edit_type_le.textChanged.connect(self._text_chanced)
        self._edit_type_le.returnPressed.connect(self._add_update_type)
        self._edit_type_le.setPlaceholderText("Typ:")

        self._edit_extra_le: QLineEdit = QLineEdit()
        self._edit_extra_le.textChanged.connect(self._text_chanced)
        self._edit_extra_le.returnPressed.connect(self._add_update_type)
        self._edit_extra_le.setPlaceholderText("Zusatzinfo")

        self._types_list: QListWidget = QListWidget()
        self._types_list.currentItemChanged.connect(self._row_chanced)

        self._add_edit_btn: QPushButton = QPushButton()
        self._add_edit_btn.setText("Typ hinzufügen")
        self._add_edit_btn.clicked.connect(self._add_update_type)
        self._activity_btn: QPushButton = QPushButton()
        self._activity_btn.setText("Typ deaktivieren")
        self._activity_btn.clicked.connect(self._set_type_activity)
        self._remove_btn: QPushButton = QPushButton()
        self._remove_btn.setText("Typ löschen")
        self._remove_btn.clicked.connect(self._delete_type)

        self._set_btn()

    def _create_layout(self) -> None:
        grid: QGridLayout = QGridLayout()

        row: int = 0
        grid.addWidget(self._types_box, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._edit_type_le, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._edit_extra_le, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._add_edit_btn, row, 0)
        grid.addWidget(self._activity_btn, row, 1)
        grid.addWidget(self._remove_btn, row, 2)

        row += 1
        grid.addWidget(self._types_list, row, 0, 1, -1)

        widget: QWidget = QWidget()
        widget.setLayout(grid)
        self.set_widget(widget=widget)
        self.show()

    def _add_type(self) -> None:
        if not self._is_input():
            self.set_info_bar(message="Nicht alle Eingaben vorhanden")
            return

        result, valid = transition.add_type(type_name=self._edit_type_le.text().strip().title(),
                                            raw_type_id=self._get_raw_id_from_name(
                                                type_name=self._types_box.currentText()),
                                            extra_value=None if self._edit_extra_le.text().strip() \
                                                                == "" else self._edit_extra_le.text().strip())
        if not valid:
            self.set_error_bar(message=result)
            return

        self.set_info_bar(message="saved")
        self._set_current_type()

    def _get_raw_id_from_name(self, type_name: str) -> int:
        for ID, type_ in self._raw_types:
            if type_ == type_name:
                return ID

    def _set_window_information(self) -> None:
        self.setWindowTitle("Typen - Vereinsmanager")

    def _set_current_type(self) -> None:
        self._edit_type_le.clear()
        self._types_list.clear()
        self._types_list_items.clear()

        bools: list = [
            True,
            False
        ]
        for bool_ in bools:
            data, valid = transition.get_single_type(
                raw_type_id=self._get_raw_id_from_name(self._types_box.currentText()),
                active=bool_)
            if not valid:
                self.set_error_bar(message=data)
                return

            for type_ in data:
                new_type: TypesListEntry = TypesListEntry(type_=type_, active=bool_)
                self._types_list.addItem(new_type)
                self._types_list_items.append(new_type)

        self._set_extra_le()
        self._edit_type_le.setFocus()
        self._types_list.setCurrentItem(None)
        self._edit_type_le.clear()
        self._edit_extra_le.clear()

        self._set_btn()

    def _set_extra_le(self) -> None:
        current_raw_type_id: int = self._get_raw_id_from_name(self._types_box.currentText())
        if current_raw_type_id == c.config.raw_type_id['membership']:
            self._edit_extra_le.setEnabled(True)
            self._edit_extra_le.setPlaceholderText("Beitrag")
            self._edit_extra_le.setValidator(QIntValidator())
        else:
            self._edit_extra_le.setEnabled(False)
            self._edit_extra_le.setPlaceholderText("Keine Eingabe möglich")
            self._edit_extra_le.setValidator(None)

    def _set_raw_types(self) -> None:
        data, valid = transition.get_raw_types()
        if not valid:
            self.set_error_bar(message=data)
            return

        self._raw_types = data
        self._types_box.clear()
        for ID, text in self._raw_types:
            self._types_box.addItem(text)

    def _set_type_activity(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        result, valid = transition.update_type_activity(id_=current_item.ID,
                                                        active=False if current_item.active else True)
        if not valid:
            self.set_error_bar(message=result)
            return

        self.set_info_bar(message="saved")
        self._set_current_type()

    def _set_btn(self) -> None:
        self._is_edit_mode()
        self._add_edit_btn.setEnabled(self._is_input())
        self._activity_btn.setEnabled(self._is_activity())
        self._remove_btn.setEnabled(self._is_remove())

    def _add_update_type(self) -> None:
        self._update_type() if self._is_edit_mode() else self._add_type()

    def _update_type(self) -> None:
        if not self._is_input():
            self.set_info_bar(message="Nicht alle Eingaben vorhanden")
            return
        current_item: TypesListEntry = self._types_list.currentItem()
        text: str = self._edit_type_le.text().strip().title()
        result, valid = transition.update_type(id_=current_item.ID, name=text,
                                               extra_value=None if self._edit_extra_le.text().strip() \
                                                                   == "" else self._edit_extra_le.text().strip())
        if not valid:
            self.set_error_bar(message=result)
            self._set_current_type()
            return

        self.set_info_bar(message="saved")
        self._set_current_type()

    def _delete_type(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        result, valid = transition.delete_type(id_=current_item.ID)
        if not valid:
            self.set_error_bar(message=result)
            return

        self.set_info_bar(message="saved")
        self._set_current_type()

    def _is_edit_mode(self) -> bool:
        if self._types_list.currentItem() is not None:
            self._add_edit_btn.setText("Typ beartbeiten")
            return True
        else:
            self._add_edit_btn.setText("Typ hinzufügen")
            return False

    def _is_input(self) -> bool:
        if len(self._edit_type_le.text().strip()) != 0:
            if self._edit_extra_le.isEnabled() and len(self._edit_extra_le.text().strip()) != 0:
                return True
            if not self._edit_extra_le.isEnabled():
                return True
        return False

    def _is_activity(self) -> bool:
        if self._types_list.currentItem() is not None:
            self._activity_btn.setText(
                "deaktivieren") if self._types_list.currentItem().active else self._activity_btn.setText("aktivieren")
            return True
        else:
            return False

    def _is_remove(self) -> bool:
        return self._types_list.currentItem() is not None

    def _row_chanced(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        if current_item is not None:
            self._edit_type_le.setText(current_item.name)
            self._edit_extra_le.setText(current_item.extra_entry)
            self._set_btn()

    def _text_chanced(self) -> None:
        self._set_btn()

    def closeEvent(self, event) -> None:
        event.ignore()
        w.window_manger.types_window = None
        event.accept()
