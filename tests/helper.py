# Purpur Tentakel
# 31.03.2022
# VereinsManager / Test Helper

from random import randint
import string
import random
import shutil

from config import config_sheet
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
    config_sheet.create_config()


def generate_temp_database():
    _generate_config()
    config_sheet.config.save_dir = "temp_save_dir"
    config_sheet.config.organisation_dir = "temp_organisation_dir"
    config_sheet.config.database_name = "unit_test_database"
    database.crate_database()


def add_generic_type() -> None:
    database.database.cursor.execute("""INSERT INTO type (name,type_id) VALUES (?,?);""", ("Type_1", 1))
    database.database.cursor.execute("""INSERT INTO type (name,type_id) VALUES (?,?);""", ("Type_2", 2))
    database.database.connection.commit()


def generate_select_handler() -> None:
    select_handler.create_select_handler()


def drop_select_handler() -> None:
    del select_handler.select_handler


def delete_temp_database():
    database.database.drop_connection()
    shutil.rmtree("temp_save_dir", ignore_errors=False)
