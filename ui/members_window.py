# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton, QDateEdit

from ui.base_window import BaseWindow
from ui.enum_sheet import EditLineType, DateType

members_window_: "MembersWindow" or None = None


class MemberListItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
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
        self.positions: list[PositionInstrumentListItem] = list()
        self.instruments: list[PositionInstrumentListItem] = list()

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


class PositionInstrumentListItem(QListWidgetItem):
    def __init__(self, name_str):
        super().__init__()
        self.name: str = name_str
        self._set_name()

    def _set_name(self):
        self.setText(self.name)


class MembersWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self._set_layout()

    def _set_ui(self) -> None:
        # Left
        self._members_lb: QLabel = QLabel()
        self._members_lb.setText("Mitglieder:")

        self._members_list: QListWidget = QListWidget()
        self._members_list.addItem(MemberListItem())  # TODO remove
        self._members_list.itemClicked.connect(self._set_current_member)

        self._add_member_btn: QPushButton = QPushButton()
        self._add_member_btn.setText("Mitglied hinzufügen")
        self._add_member_btn.clicked.connect(self._add_member)
        self._remove_member_btn: QPushButton = QPushButton()
        self._remove_member_btn.setText("Mitglied löschen")
        self._remove_member_btn.clicked.connect(self._remove_member)

        self._save_single_btn: QPushButton = QPushButton()
        self._save_single_btn.setText("Mitglied speichern")
        self._save_single_btn.clicked.connect(self._save_member)
        self._save_all_btn: QPushButton = QPushButton()
        self._save_all_btn.setText("Alles speichern")
        self._save_all_btn.clicked.connect(self._save_all)

        # Right
        self._first_name_lb: QLabel = QLabel()
        self._first_name_lb.setText("Vorname:")
        self._first_name_le: QLineEdit = QLineEdit()
        self._first_name_le.setPlaceholderText("Vorname")
        self._first_name_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.FIRST_NAME))
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.LAST_NAME))

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.STREET))
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.HOUSE_NUMBER))
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.ZIP_CODE))
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.CITY))

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._b_day_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._b_day_date.dateChanged.connect(lambda x: self._current_date_chanced(DateType.B_DAY))
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_date: QDateEdit = QDateEdit(calendarPopup=True)
        self._entry_date.dateChanged.connect(lambda x: self._current_date_chanced(DateType.ENTRY))

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")
        self._phone_number_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.PHONE_NUMBER))

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")
        self._mail_address_le.textChanged.connect(lambda x: self._current_le_text_chanced(EditLineType.MAIL_ADDRESS))

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.toggled.connect(self._set_special_member)
        self._special_member_cb.setText("Ehrenmitglied")

        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()
        self._positions_list.addItem(PositionInstrumentListItem("Vorstand"))  # TODO remove
        self._positions_list.itemClicked.connect(self._set_position)

        self._instruments_lb: QLabel = QLabel()
        self._instruments_lb.setText("Instrumente:")
        self._instruments_list: QListWidget = QListWidget()
        self._instruments_list.addItem(PositionInstrumentListItem("Klavier"))  # TODO remove
        self._instruments_list.itemClicked.connect(self._set_instruments)

        self._comment_lb: QLabel = QLabel()
        self._comment_lb.setText("Kommentar:")
        self._comment_text: QTextEdit = QTextEdit()
        self._comment_text.textChanged.connect(self._comment_chanced)

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

        # Right
        # name
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._first_name_lb, 0, 0, 1, 1)
        grid.addWidget(self._first_name_le, 0, 1, 1, -1)
        grid.addWidget(self._last_name_lb, 1, 0, 1, 1)
        grid.addWidget(self._last_name_le, 1, 1, 1, -1)

        # address
        grid.addWidget(self._address_lb, 2, 0)
        grid.addWidget(self._street_le, 2, 1, 1, 2)
        grid.addWidget(self._number_le, 2, 3, 1, -1)
        grid.addWidget(self._zip_code_le, 3, 1)
        grid.addWidget(self._city_le, 3, 2)

        grid.addWidget(self._birth_lb, 4, 0)
        grid.addWidget(self._b_day_date, 4, 1)
        grid.addWidget(self._entry_lb, 4, 2, alignment=Qt.AlignRight)
        grid.addWidget(self._entry_date, 4, 3, 1, -1)

        # phone
        grid.addWidget(self._phone_numbers_lb, 5, 0)
        grid.addWidget(self._phone_number_type_box, 5, 1)
        grid.addWidget(self._phone_number_le, 5, 2, 1, -1)

        # mail
        grid.addWidget(self._mail_address_lb, 6, 0)
        grid.addWidget(self._mail_address_type_box, 6, 1)
        grid.addWidget(self._mail_address_le, 6, 2, 1, -1)

        # member_type
        grid.addWidget(self._member_lb, 7, 0)
        grid.addWidget(self._membership_type_box, 7, 1)
        grid.addWidget(self._special_member_cb, 7, 2)

        # positions
        grid.addWidget(self._positions_lb, 8, 0, 1, 2)
        grid.addWidget(self._positions_list, 9, 0, 1, 2)

        # instruments
        grid.addWidget(self._instruments_lb, 8, 2, 1, -1)
        grid.addWidget(self._instruments_list, 9, 2, 1, -1)

        # comment
        grid.addWidget(self._comment_lb, 10, 0, 1, -1)
        grid.addWidget(self._comment_text, 11, 0, 1, -1)

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

    def _set_current_member(self) -> None:
        print("current member set")

    def _set_position(self) -> None:
        current_member:MemberListItem = self._members_list.currentItem()
        current_position: PositionInstrumentListItem = self._positions_list.currentItem()

        if current_position not in current_member.positions:
            current_member.positions.append(current_position)
            current_position.setBackground(QColor("Light Grey"))

        else:
            current_member.positions.remove(current_position)
            current_position.setBackground(QColor("White"))

        self._positions_list.setCurrentItem(None)
        print(current_member.positions)

    def _set_instruments(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_instrument: PositionInstrumentListItem = self._instruments_list.currentItem()

        if current_instrument not in current_member.instruments:
            current_member.instruments.append(current_instrument)
            current_instrument.setBackground(QColor("Light Grey"))

        else:
            current_member.instruments.remove(current_instrument)
            current_instrument.setBackground(QColor("White"))

        self._instruments_list.setCurrentItem(None)
        print(current_member.instruments)

    def _set_special_member(self) -> None:
        current_item: MemberListItem = self._members_list.currentItem()
        current_item.special_member = (self._special_member_cb.isChecked())
        print(current_item.special_member)

    def _current_le_text_chanced(self, edit_line: EditLineType) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        match edit_line:
            case EditLineType.FIRST_NAME:
                current_member.first_name = self._first_name_le.text().strip() \
                    if self._first_name_le.text().strip() else None
                current_member.set_name()
                print(current_member.first_name)
            case EditLineType.LAST_NAME:
                current_member.last_name = self._last_name_le.text().strip() \
                    if self._last_name_le.text().strip() else None
                current_member.set_name()
                print(current_member.last_name)

            case EditLineType.STREET:
                current_member.street = self._street_le.text().strip() \
                    if self._street_le.text().strip() else None
                print(current_member.street)
            case EditLineType.HOUSE_NUMBER:
                current_member.number = self._number_le.text().strip() \
                    if self._number_le.text().strip() else None
                print(current_member.number)
            case EditLineType.ZIP_CODE:
                current_member.zip_code = self._zip_code_le.text().strip() \
                    if self._zip_code_le.text().strip() else None
                print(current_member.zip_code)
            case EditLineType.CITY:
                current_member.city = self._city_le.text().strip() \
                    if self._city_le.text().strip() else None
                print(current_member.city)

            case EditLineType.PHONE_NUMBER:
                pass
            case EditLineType.MAIL_ADDRESS:
                print(self._mail_address_le.text())

    def _comment_chanced(self) -> None:
        current_member: MemberListItem = self._members_list.currentItem()
        current_member.comment_text = self._comment_text.toPlainText().strip() \
            if self._comment_text.toPlainText().strip() else None
        print(current_member.comment_text)

    def _add_member(self) -> None:
        print("member added")

    def _remove_member(self) -> None:
        print("member remuved")

    def _save_member(self) -> None:
        print("member saved")

    def _save_all(self) -> None:
        print("all saved")
