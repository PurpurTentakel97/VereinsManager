# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler

from logic.sqlite import select_handler, delete_handler, log_handler, update_handler, statistics_handler,add_handler

debug_str: str = "GlobalHandler"

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()

    @staticmethod
    def create_handler() -> None:
        select_handler.create()
        add_handler.create()
        update_handler.crate()
        delete_handler.create()
        log_handler.create()
        statistics_handler.create()


def create() -> None:
    global global_handler
    global_handler = GlobalHandler()
