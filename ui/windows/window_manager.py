# Purpur Tentakel
# 21.01.2022
# VereinsManager / Window Manager

import debug

debug_str: str = "WindowManager"

window_manger: "WindowManager"


class WindowManager:
    def __init__(self):
        # Main
        self.main_window = None
        # Type
        self.types_window = None
        # Member
        self.members_window = None
        self.member_table_window = None
        self.member_anniversary_window = None
        self.member_log_window = None
        # User
        self.user_window = None
        # Organisation
        self.organisation_data_window = None
        # global
        self.recover_window = None

    # Main
    def is_valid_close_main_window(self) -> bool:
        windows: tuple = (
            "member",
            "user",
        )
        valid = True
        for window in windows:
            if self._is_window(window=window):
                valid = False
                break
        return valid

    def is_main_window(self) -> bool:
        if self.main_window:
            return True
        debug.debug(item=debug_str, keyword="is_main_window", message=f"main_window = {self.main_window}")
        return False

    # Types
    def is_valid_types_window(self) -> [bool | str, bool]:
        if self._is_window("type"):
            return "Type Fenster bereits geöffnet.", False
        elif self._is_window("member"):
            return "Es können keine Typen berabeitet werden, währen das Mitglieder-Fenster geöffnet ist.", False

        elif self._is_window("member_table"):
            return "Es können keine Typen berabeitet werden, währen die Mitglieder-Tabellen geöffnet sind.", False

        elif self._is_window("member_anniversary"):
            return "Es können keine Typen berabeitet werden, währen die Mitglieder-Jubiläen geöffnet sind.", False

        return True, True

    # Member
    def is_valid_member_window(self, ignore_recover_window: bool = False,
                               ignore_member_table_window: bool = False,
                               ignore_member_anniversary_window: bool = False,
                               ignore_member_log_window: bool = False) -> [bool | str, bool]:
        if self._is_window("member"):
            return "Mitgliederfenster bereits geöffnet.", False

        elif self._is_window("type"):
            return "Es können keine Mitglieder berabeitet werden, währen das Typ-Fenster geöffnet ist.", False

        elif self._is_window("recover", ignore_recover_window):
            return "Es können keine Mitglieder berabeitet werden, währen das Ehmalige-Mitglieder-Fenster geöffnet ist.", False

        elif self._is_window("member_table", ignore_member_table_window):
            return "Es können keine Mitglieder berabeitet werden, währen die Mitglieder-Tabelle geöffnet ist.", False

        elif self._is_window("member_anniversary", ignore_member_anniversary_window):
            return "Es können keine Mitglieder berabeitet werden, währen die Mitglieder-Jubiläen geöffnet ist.", False

        elif self._is_window("member_log", ignore_member_log_window):
            return "Es können keine Mitglieder berabeitet werden, währen das Mitglieder-Log geöffnet ist.", False

        return True, True

    def is_valid_member_table_window(self, ignore_member_window: bool = False) -> [bool | str, bool]:
        if self._is_window("member_table"):
            return "Mitglieder Tabelle  bereits geöffnet.", False
        elif self._is_window("member", ignore_member_window):
            return "Die Tabelle kann nicht angezeigt werden, während das Mitglieder-Fenster geöffnet ist.", False

        elif self._is_window("type"):
            return "Die Tabelle kann nicht angezeigt werden, während das Typen-Fenster geöffnet ist.", False

        return True, True

    def is_valid_member_anniversary_window(self, ignore_member_window: bool = False) -> [bool | str, bool]:
        if self._is_window("member_anniversary"):
            return "Type Fenster bereits geöffnet.", False
        elif self._is_window("member", ignore_member_window):
            return "Die Tabelle kann nicht angezeigt werden, während das Mitglieder-Fenster geöffnet ist.", False

        elif self.types_window:
            return "Die Tabelle kann nicht angezeigt werden, während das Typen-Fenster geöffnet ist.", False

        return True, True

    def is_valid_member_log_window(self, ignore_member_window: bool = False) -> [bool | str, bool]:
        if self._is_window("member_anniversary"):
            return "Type Fenster bereits geöffnet.", False
        elif self._is_window("member", ignore_member_window):
            return "Das Mitglieder-Log kann nicht angezeigt werden, während das Mitglieder-Fenster geöffnet ist.", False

        elif self.types_window:
            return "Das Mitglieder-Log kann nicht angezeigt werden, während das Typen-Fenster geöffnet ist.", False

        return True, True

    # User
    def is_valid_user_window(self, ignore_recover_window: bool = False) -> [str | bool, bool]:
        if self._is_window("user"):
            return "Benutzer Fenster bereits geöffnet.", False
        elif self._is_window("recover", ignore_recover_window):
            return "Es können keine Benutzer berabeitet werden, währen das Ehmalige-Benutzer-Fenster geöffnet ist.", False
        return True, True

    # Organisation
    def is_valid_organisation_data_window(self) -> [bool | str, bool]:
        if self.organisation_data_window:
            return "Fenster bereits geöffnet", False
        return True, True

    # Global
    def is_valid_recover_window(self, type_: str, ignore_member_window: bool = False,
                                ignore_user_window: bool = False) -> [bool | str, bool]:
        if self._is_window("recover"):
            return "Wiederherstellen Fenster bereits geöffnet.", False
        match type_:
            case "member":
                if self._is_window("member", ignore_member_window):
                    return "Es können keine Ehmaligen Mitglider berabeitet werden, währen das Mitglieder-Fenster geöffnet ist.", False
            case "user":
                if self._is_window("user", ignore_user_window):
                    return "Es können keine Ehmaligen Benutzer berabeitet werden, währen das Benutzer-Fenster geöffnet ist.", False

        return True, True

    # close window
    def close_all_window(self) -> None:
        self.member_table_window.close() if self.member_table_window else None

        self.member_anniversary_window.close() if self.member_anniversary_window else None

        self.recover_window.close() if self.recover_window else None

        self.member_log_window.close() if self.member_log_window else None

        self.members_window.close() if self.members_window else None

        self.types_window.close() if self.types_window else None

        self.user_window.close() if self.user_window else None

        self.organisation_data_window.close() if self.organisation_data_window else None

    # helper
    def _is_window(self, window: str, ignore: bool = False) -> bool:
        dummy_window = False
        match window:
            case "main":
                dummy_window = self.main_window
            case "recover":
                dummy_window = self.recover_window
            case "type":
                dummy_window = self.types_window

            case "member":
                dummy_window = self.members_window
            case "member_table":
                dummy_window = self.member_table_window
            case "member_anniversary":
                dummy_window = self.member_anniversary_window
            case "member_log":
                dummy_window = self.member_log_window

            case "user":
                dummy_window = self.user_window

            case "organisation_data":
                dummy_window = self.organisation_data_window

        if dummy_window:
            return not ignore
        return False


def create_window_manager() -> None:
    global window_manger
    window_manger = WindowManager()
