# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import select_handler as s_h, add_handler as a_s


# type
def get_raw_types() -> tuple:
    return s_h.select_handler.get_raw_types()


def get_single_type(raw_type_id: int, active: bool = True) -> tuple:
    return s_h.select_handler.get_single_type(raw_type_id=raw_type_id, active=active)


def add_type(type_name: str, raw_type_id: int) -> int:
    return a_s.add_handler.add_type(type_name=type_name, raw_type_id=raw_type_id)
