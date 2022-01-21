# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members

from datetime import date

members: list = list()


class Member:
    def __init__(self, first_name: str, last_name: str):
        self.first_name: str = first_name
        self.last_name: str = last_name

        self.street: str = str()
        self.number: str = str()
        self.zip_code: str = str()
        self.city: str = str()

        self.birth_date: date | None = None
        self.entry_date: date | None = None

        self.landline_phone_number: str = str()
        self.mobile_phone_number: str = str()
        self.mail_address: str = str()

        self.membership_type: str = str()
        self.special_member: bool = False
        self.position: str = str()
        self.instrument: str = str()

        self.comment_text: str = str()
