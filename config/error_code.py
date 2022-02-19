# Purpur Tentakel
# 18.02.2022
# VereinsManager / Error Code


# Operational Error
class LoadingFailed(Exception):
    def __init__(self, info: str = ""):
        str_ = "Laden Fehlgeschlagen"
        self.message: str = str_ + "//" + info if info else str_


class AddFailed(Exception):
    def __init__(self, info: str = ""):
        str_ = "Hinzufügen Fehlgeschlagen"
        self.message: str = str_ + "//" + info if info else str_


class UpdateFailed(Exception):
    def __init__(self, info: str = ""):
        str_ = "Update Fehlgeschlagen"
        self.message: str = str_ + "//" + info if info else str_


class ActiveSetFailed(Exception):
    def __init__(self, info: str = ""):
        str_ = "Änderung der Aktivität Fehlgeschlagen"
        self.message: str = str_ + "//" + info if info else str_


class DeleteFailed(Exception):
    def __init__(self, info: str = ""):
        str_ = "Löschen Fehlgeschlagen"
        self.message: str = str_ + "//" + info if info else str_


# Database
class ForeignKeyError(Exception):
    def __init__(self, info: str = ""):
        str_ = "Datensatz noch in Benutzung"
        self.message: str = str_ + "//" + info if info else str_


# Input Error
class NoInput(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Eingabe"
        self.message: str = str_ + "//" + info if info else str_


class NoBool(Exception):
    def __init__(self, info: str = ""):
        str_ = "Kein Bool-Wert"
        self.message: str = str_ + "//" + info if info else str_


class NoId(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine ID"
        self.message: str = str_ + "//" + info if info else str_


class NoChance(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Änderung"
        self.message: str = str_ + "//" + info if info else str_


class AlreadyExists(Exception):
    def __init__(self, info: str = ""):
        str_ = "Bereits vorhanden"
        self.message: str = str_ + "//" + info if info else str_


# General
class NotFound(Exception):
    def __init__(self, info: str = ""):
        str_ = "Nicht gefunden"
        self.message: str = str_ + "//" + info if info else str_
