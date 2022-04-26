# Purpur Tentakel
# 26.04.2022
# VereinsManager / Member Export Frame

from datetime import datetime
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIntValidator

from ui.frames.list_frame import ListFrame, ListItem
import transition
import debug

debug_str: str = "MemberExportFrame"


class MemberExportFrame(QFrame):
    def __init__(self):
        super().__init__()

        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        self.member_list: ListFrame = ListFrame(window=self, get_names_method=transition.get_all_member_name,
                                                list_method=self.set_current_member, active=True)

        self._export_member_table_btn: QPushButton = QPushButton("Mitlieder Tabelle")
        self._export_member_card_btn: QPushButton = QPushButton("Mitglieder Karte")
        self._export_current_anniversary_btn: QPushButton = QPushButton("Aktuelle Jubiläen")
        self._export_other_anniversary_btn: QPushButton = QPushButton("Jubiläen im Jahr")

        self._export_other_anniversary_le: QLineEdit = QLineEdit()
        self._export_other_anniversary_le.setValidator(QIntValidator())
        self._export_other_anniversary_le.setPlaceholderText("zu exportierendes Jahr")
        self._export_other_anniversary_le.setText(str(datetime.now().year))

    def _create_layout(self) -> None:
        grid: QGridLayout = QGridLayout()
        row: int = 0
        grid.addWidget(self._export_member_table_btn, row, 0, 1, 1)
        grid.addWidget(self._export_member_card_btn, row, 1, 1, 1)
        row += 1
        grid.addWidget(self._export_current_anniversary_btn, row, 0, 1, 1)
        row += 1
        grid.addWidget(self._export_other_anniversary_btn, row, 0, 1, 1)
        grid.addWidget(self._export_other_anniversary_le, row, 1, 1, 1)

        grid_hbox: QHBoxLayout = QHBoxLayout()
        grid_hbox.addLayout(grid)
        grid_hbox.addStretch()

        right_vbox: QVBoxLayout = QVBoxLayout()
        right_vbox.addLayout(grid_hbox)
        right_vbox.addStretch()

        global_hox: QHBoxLayout = QHBoxLayout()
        global_hox.addWidget(self.member_list)
        global_hox.addLayout(right_vbox)

        self.setLayout(global_hox)

    def set_current_member(self) -> None:
        debug.debug(item=debug_str, keyword="set_current_member", message=f"None Method")
