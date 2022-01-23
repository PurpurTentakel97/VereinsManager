# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members Window

from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QLineEdit, QComboBox, QCheckBox, QTextEdit, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QPushButton

from ui.enum_sheet import EditLineType

members_window_: "MembersWindow" or None = None


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
        self._members_list.addItem("test")  # TODO remove
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
        self._first_name_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.FIRST_NAME))
        self._last_name_lb: QLabel = QLabel()
        self._last_name_lb.setText("Nachname:")
        self._last_name_le: QLineEdit = QLineEdit()
        self._last_name_le.setPlaceholderText("Nachname")
        self._last_name_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.LAST_NAME))

        self._address_lb: QLabel = QLabel()
        self._address_lb.setText("Adresse:")
        self._street_le: QLineEdit = QLineEdit()
        self._street_le.setPlaceholderText("Straße")
        self._street_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.STREET))
        self._number_le: QLineEdit = QLineEdit()
        self._number_le.setPlaceholderText("Hausnummer")
        self._number_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.HOUSE_NUMBER))
        self._zip_code_le: QLineEdit = QLineEdit()
        self._zip_code_le.setPlaceholderText("PLZ")
        self._zip_code_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.ZIP_CODE))
        self._city_le: QLineEdit = QLineEdit()
        self._city_le.setPlaceholderText("Stadt")
        self._city_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.CITY))

        self._birth_lb: QLabel = QLabel()
        self._birth_lb.setText("Geburtstag:")
        self._birth_day_le: QLineEdit = QLineEdit()
        self._birth_day_le.setPlaceholderText("Tag")
        self._birth_day_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.B_DAY_DAY))
        self._birth_month_le: QLineEdit = QLineEdit()
        self._birth_month_le.setPlaceholderText("Monat")
        self._birth_month_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.B_DAY_MONTH))
        self._birth_year_le: QLineEdit = QLineEdit()
        self._birth_year_le.setPlaceholderText("Jahr")
        self._birth_year_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.B_DAY_YEAR))
        self._entry_lb: QLabel = QLabel()
        self._entry_lb.setText("Eintritt:")
        self._entry_day_le: QLineEdit = QLineEdit()
        self._entry_day_le.setPlaceholderText("Tag")
        self._entry_day_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.ENTRY_DAY_DAY))
        self._entry_month_le: QLineEdit = QLineEdit()
        self._entry_month_le.setPlaceholderText("Monat")
        self._entry_month_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.ENTRY_DAY_MONTH))
        self._entry_year_le: QLineEdit = QLineEdit()
        self._entry_year_le.setPlaceholderText("Jahr")
        self._entry_year_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.ENTRY_DAY_YEAR))

        self._phone_numbers_lb: QLabel = QLabel()
        self._phone_numbers_lb.setText("Telefon Nummern:")
        self._phone_number_type_box: QComboBox = QComboBox()
        self._phone_number_le: QLineEdit = QLineEdit()
        self._phone_number_le.setPlaceholderText("Nummer")
        self._phone_number_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.PHONE_NUMBER))

        self._mail_address_lb: QLabel = QLabel()
        self._mail_address_lb.setText("Mail Adressen:")
        self._mail_address_type_box: QComboBox = QComboBox()
        self._mail_address_le: QLineEdit = QLineEdit()
        self._mail_address_le.setPlaceholderText("E-Mail")
        self._mail_address_le.textChanged.connect(lambda x: self._current_row_chanced(EditLineType.MAIL_ADDRESS))

        self._member_lb: QLabel = QLabel()
        self._member_lb.setText("Mitgliedsart:")
        self._membership_type_box: QComboBox = QComboBox()
        self._special_member_cb: QCheckBox = QCheckBox()
        self._special_member_cb.toggled.connect(self._set_special_member)
        self._special_member_cb.setText("Ehrenmitglied")

        self._positions_lb: QLabel = QLabel()
        self._positions_lb.setText("Positionen:")
        self._positions_list: QListWidget = QListWidget()
        self._positions_list.addItem("test")  # TODO remove
        self._positions_list.itemClicked.connect(self._set_position)

        self._instruments_lb: QLabel = QLabel()
        self._instruments_lb.setText("Instrumente:")
        self._instruments_list: QListWidget = QListWidget()
        self._instruments_list.addItem("test")  # TODO remove
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
        grid.addWidget(self._birth_day_le, 4, 1)
        grid.addWidget(self._birth_month_le, 4, 2)
        grid.addWidget(self._birth_year_le, 4, 3)
        grid.addWidget(self._entry_lb, 5, 0)
        grid.addWidget(self._entry_day_le, 5, 1)
        grid.addWidget(self._entry_month_le, 5, 2)
        grid.addWidget(self._entry_year_le, 5, 3)

        # phone
        grid.addWidget(self._phone_numbers_lb, 6, 0)
        grid.addWidget(self._phone_number_type_box, 6, 1)
        grid.addWidget(self._phone_number_le, 6, 2, 1, -1)

        # mail
        grid.addWidget(self._mail_address_lb, 7, 0)
        grid.addWidget(self._mail_address_type_box, 7, 1)
        grid.addWidget(self._mail_address_le, 7, 2, 1, -1)

        # member_type
        grid.addWidget(self._member_lb, 8, 0)
        grid.addWidget(self._membership_type_box, 8, 1)
        grid.addWidget(self._special_member_cb, 8, 2)

        # positions
        grid.addWidget(self._positions_lb, 9, 0, 1, 2)
        grid.addWidget(self._positions_list, 10, 0, 1, 2)

        # instruments
        grid.addWidget(self._instruments_lb, 9, 2, 1, -1)
        grid.addWidget(self._instruments_list, 10, 2, 1, -1)

        # comment
        grid.addWidget(self._comment_lb, 11, 0, 1, -1)
        grid.addWidget(self._comment_text, 12, 0, 1, -1)

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
        print("position set")

    def _set_instruments(self) -> None:
        print("instruments set")

    def _set_special_member(self) -> None:
        print(f"special member set {self._special_member_cb.isChecked()}")

    def _current_row_chanced(self, edit_line: EditLineType) -> None:
        match edit_line:
            case EditLineType.FIRST_NAME:
                print(self._first_name_le.text())
            case EditLineType.LAST_NAME:
                print(self._last_name_le.text())

            case EditLineType.STREET:
                print(self._street_le.text())
            case EditLineType.HOUSE_NUMBER:
                print(self._number_le.text())
            case EditLineType.ZIP_CODE:
                print(self._zip_code_le.text())
            case EditLineType.CITY:
                print(self._city_le.text())

            case EditLineType.B_DAY_DAY:
                print(self._birth_day_le.text())
            case EditLineType.B_DAY_YEAR:
                print(self._birth_year_le.text())
            case EditLineType.B_DAY_MONTH:
                print(self._birth_month_le.text())

            case EditLineType.ENTRY_DAY_DAY:
                print(self._entry_day_le.text())
            case EditLineType.ENTRY_DAY_YEAR:
                print(self._entry_year_le.text())
            case EditLineType.ENTRY_DAY_MONTH:
                print(self._entry_month_le.text())

            case EditLineType.PHONE_NUMBER:
                print(self._phone_number_le.text())
            case EditLineType.MAIL_ADDRESS:
                print(self._mail_address_le.text())

    def _comment_chanced(self) -> None:
        print(self._comment_text.toPlainText())

    def _add_member(self) -> None:
        print("member added")

    def _remove_member(self) -> None:
        print("member remuved")

    def _save_member(self) -> None:
        print("member saved")

    def _save_all(self) -> None:
        print("all saved")
