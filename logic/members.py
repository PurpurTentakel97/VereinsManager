# Purpur Tentakel
# 21.01.2022
# VereinsManager / Members

from datetime import date

members: list = list()


class Member:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name

        self.street: str = str()
        self.number: str = str()
        self.zip_code: str = str()
        self.city: str = str()

        self.birth_date: date | None = None
        self.entry_date: date | None = None

        self.phone_numbers: dict[str, str] = dict()
        self.mail_addresses: dict[str, str] = dict()

        self.membership_type: str = str()
        self.special_member: bool = False
        self.positions: set[str] = set()
        self.instruments: set[str] = set()

        self.comment_text: str = str()

    def set_first_name(self, first_name: str) -> None:
        self.first_name: str = first_name

    def set_last_name(self, last_name: str) -> None:
        self.last_name: str = last_name

    def set_street(self, street: str) -> None:
        self.street: str = street

    def set_number(self, number: str) -> None:
        self.number: str = number

    def set_zip_code(self, zip_code: str) -> None:
        self.zip_code: str = zip_code

    def set_city(self, city: str) -> None:
        self.city: str = city

    def set_birth_date(self, date_: dict[str, int]) -> None:
        self.birth_date: date = date(date_["year"], date_["month"], date_["day"])

    def set_entry_date(self, date_: dict[str, int]) -> None:
        self.entry_date: date = date(date_["year"], date_["month"], date_["day"])

    def set_landline_phone_number(self, number: str) -> None:
        self.landline_phone_number: str = number

    def set_mobile_phone_number(self, number: str) -> None:
        self.mobile_phone_number: str = number

    def set_mail_address(self, mail: str) -> None:
        self.mail_address: str = mail

    def set_membership_type(self, membership: str) -> None:
        self.membership_type: str = membership

    def set_special_member(self, special: bool) -> None:
        self.special_member: bool = special

    def add_position(self, position: str) -> None:
        self.positions.add(position)

    def remove_position(self, position: str) -> None:
        self.positions.discard(position)

    def add_instrument(self, instrument: str) -> None:
        self.instruments.add(instrument)

    def remove_instrument(self, instrument: str) -> None:
        self.instruments.discard(instrument)

    def set_comment_text(self, text: str) -> None:
        self.comment_text.str = text
