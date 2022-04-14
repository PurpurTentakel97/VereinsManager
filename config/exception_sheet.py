# Purpur Tentakel
# 18.02.2022
# VereinsManager / Exception

# 0
class BaseException_(Exception):
    def __init__(self):
        self.error_code: str = "0"
        self.message: str = str()

    def set_message(self, message: str, info) -> None:
        self.message: str = f"{self.error_code} //  {message} // {info}" if info else f"{self.error_code} // {message}"


# 100
class OperationalError(BaseException_):
    def __init__(self) -> None:
        super().__init__()
        self.error_code: str = "100"


class LoadingFailed(OperationalError):
    def __init__(self, info: str = "") -> None:
        super().__init__()
        self.error_code: str = "101"
        self.set_message(message="Laden Fehlgeschlagen", info=info)


class AddFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "102"
        self.set_message(message="Hinzufügen Fehlgeschlagen", info=info)


class UpdateFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "103"
        self.set_message(message="Update Fehlgeschlagen", info=info)


class ActiveSetFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "104"
        self.set_message(message="Änderung der Aktivität Fehlgeschlagen", info=info)


class DeleteFailed(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "105"
        self.set_message(message="Löschen Fehlgeschlagen", info=info)


class ForeignKeyError(OperationalError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "106"
        self.set_message(message="Datensatz noch in Benutzung", info=info)


# 200
class InputError(BaseException_):
    def __init__(self):
        super().__init__()
        self.error_code: str = "200"


class NoStr(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "201"
        self.set_message(message="Keine Eingabe", info=info)


class NoMembership(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "202"
        self.set_message(message="Keine Mitgliedsart vorhanden", info=info)


class NoBool(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "203"
        self.set_message(message="Kein Bool-Wert", info=info)


class NoDict(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "204"
        self.set_message(message="Kein Dictionary", info=info)


class NoInt(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "205"
        self.set_message(message="Keine Ganzzahl", info=info)


class NoPositiveInt(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "206"
        self.set_message(message="Keine positive Ganzzahl", info=info)


class NoList(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "207"
        self.set_message(message="Keine Liste", info=info)


class WrongLength(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "208"
        self.set_message(message="Falsche Länge", info=info)


class NoChance(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "209"
        self.set_message(message="Keine Änderung", info=info)


class AlreadyExists(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "210"
        self.set_message(message="Bereits vorhanden", info=info)


class ToLong(InputError):
    def __init__(self, max_length: int, text):
        super().__init__()
        self.error_code: str = "210"
        if len(str(text)) > 25:
            text = f"{str(text)[:25]}..."

        self.set_message(message=f"Länge von {max_length} Zeichen überschritten",
                         info=f"{str(text)} ({str(len(str(text)))} Zeichen)")


class WrongLetterType(InputError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "211"

        self.set_message(message=f"Invalide Art des Schreibens",
                         info=info)


# 300
class PasswordError(BaseException_):
    def __init__(self):
        super().__init__()
        self.error_code: str = "300"


class PasswordHasSpace(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "301"
        self.set_message(message="Passwort enthält Leerzeichen", info=None)


class VeryLowPassword(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "302"
        self.set_message(message="Dein Passwort ist sehr unsicher", info=None)


class LowPassword(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "303"
        self.set_message(message="Dein Passwort ist unsicher", info=None)


class PasswordToShort(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "304"
        self.set_message(message="Dein Passwort ist zu kurz", info=None)


class NoPassword(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "305"
        self.set_message(message="Kein Passwort eingegeben", info=None)


class DifferentPassword(PasswordError):
    def __init__(self):
        super().__init__()
        self.error_code: str = "306"
        self.set_message(message="Deine Passwörter stimmen nicht überein", info=None)


# 400
class UserError(BaseException_):
    def __init__(self):
        super().__init__()
        self.error_code: str = "400"


class CurrentUserException(UserError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "401"
        self.set_message(message="Dieser Benutzer kann nicht bearbeitet werden", info=info)


class DefaultUserException(UserError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "402"
        self.set_message(message="Default Benutzer kann nicht bearbeitet werden", info=info)


# 900
class GeneralError(BaseException_):
    def __init__(self):
        super().__init__()
        self.error_code: str = "900"


class NotFound(GeneralError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "901"
        self.set_message(message="Nicht gefunden", info=info)


class CaseException(GeneralError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "902"
        self.set_message(message="Falscher Typ", info=info)


class InvalidFormat(GeneralError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "903"
        self.set_message(message="Falsches Format", info=info)


class PermissionException(GeneralError):
    def __init__(self, info: str = ""):
        super().__init__()
        self.error_code: str = "904"
        self.set_message(message="Dateizugriff verweigert", info=info)
