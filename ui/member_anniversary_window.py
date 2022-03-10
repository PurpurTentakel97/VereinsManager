# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout

from ui.base_window import BaseWindow
from ui import window_manager as w, members_window as m_w
import transition
import debug

debug_str: str = "Member Anniversary Window"


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._get_data()

        self._set_window_information()
        self._set_ui()
        self._set_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _set_ui(self) -> None:
        self._tabs: QTabWidget = QTabWidget()

        self._current_widget: QWidget = QWidget()
        self._tabs.addTab(self._current_widget, "Aktuell")

        self._other_widget: QWidget = QWidget()
        self._tabs.addTab(self._other_widget, "Andere")

    def _set_layout(self) -> None:
        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self._tabs)

        widget: QWidget = QWidget()
        widget.setLayout(hbox)

        self.set_widget(widget)
        self.show()

    def _get_data(self) -> None:
        data = transition.get_anniversary_member_data(type_="current")
        if isinstance(data, str):
            self.set_error_bar(message=data)
        debug.info(item=debug_str, keyword="_get_data", message=f"data 0 {data}")

    def closeEvent(self, event) -> None:
        event.ignore()
        result = w.window_manger.is_valid_member_window(active_member_anniversary_window=True)
        if isinstance(result, str):
            w.window_manger.member_anniversary_window = None
            event.accept()
        elif result:
            w.window_manger.members_window = m_w.MembersWindow()
            w.window_manger.member_anniversary_window = None
            event.accept()
