# Purpur Tentakel
# 06.05.2022
# VereinsManager // Location Data Handler


from helpers import helper
from logic.main_handler import location_handler
import debug

debug_str: str = "Location Data Handler"


def get_location_data(ID: int) -> tuple[str | dict, bool]:
    data, valid = location_handler.get_single_location_by_ID(ID=ID)
    if not valid:
        return data, valid

    data['maps'] = _transform_maps_link(data=data)

    return data, True


def _transform_maps_link(data: dict) -> str:
    if data['maps_link']:
        return data['maps_link']

    return helper.combine_maps_string(
        street=data['street'],
        number=data['number'],
        zip_code=data['zip_code'],
        city=data['city'],
    )
