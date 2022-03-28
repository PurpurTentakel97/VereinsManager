# Purpur Tentakel
# 18.02.2022
# VereinsManager / Validation

import math

from sqlite import select_handler as s_h
from config import exception_sheet as e, config_sheet as c

validation: "Validation"


class Validation:
    def __init__(self) -> None:
        pass

    # type
    @classmethod
    def add_type(cls, type_name: str, raw_type_id: int) -> None:
        cls.must_str(str_=type_name)
        cls.must_positive_int(int_=raw_type_id, max_length=None)

        data = s_h.select_handler.get_all_single_type()
        type_name = type_name.strip().title()
        for _, name, id_, _ in data:
            if type_name == name and id_ == raw_type_id:
                raise e.AlreadyExists()

    @classmethod
    def update_type(cls, ID: int, new_name: str) -> None:
        cls.must_str(new_name)
        cls.must_positive_int(ID, max_length=None)

        data = s_h.select_handler.get_all_single_type()
        exists: bool = False
        for old_id, old_name, *_ in data:
            if ID == old_id:
                if new_name == old_name:
                    raise e.NoChance(info=new_name)
                exists = True
                break

        if not exists:
            raise e.NotFound(info=new_name)

    @classmethod
    def update_type_activity(cls, ID: int, active: bool) -> None:
        cls.must_positive_int(int_=ID, max_length=None)
        cls.must_bool(bool_=active)

        data = s_h.select_handler.get_all_single_type()
        exists: bool = False
        for old_id, old_name, old_type_id, old_active in data:
            if old_id == ID:
                if old_active == active:
                    raise e.NoChance(info="Type Aktivität")
                exists = True
                break

        if not exists:
            raise e.NotFound(info="Typ Aktivität")

    # member
    @classmethod
    def update_member(cls, data: dict) -> None:
        cls.must_dict(dict_=data)
        cls._must_multiple_str_in_dict([
            "first_name",
            "last_name",
            "street",
            "number",
            "city",
            "maps",
            "membership_type",
            "zip_code",
        ], data)

        if data["comment_text"] is not None:
            cls.must_str(str_=data["comment_text"], length=2000)

        keys: list = [
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
        cls.must_positive_int(type_id, max_length=None)

        if ID is not None:
            cls.must_positive_int(ID, max_length=None)

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

    # User
    @classmethod
    def save_update_user(cls, data: dict) -> None:
        cls.must_dict(dict_=data)
        if data["ID"] is not None:
            cls.must_positive_int(int_=data["ID"], max_length=None)
            cls.must_current_user(ID=data["ID"], same=True)
            cls.must_default_user(ID=data["ID"], same=False)

        if data["ID"] is None or data["password_1"] is not None:
            cls.must_password(password_1=data["password_1"], password_2=data["password_2"])

        cls._must_multiple_str_in_dict([
            "firstname",
            "lastname",
            "street",
            "number",
            "city",
            "phone",
            "mail",
            "position",
            "zip_code",
        ], data)

    @staticmethod
    def must_current_user(ID: int, same: bool) -> None:
        if (ID == c.config.user_id) != same:
            raise e.CurrentUserException()

    @staticmethod
    def must_default_user(ID: int, same: bool) -> None:
        if (ID == c.config.default_user_id["default"]) != same:
            raise e.DefaultUserException()

    # global
    @staticmethod
    def must_str(str_: str, length: int | None = 50) -> None:
        if not isinstance(str_, str) or len(str_.strip()) == 0:
            raise e.NoStr(info=str_)
        if length is not None:
            if len(str_) > length:
                raise e.ToLong(max_length=length, text=str_)

    @classmethod
    def _must_multiple_str_in_dict(cls, keys: list, data: dict) -> None:
        for key in keys:
            entry = data[key]
            if entry is not None:
                cls.must_str(str_=entry)

    @staticmethod
    def must_bool(bool_: bool) -> None:
        if not isinstance(bool_, bool):
            raise e.NoBool(info=str(bool_))

    @staticmethod
    def must_positive_int(int_: int, max_length: int | None = 15) -> None:
        if not isinstance(int_, int):
            raise e.NoInt(info=str(int_))
        if int_ <= 0:
            raise e.NoPositiveInt(info=str(int_))
        if max_length is not None and len(str(int_)) > max_length:
            raise e.ToLong(max_length=max_length, text=int_)

    @staticmethod
    def must_int(int_: int, max_length: int | None = 15) -> None:
        if not isinstance(int_, int):
            raise e.NoInt(info=str(int_))
        if int_ is not None and len(str(int_)) > max_length:
            raise e.ToLong(max_length=max_length, text=int_)

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

    @classmethod
    def must_password(cls, password_1: str, password_2: str) -> None:
        if not isinstance(password_1, str) or len(password_1.strip()) == 0:
            raise e.NoPassword()

        if password_1 != password_2:
            raise e.DifferentPassword()

        if len(password_1) < 8:
            raise e.PasswordToShort()

        if " " in password_1:
            raise e.PasswordHasSpace()

        count = cls._get_count_for_password(password_1)
        if count <= 0:
            raise e.VeryLowPassword()
        bits = math.log(count ** len(password_1), 2)

        if bits < 20:
            raise e.VeryLowPassword()
        elif bits < 40:
            raise e.LowPassword()

    @classmethod
    def _get_count_for_password(cls, password_1):
        digit: int = 0
        capital_letter: int = 0
        small_letter: int = 0
        special_character: int = 0
        count: int = 0
        characters: list = list()

        for character in password_1:
            if character.islower():
                small_letter = 26
            elif character.isupper():
                capital_letter = 26
            elif character.isdigit():
                digit = 10
            elif character.isprintable():
                special_character = 43
            if character in characters:
                count -= 1
            characters.append(character)

        count += (digit + capital_letter + small_letter + special_character)
        return count


def create_validation() -> None:
    global validation
    validation = Validation()
