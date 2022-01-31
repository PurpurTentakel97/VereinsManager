# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit

from ui.base_window import BaseWindow

members_window_: "MembersWindow" or None = None


class MemberListItem(QListWidgetItem):
    def __init__(self, id_: int | None = None):
        super().__init__()
        self.id_: int = id_
        self.first_name: str | None = None
        self.last_name: str | None = None

        self.street: str | None = None
        self.number: str | None = None
        self.zip_code: str | None = None
        self.city: str | None = None

        self.birth_date: QDate = QDate()
        self.entry_date: QDate = QDate()

        self.phone_numbers: dict[str, str] = dict()
        self.mail_addresses: dict[str, str] = dict()

        self.membership_type: str | None = None
        self.special_member: bool = False
        self.positions: list[PositionListItem] = list()
        self.instruments: list[PositionListItem] = list()

        self.comment_text: str | None = None

        self.set_name()

    def set_name(self) -> None:
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


class PositionListItem(QListWidgetItem):
    def __init__(self, name_str):
        super().__init__()
        self.name: str = name_str
        self._set_name()

    def _set_name(self):
        self.setText(self.name)


# noinspection PyArgumentList
class MembersWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._member_counter: int = int()
        self._positions: list[PositionListItem] = list()

        self._set_ui()
        self._set_layout()

    def _set_ui(self) -> None:
        # Left
        self._members_lb: QLabel = QLabel()
        self._members_lb.setText("Mitglieder:")

        self._members_list: QListWidget = QListWidget()

        self._add_member_btn: QPushButton = QPushButton()
        self._add_member_btn.setText("Mitglied hinzufügen")
        self._remove_member_btn: QPushButton = QPushButton()
        self._remove_member_btn.setText("Mitglied löschen")

        self._save_single_btn: QPushButton = QPushButton()
        self._save_single_btn.setText("Mitglied speichern")
        self._save_all_btn: QPushButton = QPushButton()
        self._save_all_btn.setText("Alles speichern")

        # Right
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")

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

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._b_day_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_date: QDateEdit = QDateEdit(calendarPopup=True)

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.setText("Ehrenmitglied")

        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()

        self._comment_lb: QLabel = QLabel()
        self._comment_lb.setText("Kommentar:")
        self._comment_text: QTextEdit = QTextEdit()

    def _set_layout(self) -> None:
        # Left
        label_members_hbox: QHBoxLayout = QHBoxLayout()
        label_members_hbox.addWidget(self._members_lb)
        label_members_hbox.addStretch()

        button_members_hbox: QHBoxLayout = QHBoxLayout()
        button_members_hbox.addWidget(self._add_member_btn)
        button_members_hbox.addWidget(self._remove_member_btn)
        button_members_hbox.addStretch()
        button_members_hbox.addWidget(self._save_single_btn)
        button_members_hbox.addWidget(self._save_all_btn)

        row: int = 0
        # Right
        # name
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._first_name_lb, row, 0, 1, 1)
        grid.addWidget(self._first_name_le, row, 1, 1, -1)
        row += 1
        grid.addWidget(self._last_name_lb, row, 0, 1, 1)
        grid.addWidget(self._last_name_le, row, 1, 1, -1)

        # address
        row += 1
        grid.addWidget(self._address_lb, row, 0)
        grid.addWidget(self._street_le, row, 1, 1, 2)
        grid.addWidget(self._number_le, row, 3, 1, -1)
        row += 1
        grid.addWidget(self._zip_code_le, row, 1)
        grid.addWidget(self._city_le, row, 2)

        row += 1
        grid.addWidget(self._birth_lb, row, 0)
        grid.addWidget(self._b_day_date, row, 1)
        grid.addWidget(self._entry_lb, row, 2, alignment=Qt.AlignRight)
        grid.addWidget(self._entry_date, row, 3, 1, -1)

        # phone
        row += 1
        grid.addWidget(self._phone_numbers_lb, row, 0)
        grid.addWidget(self._phone_number_type_box, row, 1)
        grid.addWidget(self._phone_number_le, row, 2, 1, -1)

        # mail
        row += 1
        grid.addWidget(self._mail_address_lb, row, 0)
        grid.addWidget(self._mail_address_type_box, row, 1)
        grid.addWidget(self._mail_address_le, row, 2, 1, -1)

        # member_type
        row += 1
        grid.addWidget(self._member_lb, row, 0)
        grid.addWidget(self._membership_type_box, row, 1)
        grid.addWidget(self._special_member_cb, row, 2)

        # positions / comment
        row += 1
        grid.addWidget(self._positions_lb, row, 0, 1, 2)
        grid.addWidget(self._comment_lb, row, 2, 1, -1)

        row += 1
        grid.addWidget(self._positions_list, row, 0, 1, 2)
        grid.addWidget(self._comment_text, row, 2, 1, -1)

        right_vbox: QVBoxLayout = QVBoxLayout()
        right_vbox.addLayout(grid)
        right_vbox.addStretch()

        # Global
        sub_global_hbox: QHBoxLayout = QHBoxLayout()
        sub_global_hbox.addWidget(self._members_list)
        sub_global_hbox.addLayout(right_vbox)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(label_members_hbox)
        global_vbox.addLayout(sub_global_hbox)
        global_vbox.addLayout(button_members_hbox)

        # set Layout
        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget)
        self.show()
