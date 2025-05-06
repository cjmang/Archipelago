import typing

from BaseClasses import Item, ItemClassification
from typing import Dict


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification = ItemClassification.progression
    event: bool = False

item_table: Dict[str, ItemData] = {
    'Card Draw': ItemData(8000),
    'Rare Card Draw': ItemData(8001),
    'Relic': ItemData(8002),
    'Boss Relic': ItemData(8003),
    'One Gold': ItemData(8004, ItemClassification.filler),
    'Five Gold': ItemData(8005, ItemClassification.filler),

    # Event Items
    'Victory': ItemData(None, ItemClassification.progression, True),
    'Beat Act 1 Boss': ItemData(None, ItemClassification.progression, True),
    'Beat Act 2 Boss': ItemData(None, ItemClassification.progression, True),
    'Beat Act 3 Boss': ItemData(None, ItemClassification.progression, True),

}

item_pool: Dict[str, int] = {
    'Card Draw': 15,
    'Rare Card Draw': 2,
    'Relic': 10,
    'Boss Relic': 2
}

event_item_pairs: Dict[str, str] = {
    "Heart Room": "Victory",
    "Act 1 Boss": "Beat Act 1 Boss",
    "Act 2 Boss": "Beat Act 2 Boss",
    "Act 3 Boss": "Beat Act 3 Boss"
}
