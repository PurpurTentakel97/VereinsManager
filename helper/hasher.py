# Purpur Tentakel
# 16.03.2022
# VereinsManager / Hasher

import bcrypt

from config import config_sheet as c


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(bytes(password, "UTF-8"), bcrypt.gensalt(rounds=c.config.hash_round))


def compare_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(bytes(password, "UTF-8"), hashed)
