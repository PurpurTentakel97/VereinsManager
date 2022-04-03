# Purpur Tentakel
# 31.03.2022
# VereinsManager / Test Helper

from random import randint
import string
import random
import shutil

from config import config_sheet as c
from sqlite import select_handler, database


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def generate_password() -> str:
    letters: list = list(string.ascii_letters)
    random.shuffle(letters)

    digits: list = list(string.digits)
    random.shuffle(digits)

    special_characters: list = ["!@#$%^&*()"]
    random.shuffle(special_characters)

    password: list = list()
    password.extend([x for x in letters[:5]])
    password.extend([x for x in digits[:3]])
    password.extend([x for x in special_characters[:2]])
    random.shuffle(password)

    return "".join(password)


def _generate_config() -> None:
    c.create_config()


def generate_temp_database():
    _generate_config()
    c.config.save_dir = "temp_save_dir"
    c.config.organisation_dir = "temp_organisation_dir"
    c.config.database_name = "unit_test_database"
    database.crate_database()


def add_generic_type() -> None:
    database.database.cursor.execute("""INSERT INTO type (name,type_id) VALUES (?,?);""", ("type_1".title(), 1))
    database.database.cursor.execute("""INSERT INTO type (name,type_id) VALUES (?,?);""", ("type_2".title(), 2))
    database.database.connection.commit()


def add_user_ids_in_config() -> None:
    c.create_config()
    c.config.user_id = 2


def generate_select_handler() -> None:
    select_handler.create_select_handler()


def drop_select_handler() -> None:
    del select_handler.select_handler


def delete_temp_database():
    database.database.drop_connection()
    shutil.rmtree("temp_save_dir", ignore_errors=False)
