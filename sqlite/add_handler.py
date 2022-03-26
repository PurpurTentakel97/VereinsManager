# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from sqlite import select_handler as s_h, log_handler as l_h
from config import exception_sheet as e, config_sheet as c
import debug

debug_str: str = "AddHandler"
add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> int:
        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name, raw_type_id))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=None, new_data=type_name)

            member_ids = s_h.select_handler.get_all_IDs_from_member(active=True)
            function_ = None
            value = None

            if raw_type_id == c.config.raw_type_id["phone"]:
                function_ = self.add_member_nexus_phone
            elif raw_type_id == c.config.raw_type_id["mail"]:
                function_ = self.add_member_nexus_mail
            elif raw_type_id == c.config.raw_type_id["position"]:
                function_ = self.add_member_nexus_position
                value = False

            if function_ is None:
                return ID
            for member_id in member_ids:
                member_id = member_id[0]
                function_(type_id=ID, value=value, member_id=member_id, log_date=None)
            return ID

        except self.OperationalError:
            raise e.AddFailed(info=f"Typ: {type_name}")

    # member
    def add_member(self, data: dict, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member 
        (first_name,last_name,street,number,zip_code,city,maps,b_day,entry_day,membership_type,special_member,comment) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command, (
                data["first_name"],
                data["last_name"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["maps"],
                data["birth_date"],
                data["entry_date"],
                data["membership_type"],
                data["special_member"],
                data["comment_text"],
            ))
            self.connection.commit()
            ID = self.cursor.lastrowid
            l_h.log_handler.log_member(target_id=ID, old_data=None, new_data=data, log_date=log_date)
            return ID
        except self.OperationalError:
            raise e.AddFailed("Mitglied")

    # member nexus
    def add_member_nexus_phone(self, type_id: int, value: str, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_phone (member_id, type_id, number) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="phone")
            return ID
        except self.OperationalError:
            raise e.AddFailed(info=value)

    def add_member_nexus_mail(self, type_id: int, value: str, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_mail (member_id, type_id, mail) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="mail")
            return ID

        except self.OperationalError:
            raise e.AddFailed(info=value)

    def add_member_nexus_position(self, type_id: int, value: bool, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_position (member_id, type_id, active) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="position")
            return ID

        except self.OperationalError:
            raise e.AddFailed(info=str(value))

    # user
    def add_user(self, data: dict) -> int:
        sql_command: str = """INSERT INTO user (first_name,last_name,street,number,zip_code,city,phone,mail,
        position,password) VALUES (?,?,?,?,?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command, (
                data["firstname"],
                data["lastname"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["phone"],
                data["mail"],
                data["position"],
                data["password_hashed"],
            ))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError:
            raise e.AddFailed("Mitglied")


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()
