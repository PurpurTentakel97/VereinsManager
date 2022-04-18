# Purpur Tentakel
# 16.03.2022
# VereinsManager / Hasher

import bcrypt

from config import config_sheet as c
import debug

debug_str: str = "Hasher"


def hash_password(password: str) -> bytes:
    result: bytes = bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt(rounds=c.config.constant['hash_rounds']))
    return result


def compare_password(password: str, hashed: bytes) -> bool:
    if isinstance(hashed, str):
        hashed = bytes(hashed, "UTF-8")
    return bcrypt.checkpw(bytes(password, "UTF-8"), hashed)
