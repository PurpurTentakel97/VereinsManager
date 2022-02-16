# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import global_handler as g_h, select_handler as s_h


# type
def get_raw_types() -> tuple:
    return s_h.select_handler.get_raw_types()
