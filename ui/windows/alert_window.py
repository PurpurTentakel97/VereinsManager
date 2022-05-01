# Purpur Tentakel
# 21.01.2022
# VereinsManager / Alert Window

from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QWidget

from ui.base_window import BaseWindow
from ui.frames.current_anniversary_frame import CurrentAnniversaryFrame

debug_str: str = "AlertWindow"

alert_window: "AlertWindow"


class AlertWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self._set_window_information()
        self._create_ui()
        self._create_layout()

    def _create_ui(self) -> None:
        # Headline
        headline_font = self.font()
        headline_font.setPointSize(30)
        headline_font.setUnderline(True)
        self._headline_lb: QLabel = QLabel()
        self._headline_lb.setFont(headline_font)
        self._headline_lb.setText("Aktuelles")

        # Anniversary
        anniversary_font = self.font()
        anniversary_font.setPointSize(20)
        self.anniversary_lb: QLabel = QLabel()
        self.anniversary_lb.setFont(anniversary_font)
        self.anniversary_lb.setText("Jubiläen:")
        self.anniversaries: CurrentAnniversaryFrame = CurrentAnniversaryFrame(self)

    def _create_layout(self) -> None:
        # Headline
        headline_hbox: QHBoxLayout = QHBoxLayout()
        headline_hbox.addStretch()
        headline_hbox.addWidget(self._headline_lb)
        headline_hbox.addStretch()

        # Anniversary
        anniversary_lb_hbox: QHBoxLayout = QHBoxLayout()
        anniversary_lb_hbox.addStretch()
        anniversary_lb_hbox.addWidget(self.anniversary_lb)
        anniversary_lb_hbox.addStretch()

        anniversary_vbox: QVBoxLayout = QVBoxLayout()
        anniversary_vbox.addLayout(anniversary_lb_hbox)
        anniversary_vbox.addWidget(self.anniversaries)

        # Grid
        column: int = 0
        row: int = 0
        grid: QGridLayout = QGridLayout()
        grid.addLayout(anniversary_vbox, row, column)

        # Global
        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(headline_hbox)
        global_vbox.addSpacing(30)
        global_vbox.addLayout(grid)

        widget: QWidget = QWidget()
        widget.setLayout(global_vbox)
        self.set_widget(widget=widget)
        self.show()
        self.resize(750, 400)

    def _set_window_information(self) -> None:
        self.setWindowTitle("Aktuelles")


def create() -> None:
    global alert_window
    alert_window = AlertWindow()
