# Purpur Tentakel
# 18.02.2022
# VereinsManager / Validation

from sqlite import select_handler as s_h
from config import error_code as e

validation: "Validation"


class Validation:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Validation"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> None:
        self.must_str_with_len(text=type_name)
        self.must_id(id_=raw_type_id)

        data = s_h.select_handler.get_all_single_type()
        type_name = type_name.strip().title()
        for _, name, id_, _ in data:
            if type_name == name and id_ == raw_type_id:
                raise e.AlreadyExists()

    def edit_type(self, new_id: int, new_name: str) -> None:
        self.must_str_with_len(new_name)
        self.must_id(new_id)

        data = s_h.select_handler.get_all_single_type()
        exists: bool = False
        for old_id, old_name, *_ in data:
            if new_id == old_id:
                if new_name == old_name:
                    raise e.NoChance(info=new_name)
                exists = True
                break

        if not exists:
            raise e.NotFound(info=new_name)

    def edit_type_activity(self, id_: int, active: bool) -> None:
        self.must_id(id_=id_)
        self.must_bool(bool_=active)

        data = s_h.select_handler.get_all_single_type()
        exists: bool = False
        for old_id, old_name, old_type_id, old_active in data:
            if old_id == id_:
                if old_active != active:
                    raise e.NoChance(info="Type Aktivität")
                exists = True
                break

        if not exists:
            raise e.NotFound(info="Typ Aktivität")

    # member
    @classmethod
    def update_member(cls, data: dict) -> None:
        cls.must_dict(dict_=data)
        keys: list = [
            "first_name",
            "last_name",
            "street",
            "number",
            "city",
            "membership_type",
            "comment_text",
        ]
        for key in keys:
            if data[key] is not None:
                cls.must_str(text=data[key])

        keys: list = [
            "zip_code",
            "birth_date",
            "entry_date",
        ]
        for key in keys:
            if data[key] is not None:
                cls.must_int(int_=data[key])

        if data["special_member"] is not None:
            cls.must_bool(bool_=data["special_member"])

    @staticmethod
    def must_str_with_len(text: str) -> None:
        if not isinstance(text, str) or len(text.strip()) == 0:
            raise e.NoStr(info=text)

    @staticmethod
    def must_str(text: str) -> None:
        if not isinstance(text, str):
            raise e.NoStr(info=text)

    @staticmethod
    def must_bool(bool_: bool) -> None:
        if not isinstance(bool_, bool):
            raise e.NoBool()

    @staticmethod
    def must_id(id_: int) -> None:
        if not isinstance(id_, int) or id_ <= 0:
            raise e.NoId()

    @staticmethod
    def must_int(int_: int) -> None:
        if not isinstance(int_, int):
            raise e.NoInt()

    @staticmethod
    def must_dict(dict_: dict) -> None:
        if not isinstance(dict_, dict):
            raise e.NoDict()


def create_validation() -> None:
    global validation
    validation = Validation()
