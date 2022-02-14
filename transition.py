# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import global_handler, select_handler

g_h = global_handler.global_handler
s_h = select_handler.select_handler


# type
def get_types_of_member() -> tuple:
    return s_h.get_types_of_member()
