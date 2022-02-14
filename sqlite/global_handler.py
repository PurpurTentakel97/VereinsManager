# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler

from sqlite import select_handler

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()
        self.select_handler = select_handler.select_handler

    def __str__(self) -> str:
        return "GlobalHandler"

    @staticmethod
    def create_handler() -> None:
        select_handler.create_select_handler()


def create_global_handler() -> None:
    global global_handler
    global_handler = GlobalHandler()
