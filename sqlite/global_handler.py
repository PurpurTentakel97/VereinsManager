# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler

from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()

    def __str__(self) -> str:
        return "GlobalHandler"

    @staticmethod
    def create_handler() -> None:
        s_h.create_select_handler()
        a_h.create_add_handler()
        u_h.crate_update_handler()
        d_h.create_delete_handler()

    @staticmethod
    def get_member_data(id_: int, active: bool = True) -> dict | str:
        member_data: dict = s_h.select_handler.get_member_data_by_id(id_=id_, active=active)
        if isinstance(member_data, str):
            return member_data
        data: dict = {
            "member_data": member_data,
        }

        return data


def create_global_handler() -> None:
    global global_handler
    global_handler = GlobalHandler()
