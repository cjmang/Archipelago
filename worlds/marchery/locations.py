from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location


if TYPE_CHECKING:
    from .world import MagicArcheryWorld

LOCATION_NAME_TO_ID = {
    "Concentration Level": 1,
    "Strength Level": 201,
    "Dexterity Level": 401,
    "Accuracy Level": 601,
    "Vitality Level": 801,
    "Magic Level": 1001,
}

class MALocation(Location):
    game = "Magic Archery"


def create_all_locations(world: MagicArcheryWorld) -> None:
    create_regular_locations(world)

def create_regular_locations(world: MagicArcheryWorld) -> None:
    forest = world.get_region("Forest")
    # locations = {}
    # forest.add_locations(locations)
    forest.add_locations(location_table, MALocation)

def create_location_table() -> dict[str, int]:
    ret: dict[str, int] = {}
    for loc_name, start in LOCATION_NAME_TO_ID.items():
        for i in range(200):
            ret[f"{loc_name} {i + 1}"] = start + i
    return ret

location_table = create_location_table()