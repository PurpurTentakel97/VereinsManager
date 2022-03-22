# Purpur Tentakel
# 18.02.2022
# VereinsManager / Error Code

import debug


class BaseException_(Exception):
    def __init__(self) -> None:
        self.message: str = str()

    def set_message(self, message: str, info) -> None:
        self.message: str = message + "//" + info if info else message


#
class OperationalError(BaseException_):
    def __init__(self) -> None:
        super().__init__()


class LoadingFailed(OperationalError):
    def __init__(self, info: str = "") -> None:
        super().__init__()
        self.set_message(message="Laden Fehlgeschlagen", info=info)


class AddFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.set_message(message="Hinzufügen Fehlgeschlagen", info=info)


class UpdateFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.set_message(message="Update Fehlgeschlagen", info=info)


class ActiveSetFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.set_message(message="Änderung der Aktivität Fehlgeschlagen", info=info)


class DeleteFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.set_message(message="Löschen Fehlgeschlagen", info=info)


class ForeignKeyError(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.set_message(message="Datensatz noch in Benutzung", info=info)


#
class InputError(BaseException_):
    def __init__(self):
        super().__init__()


class NoStr(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Keine Eingabe", info=info)


class NoBool(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Kein Bool-Wert", info=info)


class NoDict(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Kein Dictionary", info=info)


class NoInt(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Keine Ganzzahl", info=info)


class NoPositiveInt(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Keine positive Ganzzahl", info=info)


class NoList(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Keine Liste", info=info)


class WrongLength(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Falsche Länge", info=info)


class NoChance(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Keine Änderung", info=info)


class AlreadyExists(InputError):
    def __init__(self, info: str = ""):
        self.set_message(message="Bereits vorhanden", info=info)


class ToLong(InputError):
    def __init__(self, max_length: int, text):
        if len(text) > 25:
            text = f"{str(text)[:25]}..."

        self.set_message(message=f"Länge von {max_length} Zeichen überschritten",
                         info=f"{str(text)} ({str(len(text))} Zeichen")


#
class PasswordError(BaseException_):
    def __init__(self):
        super().__init__()


class PasswordHasSpace(PasswordError):
    def __init__(self):
        self.set_message(message="Passwort enthält Leerzeichen", info=None)


class VeryLowPassword(PasswordError):
    def __init__(self):
        self.set_message(message="Dein Passwort ist sehr unsicher", info=None)


class LowPassword(PasswordError):
    def __init__(self):
        self.set_message(message="Dein Passwort ist unsicher", info=None)


class PasswordToShort(PasswordError):
    def __init__(self):
        self.set_message(message="Dein Passwort ist zu kurz", info=None)


class DifferentPassword(PasswordError):
    def __init__(self):
        self.set_message(message="Deine Passwörter stimmen nicht überein", info=None)


#
class UserError(BaseException_):
    def __init__(self):
        super().__init__()


class CurrentUserException(UserError):
    def __init__(self, info: str = ""):
        self.set_message(message="Dieser Benutzer kann nicht bearbeitet werden", info=info)


class DefaultUserException(UserError):
    def __init__(self, info: str = ""):
        self.set_message(message="Default Benutzer kann nicht bearbeitet werden", info=info)


#
class GeneralError(BaseException_):
    def __init__(self):
        super().__init__()


class NotFound(GeneralError):
    def __init__(self, info: str = ""):
        self.set_message(message="Nicht gefunden", info=info)
