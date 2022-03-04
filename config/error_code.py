# Purpur Tentakel
# 18.02.2022
# VereinsManager / Error Code

import debug


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
class NoStr(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Eingabe"
        self.message: str = str_ + "//" + info if info else str_


class NoBool(Exception):
    def __init__(self, info: str = ""):
        str_ = "Kein Bool-Wert"
        self.message: str = str_ + "//" + info if info else str_


class NoDict(Exception):
    def __init__(self, info: str = ""):
        str_ = "Kein Dictionary"
        self.message: str = str_ + "//" + info if info else str_


class NoInt(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Ganzzahl"
        self.message: str = str_ + "//" + info if info else str_


class NoPositiveInt(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine positive Ganzzahl"
        self.message: str = str_ + "//" + info if info else str_


class NoList(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Liste"
        self.message: str = str_ + "//" + info if info else str_


class WrongLength(Exception):
    def __init__(self, info: str = ""):
        str_ = "Falsche Länge"
        self.message: str = str_ + "//" + info if info else str_


class NoChance(Exception):
    def __init__(self, info: str = ""):
        str_ = "Keine Änderung"
        self.message: str = str_ + "//" + info if info else str_


class AlreadyExists(Exception):
    def __init__(self, info: str = ""):
        str_ = "Bereits vorhanden"
        self.message: str = str_ + "//" + info if info else str_


class ToLong(Exception):
    def __init__(self, max_length: int, text):
        text = str(text)
        if len(text) > 15:
            text = f"{text[:15]}..."
        self.message: str = f"Länge von {max_length} Zeichen überschritten // {text}"


# General
class NotFound(Exception):
    def __init__(self, info: str = ""):
        str_ = "Nicht gefunden"
        self.message: str = str_ + "//" + info if info else str_
