# Purpur Tentakel
# 21.01.2022
# VereinsManager /Types Window

from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QComboBox, QListWidget, QListWidgetItem, QLineEdit

import debug
from ui.base_window import BaseWindow
from config.error_code import ErrorCode
import transition

types_window_: "TypesWindow" or None = None


class TypesListEntry(QListWidgetItem):
    def __init__(self, type_: tuple, active: bool = True) -> None:
        super().__init__()
        self.id_: int = int()
        self.name: str = str()
        self.raw_id: int = int()
        self.raw_name: str = str()
        self.id_, self.name, self.raw_id, self.raw_name = type_

        self.active: bool = active

        self._set_name()

    def _set_name(self) -> None:
        self.setText(self.name) if self.active else self.setText(self.name + " (inactive)")


class TypesWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()
        self._types_list_items: list = list()
        self._raw_types: tuple = tuple()

        self._create_ui()
        self._create_layout()
        self._set_window_information()

        self._set_types()

    def __str__(self) -> str:
        return "TypesWindow(BaseWindow)"

    def _create_ui(self) -> None:
        self._types_box: QComboBox = QComboBox()
        self._types_box.currentTextChanged.connect(self._set_current_type)

        self._edit: QLineEdit = QLineEdit()
        self._edit.textChanged.connect(self._text_chanced)
        self._edit.returnPressed.connect(self._add_edit_type)
        self._edit.setPlaceholderText("Typ:")

        self._types_list: QListWidget = QListWidget()
        self._types_list.currentItemChanged.connect(self._row_chanced)

        self._add_edit_btn: QPushButton = QPushButton()
        self._add_edit_btn.setText("Typ hinzufügen")
        self._add_edit_btn.clicked.connect(self._add_edit_type)
        self._activity_btn: QPushButton = QPushButton()
        self._activity_btn.setText("Typ deaktivieren")
        self._activity_btn.clicked.connect(self._set_type_activity)
        self._remove_btn: QPushButton = QPushButton()
        self._remove_btn.setText("Typ löschen")
        self._remove_btn.clicked.connect(self._remove_type)

        self._set_btn()

    def _create_layout(self) -> None:
        grid: QGridLayout = QGridLayout()

        row: int = 0
        grid.addWidget(self._types_box, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._edit, row, 0, 1, -1)

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

    def _set_window_information(self) -> None:
        self.setWindowTitle("Typen bearbeiten")

    def _set_current_type(self) -> None:
        self._edit.clear()
        self._types_list.clear()
        self._types_list_items.clear()
        error_code, types = transition.get_single_type(
            raw_type_id=self._get_raw_id_from_name(self._types_box.currentText()))
        if error_code == ErrorCode.LOAD_S:
            for type_ in types:
                new_type: TypesListEntry = TypesListEntry(type_=type_)
                self._types_list.addItem(new_type)
                self._types_list_items.append(new_type)
        else:
            self.handle_error_code(error_code=error_code, type_="Typen")

        error_code, types = transition.get_single_type(
            raw_type_id=self._get_raw_id_from_name(self._types_box.currentText()),
            active=False)
        if error_code == ErrorCode.LOAD_S:
            for type_ in types:
                new_type: TypesListEntry = TypesListEntry(type_=type_, active=False)
                self._types_list.addItem(new_type)
                self._types_list_items.append(new_type)
            self._edit.setFocus()
            self._types_list.setCurrentItem(None)
            self._edit.clear()

            self._set_btn()

        else:
            self.handle_error_code(error_code=error_code, type_="Typen")

    def _set_types(self) -> None:
        error_code, self._raw_types = transition.get_raw_types()
        if error_code == ErrorCode.LOAD_S:
            self._types_box.clear()
            for ID, text in self._raw_types:
                self._types_box.addItem(text)
        else:
            self.handle_error_code(error_code=error_code, type_="Grund Typen")

    def _row_chanced(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        if current_item is not None:
            self._edit.setText(current_item.name)
            self._set_btn()

    def _text_chanced(self) -> None:
        self._set_btn()

    def _set_btn(self) -> None:
        self._is_edit_mode()
        self._add_edit_btn.setEnabled(self._is_input())
        self._activity_btn.setEnabled(self._is_activity())
        self._remove_btn.setEnabled(self._is_remove())

    def _is_edit_mode(self) -> bool:
        if self._types_list.currentItem() is not None:
            self._add_edit_btn.setText("Typ beartbeiten")
            return True
        else:
            self._add_edit_btn.setText("Typ hinzufügen")
            return False

    def _is_input(self) -> bool:
        return False if len(self._edit.text().strip()) == 0 else True

    def _is_activity(self) -> bool:
        if self._types_list.currentItem() is not None:
            self._activity_btn.setText(
                "deaktivieren") if self._types_list.currentItem().active else self._activity_btn.setText("aktivieren")
            return True
        else:
            return False

    def _is_remove(self) -> bool:
        return self._types_list.currentItem() is not None

    def _add_edit_type(self) -> None:
        self._edit_type() if self._is_edit_mode() else self._add_type()

    def _get_raw_id_from_name(self, type_name: str) -> int:
        for ID, type_ in self._raw_types:
            if type_ == type_name:
                return ID

    def _add_type(self) -> None:
        error_code: ErrorCode = transition.add_type(type_name=self._edit.text().strip().title(),
                                                    raw_type_id=self._get_raw_id_from_name(
                                                        type_name=self._types_box.currentText()))
        if error_code == ErrorCode.ADD_S:
            self._set_current_type()
        else:
            debug.error(item=self, keyword="_add_type", message="Typ anlegen fehlgeschlagen")
            self.handle_error_code(error_code=error_code, type_="Typ")

    def _edit_type(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        text: str = self._edit.text().strip().title()
        error_code: ErrorCode = transition.update_type(id_=current_item.id_, name=text)
        if error_code == ErrorCode.UPDATE_S:
            self._set_current_type()
        elif error_code == ErrorCode.NO_CHANCE:
            self._set_current_type()
            self.set_status_bar("Keine Änderungen vorgenommen.")
        else:
            debug.error(item=self, keyword="_edit_type", message="Typ editieren fehlgeschlagen")
            self.handle_error_code(error_code=error_code, type_=f"Typ {text}")

    def _is_correct_input(self) -> bool:
        if len(self._edit.text().strip()) > 0:
            double: bool = False
            for item in self._types_list_items:
                if item.name == self._edit.text().strip().title():
                    double = True
                    break
            if not double:
                return True
            else:
                debug.info(item=self, keyword="_is_correct_input", message="Typ bereits vorhanden")
                self.set_status_bar("Typ bereits vorhanden")
                return False
        else:
            debug.info(item=self, keyword="_is_correct_input", message="Kein Typ eingegeben")
            self.set_status_bar("Kein Typ eingegeben")
            return False

    def _set_type_activity(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        error_code: ErrorCode = transition.update_type_activity(id_=current_item.id_,
                                                                active=False if current_item.active else True)
        if error_code == ErrorCode.UPDATE_S:
            self._set_current_type()
        else:
            debug.error(item=self, keyword="_set_type_activity", message="Typ konnte nicht gesetzt werden")
            self.handle_error_code(error_code=error_code, type_=f"Typ {current_item.name}")

    def _remove_type(self) -> None:
        current_item: TypesListEntry = self._types_list.currentItem()
        error_code: ErrorCode = transition.delete_type(id_=current_item.id_)
        if error_code == ErrorCode.DELETE_S:
            self._set_current_type()
        else:
            debug.error(item=self, keyword="_remove_type", message="Typ konnte nicht gelöscht werden")
            self.handle_error_code(error_code=error_code, type_=f"Typ {current_item.name}")
