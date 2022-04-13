# Purpur Tentakel
# 08.04.2022
# VereinsManager / Organisation Data Window

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QTextEdit, QGridLayout, QHBoxLayout, \
    QVBoxLayout, QWidget

import transition
from ui.windows import window_manager as w
from ui.windows.base_window import BaseWindow
import debug

debug_str: str = "OrganisationDataWindow"


class OrganisationDataWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.ID: int | None = None
        self.contact_persons: list = list()

        self._set_window_information()
        self._create_ui()
        self._create_layout()
        self._set_contact_persons()
        self._set_organisation_data()

    def _create_ui(self) -> None:
        # buttons
        self._save_btn: QPushButton = QPushButton("Speichern")
        self._save_btn.clicked.connect(self._save)
        self._restore_btn: QPushButton = QPushButton("Zurücksetzten")
        self._restore_btn.clicked.connect(self._set_organisation_data)

        # organisation
        self._organisation_name_lb: QLabel = QLabel("Name:")
        self._name_le: QLineEdit = QLineEdit()
        self._name_le.setPlaceholderText("Name")

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.setValidator(QIntValidator())
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._county_le: QLineEdit = QLineEdit()
        self._county_le.setPlaceholderText("Land")

        self._bank_lb: QLabel = QLabel("Bankverbundung:")
        self._bank_name_le: QLineEdit = QLineEdit()
        self._bank_name_le.setPlaceholderText("Name")
        self._bank_owner_le: QLineEdit = QLineEdit()
        self._bank_owner_le.setPlaceholderText("Inhaber")
        self._bank_IBAN_le: QLineEdit = QLineEdit()
        self._bank_IBAN_le.setPlaceholderText("IBAN")
        self._bank_BIC_le: QLineEdit = QLineEdit()
        self._bank_BIC_le.setPlaceholderText("BIC")

        self._contact_person_lb: QLabel = QLabel("Komtaktperson:")
        self._contact_person_box: QComboBox = QComboBox()

        self._web_lb: QLabel = QLabel("Homepage:")
        self._web_le: QLineEdit = QLineEdit()
        self._web_le.setPlaceholderText("Homepage")

        self._extra_info_lb: QLabel = QLabel("Extra Infos:")
        self._extra_info_text: QTextEdit = QTextEdit()
        self._extra_info_text.setPlaceholderText("Extra Infos")
        self._extra_info_text.setTabChangesFocus(True)

    def _create_layout(self) -> None:
        extra_text_vbox: QVBoxLayout = QVBoxLayout()
        extra_text_vbox.addWidget(self._extra_info_lb)
        extra_text_vbox.addStretch()

        grid: QGridLayout = QGridLayout()
        row: int = 0
        grid.addWidget(self._organisation_name_lb, row, 0, 1, 1)
        grid.addWidget(self._name_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._address_lb, row, 0, 1, 1)
        grid.addWidget(self._street_le, row, 1, 1, 2)
        grid.addWidget(self._number_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._zip_code_le, row, 1, 1, 1)
        grid.addWidget(self._city_le, row, 2, 1, 1)
        grid.addWidget(self._county_le, row, 3, 1, 1)
        row += 1
        grid.addWidget(self._bank_lb, row, 0, 1, 1)
        grid.addWidget(self._bank_name_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._bank_owner_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._bank_IBAN_le, row, 1, 1, 2)
        grid.addWidget(self._bank_BIC_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._contact_person_lb, row, 0, 1, 1)
        grid.addWidget(self._contact_person_box, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._web_lb, row, 0, 1, 1)
        grid.addWidget(self._web_le, row, 1, 1, -1)
        row += 1
        grid.addLayout(extra_text_vbox, row, 0, 1, 1)
        grid.addWidget(self._extra_info_text, row, 1, 1, -1)

        buttons_hbox: QHBoxLayout = QHBoxLayout()
        buttons_hbox.addStretch()
        buttons_hbox.addWidget(self._restore_btn)
        buttons_hbox.addWidget(self._save_btn)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(grid)
        global_vbox.addLayout(buttons_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.show()

    def _get_ID_from_contact_person(self) -> int | None:
        current_entry: str = self._contact_person_box.currentText()

        for ID, display_name in self.contact_persons:
            if current_entry == display_name:
                return ID

        return None

    @staticmethod
    def _get_display_name(firstname: str, lastname: str) -> str:
        if firstname and lastname:
            return f"{firstname} {lastname}"
        if firstname:
            return firstname
        if lastname:
            return lastname
        return "Kein Name vorhanden"

    def _set_window_information(self) -> None:
        self.setWindowTitle("Vereinsinformationen")

    def _set_contact_persons(self) -> None:
        data, valid = transition.get_all_user_name()  # TODO chance to without default when validation is ready
        if not valid:
            self.set_error_bar(message=data)

        contact_persons: list = list()
        for ID, firstname, lastname in data:
            display_name = self._get_display_name(firstname=firstname, lastname=lastname)
            contact_persons.append([ID, display_name])
            self._contact_person_box.addItem(display_name)

        self.contact_persons = contact_persons

    def _set_organisation_data(self) -> None:
        data, valid = transition.get_organisation_data()
        if not valid:
            self.set_error_bar(message=data)
            return

        self.ID = data['ID']
        self._name_le.setText("" if data['name'] is None else data['name'])
        self._street_le.setText("" if data['street'] is None else data['street'])
        self._number_le.setText("" if data['number'] is None else data['number'])
        self._zip_code_le.setText("" if data['zip_code'] is None else data['zip_code'])
        self._city_le.setText("" if data['city'] is None else data['city'])
        self._county_le.setText("" if data['country'] is None else data['country'])
        self._bank_name_le.setText("" if data['bank_name'] is None else data['bank_name'])
        self._bank_owner_le.setText("" if data['bank_owner'] is None else data['bank_owner'])
        self._bank_IBAN_le.setText("" if data['bank_IBAN'] is None else data['bank_IBAN'])
        self._bank_BIC_le.setText("" if data['bank_BIC'] is None else data['bank_BIC'])
        self._web_le.setText("" if data['web_link'] is None else data['web_link'])
        self._extra_info_text.setText("" if data['extra_text'] is None else data['extra_text'])
        self._contact_person_box.setCurrentText(
            self._get_display_name(firstname=data['contact_person'][1], lastname=data['contact_person'][2]))

    def _save(self) -> None:
        data: dict = {
            "ID": self.ID,
            "name": None if self._name_le.text().strip() == "" else self._name_le.text().strip(),
            "street": None if self._street_le.text().strip() == "" else self._street_le.text().strip().title(),
            "number": None if self._number_le.text().strip() == "" else self._number_le.text().strip(),
            "zip_code": None if self._zip_code_le.text().strip() == "" else self._zip_code_le.text().strip(),
            "city": None if self._city_le.text().strip() == "" else self._city_le.text().strip().title(),
            "country": None if self._county_le.text().strip() == "" else self._county_le.text().strip().title(),
            "bank_name": None if self._bank_name_le.text().strip() == "" else self._bank_name_le.text().strip().title(),
            "bank_owner": None if self._bank_owner_le.text().strip() == "" else self._bank_owner_le.text().strip().title(),
            "bank_IBAN": None if self._bank_IBAN_le.text() == "" else self._bank_IBAN_le.text().strip(),
            "bank_BIC": None if self._bank_BIC_le.text().strip() == "" else self._bank_BIC_le.text().strip(),
            "contact_person": self._get_ID_from_contact_person(),
            "web_link": None if self._web_le.text().strip() == "" else self._web_le.text().strip(),
            "extra_text": None if self._extra_info_text.toPlainText().strip() == "" else self._extra_info_text.toPlainText().strip(),
        }

        ID, result = transition.add_update_organisation(data=data)

        if not result:
            self.set_error_bar(message=ID)
            return
        else:
            self.ID = ID
            self.set_info_bar(message="saved")

    def closeEvent(self, event) -> None:
        event.ignore()
        w.window_manger.organisation_data_window = None
        event.accept()
