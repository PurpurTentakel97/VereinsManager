# Purpur Tentakel
# 21.03.2022
# VereinsManager / Global Handler

from logic.handler import member_handler, user_handler
import debug

debug_str: str = "Global Handler"


def delete_inactive_data() -> None:
    member_handler.delete_inactive_member()
    user_handler.delete_inactive_user()
