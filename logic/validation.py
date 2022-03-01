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
    @classmethod
    def add_type(cls, type_name: str, raw_type_id: int) -> None:
        cls.must_str(text=type_name)
        cls.must_positive_int(int_=raw_type_id)

        data = s_h.select_handler.get_all_single_type()
        type_name = type_name.strip().title()
        for _, name, id_, _ in data:
            if type_name == name and id_ == raw_type_id:
                raise e.AlreadyExists()

    @classmethod
    def edit_type(cls, new_id: int, new_name: str) -> None:
        cls.must_str(new_name)
        cls.must_positive_int(new_id)

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

    @classmethod
    def edit_type_activity(cls, id_: int, active: bool) -> None:
        cls.must_positive_int(int_=id_)
        cls.must_bool(bool_=active)

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

    # member nexus
    @classmethod
    def update_member_nexus(cls, data: list, type_: str) -> None:
        cls.must_list(data)
        cls.must_length(4, data)
        ID, type_id, Type, value = data
        cls.must_positive_int(type_id)
        if Type is not None:
            cls.must_str(Type)
        match type_:
            case "phone":
                cls._update_member_nexus_phone(phone=value)
            case "mail":
                cls._update_member_nexus_mail(mail=value)
            case "position":
                cls._update_member_nexus_position(active=value)

    @classmethod
    def _update_member_nexus_phone(cls, phone: str) -> None:
        if phone is not None:
            cls.must_str(phone)

    @classmethod
    def _update_member_nexus_mail(cls, mail: str) -> None:
        if mail is not None:
            cls.must_str(mail)

    @classmethod
    def _update_member_nexus_position(cls, active: bool) -> None:
        if active is not None:
            cls.must_bool(active)

    # global
    @staticmethod
    def must_str(text: str) -> None:
        if not isinstance(text, str) or len(text.strip()) == 0:
            raise e.NoStr(info=text)

    @staticmethod
    def must_bool(bool_: bool) -> None:
        if not isinstance(bool_, bool):
            raise e.NoBool(info=str(bool_))

    @staticmethod
    def must_positive_int(int_: int) -> None:
        if not isinstance(int_, int):
            raise e.NoInt(info=str(int_))
        if int_ <= 0:
            raise e.NoPositiveInt(info=str(int_))

    @staticmethod
    def must_int(int_: int) -> None:
        if not isinstance(int_, int):
            raise e.NoInt(info=str(int_))

    @staticmethod
    def must_dict(dict_: dict) -> None:
        if not isinstance(dict_, dict):
            raise e.NoDict(str(dict_))

    @staticmethod
    def must_list(list_: list) -> None:
        if not isinstance(list_, list):
            raise e.NoList(str(list_))

    @staticmethod
    def must_length(len_: int, data) -> None:
        if not len(data) == len_:
            raise e.WrongLength(str(len_) + "//" + str(data))


def create_validation() -> None:
    global validation
    validation = Validation()
