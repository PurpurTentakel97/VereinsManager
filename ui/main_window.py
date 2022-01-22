# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main Window


from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget
from ui.base_window import BaseWindow

window: "MainWindow" or None = None


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self._set_layout()

    def _set_ui(self) -> None:
        self._members_btn: QPushButton = QPushButton()
        self._members_btn.setText("Mitglieder")
        self._members_btn.clicked.connect(self._open_members)

        self._performance_btn: QPushButton = QPushButton()
        self._performance_btn.setText("Auftritte")
        self._performance_btn.clicked.connect(self._open_performances)

        self._my_job_btn: QPushButton = QPushButton()
        self._my_job_btn.setText("Meine Aufgaben")
        self._my_job_btn.clicked.connect(self._open_my_jobs)

        self._job_btn: QPushButton = QPushButton()
        self._job_btn.setText("Aufgaben")
        self._job_btn.clicked.connect(self._open_jobs)

    def _set_layout(self) -> None:
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._members_btn, 0, 0)
        grid.addWidget(self._performance_btn, 1, 0)
        grid.addWidget(self._my_job_btn, 0, 1)
        grid.addWidget(self._job_btn, 1, 1)

        widget: QWidget = QWidget()
        widget.setLayout(grid)

        self.set_widget(widget)
        self.show()

    def _open_members(self) -> None:
        print("open members")

    def _open_my_jobs(self) -> None:
        print("open my jobs")

    def _open_jobs(self) -> None:
        print("open jobs")

    def _open_performances(self) -> None:
        print("open performances")


def create_main_window() -> None:
    global window
    window = MainWindow()
