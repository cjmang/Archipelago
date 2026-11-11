from enum import StrEnum

from BaseClasses import CollectionState, Item, Location, Region
from worlds.gstla.game_data.loader import load_game_data
from worlds.gstla.game_data.locations import FLAG_OVERWRITES
from worlds.gstla.names import LocationName
from .gstla_types import ItemType, LocationData, LocationType
from .items import GSTLAItem


def allow_djinn(_: CollectionState, item: Item) -> bool:
    return isinstance(item, GSTLAItem) and item.item_data.type == ItemType.Djinn


class GSTLALocation(Location):
    game: str = 'Golden Sun The Lost Age'
    location_data: LocationData

    def __init__(self, player: int, name: str | StrEnum, location: LocationData, region: Region):
        # Yes, calling str(name) because it's secretly an enum, and pickling does terrible things in MultiServer
        super().__init__(player, str(name), location.id, region)
        self.location_data = location
        if location.type == LocationType.Djinn:
            self.always_allow = allow_djinn
        elif location.type == LocationType.Event:
            self.address = None


# Locations that cannot have remote items
# TODO: Understand and document the logic behind this remote_blacklist
def get_remote_blacklist() -> set[int]:
    game_data = load_game_data()
    return set(FLAG_OVERWRITES) | {game_data.location_by_name[LocationName.Idejima_Jenna].id}
