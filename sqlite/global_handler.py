# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler

from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h, \
    log_handler as l_h
import debug

debug_str: str = "GlobalHandler"

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()

    @staticmethod
    def create_handler() -> None:
        s_h.create_select_handler()
        a_h.create_add_handler()
        u_h.crate_update_handler()
        d_h.create_delete_handler()
        l_h.create_log_handler()


def create_global_handler() -> None:
    global global_handler
    global_handler = GlobalHandler()
