# Purpur Tentakel
# 18.02.2022
# VereinsManager / Validation

from sqlite import select_handler as s_h
from config.error_code import ErrorCode

validation: "Validation"


class Validation:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Validation"

    def add_type(self, type_name: str, raw_type_id: int) -> ErrorCode:
        if not self._is_str(text=type_name):
            return ErrorCode.NO_INPUT
        if not self._is_id(id_=raw_type_id):
            return ErrorCode.NO_ID

        error_code, data = s_h.select_handler.get_all_single_type()
        type_name = type_name.strip().title()
        if error_code == ErrorCode.LOAD_S:
            for _, name, id_, _ in data:
                if type_name == name and id_ == raw_type_id:
                    return ErrorCode.ALREADY_EXISTS_E
            return ErrorCode.OK_S

        else:
            return error_code

    @staticmethod
    def _is_str(text: str) -> bool:
        return isinstance(text, str) and len(text.strip()) > 0

    @staticmethod
    def _is_id(id_: int) -> bool:
        return isinstance(id_, int) and id_ > 0


def create_validation() -> None:
    global validation
    validation = Validation()
