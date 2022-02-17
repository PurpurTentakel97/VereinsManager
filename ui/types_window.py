# Purpur Tentakel
# 21.01.2022
# VereinsManager /Types Window

from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QComboBox, QListWidget, QListWidgetItem, QLineEdit

import debug
from ui.base_window import BaseWindow
import transition

types_window_: "TypesWindow" or None = None


class TypesListEntry(QListWidgetItem):
    def __init__(self, type_: tuple) -> None:
        super().__init__()
        self.id_: int = int()
        self.name: str = str()
        self.raw_id: int = int()
        self.raw_name: str = str()
        self.id_, self.name, self.raw_id, self.raw_name = type_
        self._set_name()

    def _set_name(self) -> None:
        self.setText(self.name)


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
        self._edit.returnPressed.connect(self._edit_line_return_pressed)
        self._edit.setPlaceholderText("Typ:")

        self._add_btn: QPushButton = QPushButton()
        self._add_btn.setText("Typ hinzufügen")
        self._add_btn.setEnabled(False)
        self._add_btn.clicked.connect(self._add_type)
        self._edit_btn: QPushButton = QPushButton()
        self._edit_btn.setText("Typ bearbeiten")
        self._edit_btn.setEnabled(False)
        self._edit_btn.clicked.connect(self._edit_type)
        self._remove_btn: QPushButton = QPushButton()
        self._remove_btn.setText("Typ löschen")
        self._remove_btn.setEnabled(False)
        self._remove_btn.clicked.connect(self._remove_type)

        self._types_list: QListWidget = QListWidget()
        self._types_list.currentItemChanged.connect(self._row_chanced)

    def _create_layout(self) -> None:
        grid: QGridLayout = QGridLayout()

        row: int = 0
        grid.addWidget(self._types_box, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._edit, row, 0, 1, -1)

        row += 1
        grid.addWidget(self._add_btn, row, 0)
        grid.addWidget(self._edit_btn, row, 1)
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
        self._add_btn.setEnabled(self._is_add())
        self._edit_btn.setEnabled(self._is_edit())
        self._remove_btn.setEnabled(self._is_remove())
        types: tuple = transition.get_single_type(raw_type_id=self._get_id_from_raw_type(self._types_box.currentText()))
        for type_ in types:
            new_type: TypesListEntry = TypesListEntry(type_)
            self._types_list.addItem(new_type)
            self._types_list_items.append(new_type)
        self._edit.setFocus()
        self._types_list.setCurrentItem(None)

    def _set_types(self) -> None:
        self._raw_types = transition.get_raw_types()
        self._types_box.clear()
        for ID, text in self._raw_types:
            self._types_box.addItem(text)
        debug.info(item=self, keyword="_set_types", message=f"all active types = {self._raw_types}")

    def _row_chanced(self) -> None:
        current_type: TypesListEntry = self._types_list.currentItem()
        self._set_btn()
        if current_type is not None:
            self._edit.setText(current_type.name)
        self._edit.setFocus()

    def _text_chanced(self) -> None:
        self._set_btn()

    def _set_btn(self) -> None:
        self._add_btn.setEnabled(self._is_add())
        self._edit_btn.setEnabled(self._is_edit())
        self._remove_btn.setEnabled(self._is_remove())

    def _is_add(self) -> bool:
        return self._types_list.currentItem() is None and len(self._edit.text().strip()) > 0

    def _is_edit(self) -> bool:
        return self._types_list.currentItem() is not None and len(self._edit.text().strip()) > 0

    def _is_remove(self) -> bool:
        return self._types_list.currentItem() is not None

    def _edit_line_return_pressed(self) -> None:
        if self._is_edit():
            self._edit_type()
        else:
            self._add_type()

    def _get_id_from_raw_type(self, type_name: str) -> int:
        for ID, type_ in self._raw_types:
            if type_ == type_name:
                return ID

    def _add_type(self) -> None:
        if len(self._edit.text().strip()) > 0:
            double: bool = False
            for item in self._types_list_items:
                if item.name == self._edit.text():
                    double = True
                    break
            if not double:
                transition.add_type(display_name=self._types_box.currentText(), type_=self._edit.text().strip().title())
                self._set_current_type()
            else:
                self.set_status_bar("Typ bereits vorhanden")
        else:
            self.set_status_bar("Kein Name eingegeben")

    def _edit_type(self) -> None:
        transition.edit_type(display_name=self._types_box.currentText(), new_type_=self._edit.text().strip().title(),
                             type_id=self._types_list.currentItem().id_)
        self._set_current_type()
        self._edit.clear()

    def _remove_type(self) -> None:
        transition.remove_type(display_name=self._types_box.currentText(), type_id=self._types_list.currentItem().id_)
        self._set_current_type()
        self._edit.clear()
