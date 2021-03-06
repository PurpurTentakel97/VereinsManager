# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

import sys

from logic.sqlite.database import Database
from config import exception_sheet as e, config_sheet as c
from logic.sqlite import select_handler as s_h, log_handler as l_h
import debug

debug_str: str = "AddHandler"
add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def add_type(self, type_name: str, raw_type_id: int, extra_value: str) -> int:
        sql_command: str = f"""INSERT INTO type (name,type_id,extra_value) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name, raw_type_id, extra_value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=None, new_data=type_name)
            l_h.log_handler.log_type(target_id=ID, target_column="extra_value", old_data=None, new_data=extra_value)

            member_ids = s_h.select_handler.get_all_IDs_from_member(active=True)
            function_ = None
            value = None

            if raw_type_id == c.config.raw_type_id.phone:
                function_ = self.add_member_nexus_phone
            elif raw_type_id == c.config.raw_type_id.mail:
                function_ = self.add_member_nexus_mail
            elif raw_type_id == c.config.raw_type_id.position:
                function_ = self.add_member_nexus_position
                value = False

            if function_ is None:
                return ID
            for member_id in member_ids:
                member_id = member_id[0]
                function_(type_id=ID, value=value, member_id=member_id, log_date=None)
            return ID

        except self.OperationalError:
            debug.error(item=debug_str, keyword="add_type", error_=sys.exc_info())
            raise e.AddFailed(info=f"Typ: {type_name}")

    # member
    def add_member(self, data: dict, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member 
        (first_name,last_name,street,number,zip_code,city,country,maps,b_day,entry_day,membership_type,special_member,comment) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command, (
                data["first_name"],
                data["last_name"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["country"],
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
            debug.error(item=debug_str, keyword="add_member", error_=sys.exc_info())
            raise e.AddFailed("Mitglied")

    # member nexus
    def add_member_nexus_phone(self, type_id: int, value: str, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_phone (member_id, type_id, number) VALUES (?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="phone")
            return ID
        except self.OperationalError:
            debug.error(item=debug_str, keyword="add_member_nexus_phone", error_=sys.exc_info())
            raise e.AddFailed(info=value)

    def add_member_nexus_mail(self, type_id: int, value: str, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_mail (member_id, type_id, mail) VALUES (?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="mail")
            return ID

        except self.OperationalError:
            debug.error(item=debug_str, keyword="add_member_nexus_mail", error_=sys.exc_info())
            raise e.AddFailed(info=value)

    def add_member_nexus_position(self, type_id: int, value: bool, member_id: int, log_date: int | None) -> int:
        sql_command: str = f"""INSERT INTO member_position (member_id, type_id, active) VALUES (?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value, log_date=log_date,
                                             type_="position")
            return ID

        except self.OperationalError:
            debug.error(item=debug_str, keyword="add_member_nexus_position", error_=sys.exc_info())
            raise e.AddFailed(info=str(value))

    # user
    def add_user(self, data: dict) -> int:
        sql_command: str = """INSERT INTO user (first_name,last_name,street,number,zip_code,city,country,phone,mail,
        position,password) VALUES (?,?,?,?,?,?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command, (
                data["firstname"],
                data["lastname"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["country"],
                data["phone"],
                data["mail"],
                data["position"],
                data["password_hashed"],
            ))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError:
            debug.error(item=debug_str, keyword="add_user", error_=sys.exc_info())
            raise e.AddFailed("Mitglied")

    # organisation
    def add_organisation(self, data: dict) -> int:
        sql_command: str = """INSERT INTO organisation (name,street,zip_code,city,country,bank_name,bank_owner,
                            bank_IBAN,bank_BIC,contact_person,web_link,extra_text) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""

        try:
            self.cursor.execute(sql_command, (
                data["name"],
                data["street"],
                data["zip_code"],
                data["city"],
                data["country"],
                data["bank_name"],
                data["bank_owner"],
                data["bank_IBAN"],
                data["bank_BIC"],
                data["contact_person"],
                data["web_link"],
                data["extra_text"],
            ))
            self.connection.commit()
            return self.cursor.lastrowid

        except self.OperationalError:
            debug.error(item=debug_str, keyword=f"add_organisation", error_=sys.exc_info())
            raise e.AddFailed(info="Organisationsdaten")

    # location
    def add_location(self, data: dict) -> int:
        sql_command: str = """INSERT INTO location (owner, name, street, number, zip_code, city, country, maps_link, 
        comment) VALUES(?,?,?,?,?,?,?,?,?)"""

        try:
            self.cursor.execute(sql_command, (
                data['owner'],
                data['name'],
                data['street'],
                data['number'],
                data['zip_code'],
                data['city'],
                data['country'],
                data['maps_link'],
                data['comment'],
            ))
            self.connection.commit()
            return self.cursor.lastrowid

        except self.OperationalError:
            debug.error(item=debug_str, keyword=f"add_location", error_=sys.exc_info())
            raise e.AddFailed(info="add new location")

    # schedule
    def add_schedule_day(self, data: dict) -> int:
        sql_command: str = """INSERT INTO schedule_day (date,hour,minute,location,uniform,comment) 
        VALUES (?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command, (
                data['date'],
                data['hour'],
                data['minute'],
                data['location'],
                data['uniform'],
                data['comment'],
            ))
            self.connection.commit()
            return self.cursor.lastrowid

        except self.OperationalError:
            debug.error(item=debug_str, keyword=f"add_schedule_day", error_=sys.exc_info())
            raise e.AddFailed("Add Schedule Day")

    def add_schedule_entry(self, data: dict, day_id: int) -> int:
        sql_command:str = """INSERT INTO schedule_entry (day,title,hour,minute,entry_type,location,comment) 
        VALUES (?,?,?,?,?,?,?);"""

        try:
            self.cursor.execute(sql_command,(
                day_id,
                data['title'],
                data['hour'],
                data['minute'],
                data['entry_type'],
                data['location'],
                data['comment'],
            ))
            self.connection.commit()
            return self.cursor.lastrowid

        except self.OperationalError:
            debug.error(item=debug_str, keyword=f"add_schedule_entry", error_=sys.exc_info())
            raise e.AddFailed("Add Schedule Entry")


def create() -> None:
    global add_handler
    add_handler = AddHandler()
