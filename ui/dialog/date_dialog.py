# Purpur Tentakel
# 24.03.2022
# VereinsManager / Date Input Dialog


from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QDateEdit, QVBoxLayout, QLabel


class DateInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Log Date")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Wähle das Log datum oder klicke Cancel")
        self.layout.addWidget(message)
        self.layout.addWidget(self.date)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_date(self) -> None:
        return self.date.date()
