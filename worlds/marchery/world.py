from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as magic_options

class MagicArcheryWorld(World):
    """
    It's a thing
    """

    game = "Magic Archery"


    options_dataclass = magic_options.MArcheryOptions
    options: magic_options.MArcheryOptions

    location_name_to_id = locations.location_table
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Forest"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.MAItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {}
