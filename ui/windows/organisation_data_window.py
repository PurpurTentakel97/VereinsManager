# Purpur Tentakel
# 08.04.2022
# VereinsManager / Organisation Data Window

# name
# adresse
#     straße
#     nummer
#     plz
#     stadt
#     land
# allgemeiner Ansprechpartner
#     drop down per user
# web
# bankverbindung
#     name
#     Inhaber
#     IBAN
#     BIC
# zusatzinfos

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QTextEdit, QGridLayout, QHBoxLayout, \
    QVBoxLayout, QWidget

from ui.windows.base_window import BaseWindow
from ui.windows import window_manager as w_m


class OrganisationDataWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Vereinsinformationen")

    def _create_ui(self) -> None:
        # buttons
        self._save_btn: QPushButton = QPushButton("Speichern")
        self._restore_btn: QPushButton = QPushButton("Zurücksetzten")

        # organisation
        self._organisation_name_lb: QLabel = QLabel("Name:")
        self._organisation_name_le: QLineEdit = QLineEdit()
        self._organisation_name_le.setPlaceholderText("Name")

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

    def _create_layout(self) -> None:
        extra_text_vbox: QVBoxLayout = QVBoxLayout()
        extra_text_vbox.addWidget(self._extra_info_lb)
        extra_text_vbox.addStretch()

        grid: QGridLayout = QGridLayout()
        row: int = 0
        grid.addWidget(self._organisation_name_lb, row, 0, 1, 1)
        grid.addWidget(self._organisation_name_le, row, 1, 1, -1)
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

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.organisation_data_window = None
        event.accept()
