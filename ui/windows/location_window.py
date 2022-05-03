# Purpur Tentakel
# 05.02.2022
# VereinsManager // Location Window

from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QWidget

import transition
from config import config_sheet as c
from ui.base_window import BaseWindow
from ui.frames.list_frame import ListItem, ListFrame
from ui import window_manager as w
import debug

debug_str: str = "LocationWindow"


class LocationWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._raw_country_ids: list = list()
        self._is_edit: bool = bool()

        self._create_ui()
        self._create_layout()
        self._set_window_information()
        self._load_countries()
        self._set_first_location()

    def _create_ui(self) -> None:
        self._location_lb: QLabel = QLabel("Orte:")
        self._export_location_btn: QPushButton = QPushButton("Ort Exportieren")

        self._location_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_location_name,
                                                   list_method=self.load_location, active=True)

        self._add_location_btn: QPushButton = QPushButton("Ort hinzufügen")
        self._add_location_btn.clicked.connect(self._add_location)
        self._delete_location_btn: QPushButton = QPushButton("Ort löschen")
        self._recover_location_btn: QPushButton = QPushButton("Ort wieder herstellen")

        self._save_btn: QPushButton = QPushButton("Speichern")
        self._save_btn.clicked.connect(self._save)
        self._break_btn: QPushButton = QPushButton("Zurücksetzten")
        self._break_btn.clicked.connect(lambda: self._set_edite_mode(is_edit=False))

        self._owner_lb: QLabel = QLabel("Inhaber:")
        self._owner_le: QLineEdit = QLineEdit()
        self._owner_le.setPlaceholderText("Inhaber des Ortes")
        self._owner_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._name_lb: QLabel = QLabel("Name:")
        self._name_le: QLineEdit = QLineEdit()
        self._name_le.setPlaceholderText("Name des Ortes")
        self._name_le.textChanged.connect(self._set_name_le)

        self._address_lb: QLabel = QLabel("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._country_box: QComboBox = QComboBox()
        self._country_box.currentTextChanged.connect(lambda: self._set_edite_mode(is_edit=True))

        self._maps_link_le: QLineEdit = QLineEdit()
        self._maps_link_le.setPlaceholderText("Google Maps URL (falls nötig // nicht empfohlen)")
        self._maps_link_le.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))
        self._maps_link_btn: QPushButton = QPushButton("Google Maps")

        self._comment_lb: QLabel = QLabel("Kommantar:")
        self._comment_text: QTextEdit = QTextEdit()
        self._comment_text.setPlaceholderText("Füge einen Kommentar hinzu....")
        self._comment_text.textChanged.connect(lambda: self._set_edite_mode(is_edit=True))

    def _create_layout(self) -> None:
        header_btn_hbox: QHBoxLayout = QHBoxLayout()
        header_btn_hbox.addWidget(self._location_lb)
        header_btn_hbox.addStretch()
        header_btn_hbox.addWidget(self._export_location_btn)

        footer_btn_hbox: QHBoxLayout = QHBoxLayout()
        footer_btn_hbox.addWidget(self._add_location_btn)
        footer_btn_hbox.addWidget(self._delete_location_btn)
        footer_btn_hbox.addWidget(self._recover_location_btn)
        footer_btn_hbox.addStretch()
        footer_btn_hbox.addWidget(self._break_btn)
        footer_btn_hbox.addWidget(self._save_btn)

        row = 0
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._owner_lb, row, 0, 1, 1)
        grid.addWidget(self._owner_le, row, 1, 1, -1)

        row += 1
        grid.addWidget(self._name_lb, row, 0, 1, 1)
        grid.addWidget(self._name_le, row, 1, 1, -1)

        row += 1
        grid.addWidget(self._address_lb, row, 0, 1, 1)
        grid.addWidget(self._street_le, row, 1, 1, 2)
        grid.addWidget(self._number_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._zip_code_le, row, 1, 1, 1)
        grid.addWidget(self._city_le, row, 2, 1, 1)
        grid.addWidget(self._country_box, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._maps_link_le, row, 1, 1, 2)
        grid.addWidget(self._maps_link_btn, row, 3, 1, -1)

        row += 1
        grid.addWidget(self._comment_lb, row, 0, 1, 1)
        row += 1
        grid.addWidget(self._comment_text, row, 0, 1, -1)

        inner_hbox: QHBoxLayout = QHBoxLayout()
        inner_hbox.addWidget(self._location_list)
        inner_hbox.addLayout(grid)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(header_btn_hbox)
        global_vbox.addLayout(inner_hbox)
        global_vbox.addLayout(footer_btn_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.show()

    def _add_location(self) -> None:
        new_location: ListItem = ListItem(ID=None)
        self._location_list.list_items.append(new_location)
        self._location_list.list.addItem(new_location)
        self._location_list.list.setCurrentItem(new_location)

        self._set_location_None()

        self._set_edite_mode()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Orte")

    def _set_edite_mode(self, is_edit: bool = True) -> None:
        self._is_edit = is_edit
        invert_is_edit: bool = not is_edit

        self._save_btn.setEnabled(self._is_edit)
        self._break_btn.setEnabled(self._is_edit)

        self._add_location_btn.setEnabled(invert_is_edit)
        self._delete_location_btn.setEnabled(invert_is_edit)
        self._recover_location_btn.setEnabled(invert_is_edit)
        self._location_list.list.setEnabled(invert_is_edit)

    def _set_name_le(self) -> None:
        current_location: ListItem = self._location_list.list.currentItem()
        current_location.first_name = self._name_le.text().strip()
        current_location.set_name()
        self._set_edite_mode()

    def _set_first_location(self) -> None:
        self.load_location()

    def _set_location_None(self) -> None:
        self._owner_le.setText("")
        self._name_le.setText("")
        self._street_le.setText("")
        self._number_le.setText("")
        self._zip_code_le.setText("")
        self._city_le.setText("")
        self._maps_link_le.setText("")
        self._comment_text.setText("")

    def _load_countries(self) -> None:
        data, valid = transition.get_single_type(raw_type_id=c.config.raw_type_id['country'], active=True)
        if not valid:
            self.set_error_bar(message=data)
            return
        for ID, name, *_ in data:
            self._raw_country_ids.append((ID, name))
            self._country_box.addItem(name)

    def load_location(self) -> None:
        current_location: ListItem = self._location_list.list.currentItem()
        if current_location is None:
            self._add_location()
            return

        data, valid = transition.get_single_location_ID(ID=current_location.ID)
        if not valid:
            self.set_error_bar(message=data)
            return

        self._owner_le.setText(data['owner'] if not None else "")
        self._name_le.setText(data['name'] if not None else "")
        self._street_le.setText(data['street'] if not None else "")
        self._number_le.setText(data['number'] if not None else "")
        self._zip_code_le.setText(data['zip_code'] if not None else "")
        self._city_le.setText(data['city'] if not None else "")
        self._country_box.setCurrentText(data['country'])
        self._maps_link_le.setText(data['maps_link'] if not None else "")
        self._comment_text.setText(data['comment'] if not None else "")

        self._set_edite_mode(is_edit=False)

    def _save(self) -> None:
        current_location: ListItem = self._location_list.list.currentItem()
        output: dict = {
            "ID": current_location.ID,
            "owner": self._owner_le.text().strip() if not self._owner_le.text().strip() == "" else None,
            "name": self._name_le.text().strip() if not self._name_le.text().strip() == "" else None,
            "street": self._street_le.text().strip().title() if not self._street_le.text().strip() == "" else None,
            "number": self._number_le.text().strip().title() if not self._number_le.text().strip() == "" else None,
            "zip_code": self._zip_code_le.text().strip() if not self._zip_code_le.text().strip() == "" else None,
            "city": self._city_le.text().strip().title() if not self._city_le.text().strip() == "" else None,
            "country": self._country_box.currentText(),
            "maps_link": self._maps_link_le.text().strip() if not self._maps_link_le.text().strip() == "" else None,
            "comment": self._comment_text.toPlainText() if not self._comment_text.toPlainText() == "" else None,
        }

        ID, valid = transition.save_location(data=output)
        if not valid:
            self.set_error_bar(message=ID)
            return

        if ID:
            current_location.ID = ID
        self.set_info_bar(message="saved")
        self._set_edite_mode(is_edit=False)

    def closeEvent(self, event) -> None:
        event.ignore()
        w.window_manger.location_window = None
        event.accept()
