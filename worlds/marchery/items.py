from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import MagicArcheryWorld


ITEM_NAME_TO_ID = {
    "Concentration": 1,
    "Strength": 2,
    "Dexterity": 3,
    "Accuracy": 4,
    "Vitality": 5,
    "Magic": 6,
    "Arrow": 7,
}

# TODO: clean this up once the world design is figured out
ITEM_NAME_TO_COUNT = {
    "Concentration": 200,
    "Strength": 200,
    "Dexterity": 200,
    "Accuracy": 200,
    "Vitality": 200,
    "Magic": 200,
    "Arrow": 0,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Concentration": ItemClassification.progression,
    "Strength": ItemClassification.progression,
    "Dexterity": ItemClassification.progression,
    "Accuracy": ItemClassification.progression,
    "Vitality": ItemClassification.progression,
    "Magic": ItemClassification.progression,
    "Arrow": ItemClassification.filler,
}

class MAItem(Item):
    game = "Magic Archery"

def get_random_filler_item_name(world: MagicArcheryWorld) -> str:
    return "Arrow"


def create_item_with_correct_classification(world: MagicArcheryWorld, name: str) -> MAItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]


    return MAItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: MagicArcheryWorld) -> None:
    itempool = []
    for item_name, count in ITEM_NAME_TO_COUNT.items():
        itempool += [world.create_item(item_name) for _ in range(count)]

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
