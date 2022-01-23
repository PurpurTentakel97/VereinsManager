# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main Window


from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget
from ui.base_window import BaseWindow
from ui import members_window

main_window_: "MainWindow" or None = None


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self._set_ui()
        self._set_layout()

    def _set_ui(self) -> None:
        self._members_btn: QPushButton = QPushButton()
        self._members_btn.setText("Mitglieder")
        self._members_btn.clicked.connect(self._open_members)

        self._old_members_btn: QPushButton = QPushButton()
        self._old_members_btn.setText("Ehmalige Mitglieder")
        self._old_members_btn.clicked.connect(self._open_old_members)

        self._performance_btn: QPushButton = QPushButton()
        self._performance_btn.setText("Auftritte")
        self._performance_btn.clicked.connect(self._open_performances)

        self._my_job_btn: QPushButton = QPushButton()
        self._my_job_btn.setText("Meine Aufgaben")
        self._my_job_btn.clicked.connect(self._open_my_jobs)

        self._job_btn: QPushButton = QPushButton()
        self._job_btn.setText("Aufgaben")
        self._job_btn.clicked.connect(self._open_jobs)

        self._edit_types_btn: QPushButton = QPushButton()
        self._edit_types_btn.setText("Typen bearbeiten")
        self._edit_types_btn.clicked.connect(self._open_edit_types)

    def _set_layout(self) -> None:
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self._members_btn, 0, 0)
        grid.addWidget(self._old_members_btn, 0, 1)
        grid.addWidget(self._my_job_btn, 1, 0)
        grid.addWidget(self._job_btn, 1, 1)
        grid.addWidget(self._performance_btn, 2, 0)
        grid.addWidget(self._edit_types_btn, 2, 1)

        widget: QWidget = QWidget()
        widget.setLayout(grid)

        self.set_widget(widget)
        self.show()

    @staticmethod
    def _open_members() -> None:
        members_window.members_window_ = members_window.MembersWindow()

    def _open_old_members(self) -> None:
        print("open old members")

    def _open_my_jobs(self) -> None:
        print("open my jobs")

    def _open_jobs(self) -> None:
        print("open jobs")

    def _open_performances(self) -> None:
        print("open performances")

    def _open_edit_types(self) -> None:
        print("type edit opened")


def create_main_window() -> None:
    global main_window_
    main_window_ = MainWindow()
