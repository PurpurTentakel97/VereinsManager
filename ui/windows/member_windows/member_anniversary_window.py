# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from ui.windows.base_window import BaseWindow
from ui import window_manager as w, export_manager
from ui.windows.member_windows import members_window
from ui.frames.other_anniversary_frame import OtherAnniversaryFrame
from ui.frames.current_anniversary_frame import CurrentAnniversaryFrame

debug_str: str = "Member Anniversary Window"


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._current_frame: CurrentAnniversaryFrame = CurrentAnniversaryFrame(self)
        self._other_frame: OtherAnniversaryFrame = OtherAnniversaryFrame(self)

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)

        self._tabs: QTabWidget = QTabWidget()
        self._tabs.addTab(self._current_frame, "Aktuell")
        self._tabs.addTab(self._other_frame, "Andere")

    def _create_layout(self) -> None:

        # global widget
        global_h_box: QHBoxLayout = QHBoxLayout()
        global_h_box.addStretch()
        global_h_box.addWidget(self._export_btn)

        global_v_box: QVBoxLayout = QVBoxLayout()
        global_v_box.addLayout(global_h_box)
        global_v_box.addWidget(self._tabs)

        widget: QWidget = QWidget()
        widget.setLayout(global_v_box)

        self.set_widget(widget)
        self.show()
        self.resize(700, 500)

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _export(self) -> None:
        message, valid = export_manager.export_member_anniversary(index=self._tabs.currentIndex(),
                                                                  year=self._other_frame.other_year)

        if not valid:
            self.set_error_bar(message=message)
            return

        self.set_info_bar(message=message)

    def closeEvent(self, event) -> None:
        event.ignore()
        result, valid = w.window_manger.is_valid_member_window(ignore_member_anniversary_window=True)
        if not valid:
            w.window_manger.member_anniversary_window = None
            event.accept()
            return

        w.window_manger.members_window = members_window.MembersWindow()
        w.window_manger.member_anniversary_window = None
        event.accept()
