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
        self.member_table_window = None
        self.member_anniversary_window = None
        # User
        self.user_window = None

    # Main
    @staticmethod
    def is_valid_main_window() -> bool | str:
        return True

    def is_valid_close_main_window(self) -> bool:
        if self.members_window:
            return False
        else:
            return True

    # Types
    def is_valid_types_window(self) -> bool | str:
        if self.members_window:
            return "Es können keine Typen berabeitet werden, währen das Mitglieder-Fenster geöffnet ist."

        elif self.member_table_window:
            return "Es können keine Typen berabeitet werden, währen die Mitglieder-Tabelle geöffnet ist."

        elif self.member_anniversary_window:
            return "Es können keine Typen berabeitet werden, währen die Mitglieder-Jubiläen geöffnet ist."

        return True

    # Member
    def is_valid_member_window(self, active_recover_member_window: bool = False,
                               active_member_table_window: bool = False,
                               active_member_anniversary_window: bool = False) -> bool | str:
        if self.types_window:
            return "Es können keine Mitglieder berabeitet werden, währen das Typ-Fenster geöffnet ist."

        elif self.recover_member_window and not active_recover_member_window:
            return "Es können keine Mitglieder berabeitet werden, währen das Ehmalige-Mitglieder-Fenster geöffnet ist."

        elif self.member_table_window and not active_member_table_window:
            return "Es können keine Mitglieder berabeitet werden, währen die Mitglieder-Tabelle geöffnet ist."

        elif self.member_anniversary_window and not active_member_anniversary_window:
            return "Es können keine Mitglieder berabeitet werden, währen die Mitglieder-Jubiläen geöffnet ist."

        return True

    def is_valid_recover_member_window(self, active_member_window: bool = False) -> bool | str:
        if self.members_window and not active_member_window:
            return "Es können keine Ehmaligen Mitglider berabeitet werden, währen das Mitglieder-Fenster geöffnet ist."

        elif self.member_table_window:
            return "Es können keine Ehmaligen Mitglider berabeitet werden, währen die Mitglieder-Tabelle geöffnet ist."

        return True

    def is_valid_member_table_window(self, active_member_window: bool = False) -> bool | str:
        if self.members_window and not active_member_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Mitglieder-Fenster geöffnet ist."

        elif self.recover_member_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Ehmalige-Mitglieder-Fenster geöffnet ist."

        elif self.types_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Typen-Fenster geöffnet ist."

        return True

    def is_valid_member_anniversary_window(self, active_member_window: bool = False) -> bool | str:
        if self.members_window and not active_member_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Mitglieder-Fenster geöffnet ist."

        elif self.recover_member_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Ehmalige-Mitglieder-Fenster geöffnet ist."

        elif self.types_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Typen-Fenster geöffnet ist."

        return True

    # User
    @staticmethod
    def is_valid_user_window() -> bool:
        return True

    # close window

    def close_all_window(self) -> None:
        self.member_table_window.close() if self.member_table_window else None
        self.member_table_window = None

        self.member_anniversary_window.close() if self.member_anniversary_window else None
        self.member_anniversary_window = None

        self.recover_member_window.close() if self.recover_member_window else None
        self.recover_member_window = None

        self.members_window.close() if self.members_window else None
        self.members_window = None

        self.types_window.close() if self.types_window else None
        self.types_window = None

        self.user_window.close() if self.user_window else None
        self.user_window = None


def create_window_manager() -> None:
    global window_manger
    window_manger = WindowManager()
