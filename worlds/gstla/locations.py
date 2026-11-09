from typing import TYPE_CHECKING

from BaseClasses import Location, Region
from worlds.gstla.names import LocationName
from worlds.gstla.new_game_data.location_names import ids_by_loc_name
from worlds.gstla.new_game_data.locations import FLAG_OVERWRITES
from .gstla_types import ItemType, LocationData

if TYPE_CHECKING:
    from .items import GSTLAItem


def allow_djinn(_, item: 'GSTLAItem') -> bool:
    return item.item_data.type == ItemType.Djinn


class GSTLALocation(Location):
    game: str = 'Golden Sun The Lost Age'
    location_data: LocationData
    item: 'GSTLAItem'

    def __init__(self, player: int, name: str, location: LocationData, region: Region):
        # Yes, calling str(name) because it's secretly an enum, and pickling does terrible things in MultiServer
        super().__init__(player, str(name), location.id, region)
        self.location_data = location

    @staticmethod
    def create_djinn_location(player: int, name: str, location: LocationData, region: Region) -> 'GSTLALocation':
        # TODO: Replace with DjinnLocation.as_location()
        ret = GSTLALocation(player, name, location, region)
        ret.always_allow = allow_djinn
        return ret

    @staticmethod
    def create_event_location(player: int, name: str, location: LocationData, region: Region):
        # TODO: Replace with EventLocation.as_location()
        ret = GSTLALocation(player, name, location, region)
        ret.address = None
        return ret


# Locations that cannot have remote items
# TODO: Understand and document the logic behind this remote_blacklist
remote_blacklist: set[int] = set(FLAG_OVERWRITES) | {ids_by_loc_name[LocationName.Idejima_Jenna]}
