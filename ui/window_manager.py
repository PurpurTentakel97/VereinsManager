# Purpur Tentakel
# 21.01.2022
# VereinsManager / Window Manager

window_manger: "WindowManager"


class WindowManager:
    def __init__(self):
        # Main
        self.main_window = None
        # Type
        self.types_window = None
        # Member
        self.members_window = None
        self.recover_member_window = None

    # Main
    @staticmethod
    def is_valid_main_window() -> bool | str:
        return True

    # Types
    def is_valid_types_window(self) -> bool | str:
        if self.members_window:
            return "Es können eine Typen berabeitet werden, währen das Mitglieder-Fenster geöffnet ist."

        return True

    # Member
    def is_valid_member_window(self, recover_member_window: bool = False) -> bool | str:
        if self.types_window:
            return "Es können eine Mitglieder berabeitet werden, währen das Typ-Fenster geöffnet ist."

        elif self.recover_member_window and not recover_member_window:
            return "Es können eine Mitglieder berabeitet werden, währen das Ehmalige-Mitglieder-Fenster geöffnet ist."

        return True

    def is_valid_recover_member_window(self, member_window: bool = False) -> bool | str:
        if self.members_window and not member_window:
            return "Es können eine Ehmaligen Mitglider berabeitet werden, währen das Mitglieder-Fenster geöffnet ist."

        return True


def create_window_manager() -> None:
    global window_manger
    window_manger = WindowManager()
