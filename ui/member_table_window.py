# Purpur Tentakel
# 06.03.2022
# VereinsManager / Member Table Window

from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QWidget

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w


class MemberTableWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._set_window_information()
        self._set_ui()
        self._set_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Mitglieder Tabelle - Vereinsmanager")

    def _set_ui(self) -> None:
        self.tabs: QTabWidget = QTabWidget()

    def _set_layout(self) -> None:
        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self.tabs)

        widget: QWidget = QWidget()
        widget.setLayout(hbox)
        self.set_widget(widget=widget)

        self.show()

    def closeEvent(self, event) -> None:
        event.ignore()
        result = w.window_manger.is_valid_member_window(active_member_table_window=True)
        if isinstance(result,str):
            w.window_manger.member_table_window = None
            event.accept()
        elif result:
            w.window_manger.members_window = m_w.MembersWindow()
            w.window_manger.member_table_window = None
            event.accept()

