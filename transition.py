# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import global_handler as g_h, select_handler as s_h


# type
def get_raw_types() -> tuple:
    return s_h.select_handler.get_raw_types()


def get_single_type(raw_type_id: int, active: bool = True) -> tuple:
    return s_h.select_handler.get_single_type(raw_type_id=raw_type_id, active=active)
