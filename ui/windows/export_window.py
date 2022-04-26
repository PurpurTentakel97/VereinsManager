# Purpur Tentakel
# 26.04.2022
# VereinsManager / Export Window

from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from ui import window_manager as w_m
from ui.windows.base_window import BaseWindow
from ui.frames.member_export_frame import MemberExportFrame
import debug

debug_str: str = "ExportWindow"


class ExportWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        self._member_frame: MemberExportFrame = MemberExportFrame(window=self)

        self._tabs: QTabWidget = QTabWidget()
        self._tabs.addTab(self._member_frame, "Mitglieder")

    def _create_layout(self) -> None:
        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addWidget(self._tabs)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)

        self.set_widget(widget=widget)
        self.show()

    def _get_current_tab_index(self) -> int:
        return self._tabs.currentIndex()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Exportieren")

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.export_window = None
        event.accept()
