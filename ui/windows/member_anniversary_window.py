# Purpur Tentakel
# 21.01.2022
# VereinsManager / Member Anniversary Window

from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog

from ui.windows.base_window import BaseWindow
from ui.windows import members_window as m_w, window_manager as w
from config import config_sheet as c
from ui.frames.current_anniversary_frame import CurrentAnniversaryFrame
from ui.frames.other_anniversary_frame import OtherAnniversaryFrame
import transition

debug_str: str = "Member Anniversary Window"


class MemberAnniversaryWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self._current_frame: CurrentAnniversaryFrame = CurrentAnniversaryFrame(self)
        self._other_frame: OtherAnniversaryFrame = OtherAnniversaryFrame(self)

        self._set_window_information()
        self._set_ui()
        self._set_layout()

    def _set_window_information(self) -> None:
        self.setWindowTitle("Jubiläen")

    def _set_ui(self) -> None:
        self._export_btn: QPushButton = QPushButton()
        self._export_btn.setText("Exportieren")
        self._export_btn.clicked.connect(self._export)

        self._tabs: QTabWidget = QTabWidget()
        self._tabs.addTab(self._current_frame, "Aktuell")
        self._tabs.addTab(self._other_frame, "Andere")

    def _set_layout(self) -> None:

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

    def _export(self) -> None:
        transition.create_default_dir("export")
        file, check = QFileDialog.getSaveFileName(None, "Mitglieder PDF exportieren",
                                                  f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.export_dir}/{c.config.member_dir}/Geburtstage-Jubilaen.pdf",
                                                  "PDF (*.pdf);;All Files (*)")
        if not check:
            self.set_info_bar(message="Export abgebrochen")
            return
        match self._tabs.currentIndex():
            case 0:
                transition.get_member_anniversary_pdf(path=file)
            case 1:
                transition.get_member_anniversary_pdf(path=file, year=self._other_frame.other_year)

        if self._open_permission():
            transition.open_latest_export()

        self.set_info_bar(message="Export abgeschlossen")

    def closeEvent(self, event) -> None:
        event.ignore()
        result, valid = w.window_manger.is_valid_member_window(active_member_anniversary_window=True)
        if not valid:
            w.window_manger.member_anniversary_window = None
            event.accept()
            return

        w.window_manger.members_window = m_w.MembersWindow()
        w.window_manger.member_anniversary_window = None
        event.accept()
