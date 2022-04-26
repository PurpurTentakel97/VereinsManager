# Purpur Tentakel
# 26.04.2022
# VereinsManager / Export Window

from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from ui import window_manager as w_m
from ui.windows.base_window import BaseWindow
from ui.frames.member_export_frame import MemberExportFrame


class ExportWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton("Exportieren")
        self._export_btn.clicked.connect(self._export)

        self._member_frame: MemberExportFrame = MemberExportFrame()

        self._tabs: QTabWidget = QTabWidget()
        self._tabs.addTab(self._member_frame, "Mitglieder")

    def _create_layout(self) -> None:
        buttons_hbox: QHBoxLayout = QHBoxLayout()
        buttons_hbox.addStretch()
        buttons_hbox.addWidget(self._export_btn)

        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addWidget(self._tabs)
        global_vbox.addLayout(buttons_hbox)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)

        self.set_widget(widget=widget)
        self.show()

    def _get_current_tab_index(self) -> int:
        return self._tabs.currentIndex()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Exportieren")

    def _export(self) -> None:
        match self._get_current_tab_index():
            case 0:
                print("member +++ TODO +++")

    def closeEvent(self, event) -> None:
        event.ignore()
        w_m.window_manger.export_window = None
        event.accept()
