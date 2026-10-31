from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import CharacterIndex, ItemCategory, ItemType
from .base import BaseItem

# previously in game_data.py:
# class CharacterDatum(NamedTuple):
#     id: int
#     name: str
#     flag: int
#     addr: int
#     item_type: ItemType = ItemType.Character
#
#  values below are ap_id, name, ap_id/flag, addr (addr here is some ROM offset
#  CharacterDatum(3328, 'Isaac', 3328, 16384384),
#  CharacterDatum(3329, 'Garet', 3329, 16384386),
#  CharacterDatum(3330, 'Ivan', 3330, 16384388),
#  CharacterDatum(3331, 'Mia', 3331, 16384390),
#  # Felix is 3332, but we don't do nutin with him
#  CharacterDatum(3333, 'Jenna', 3333, 16384392),
#  CharacterDatum(3334, 'Sheba', 3334, 16384394),
#  CharacterDatum(3335, 'Piers', 3335, 16384396),


@dataclass(frozen=True, slots=True, kw_only=True)
class Character(BaseItem):
    """
    Temporary notes:
    0xD00 == 3328
    So:
     0xD00 + 0 (Isaac index) = 3328,
     0xD00 + 1 (Garet index) = 3329,
     etc. also see _setup_characters
    But we also use these numbers (3328) as the location ID for Isaac
    """

    ITEM_TYPE = ItemType.Character
    CLASSIFICATION = ItemClassification.progression
    CATEGORY = ItemCategory.characters

    # addr: int  # unused, is some ROM address/offset
    index: CharacterIndex
    name: str

    @property
    def ap_id(self) -> int:
        return 0xD00 + self.index

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        """TODO: This stuff is also in item_locations.json, should we use that instead?"""
        return tuple(
            cls(index=index, name=index.name.capitalize())
            for index in CharacterIndex
            if index is not CharacterIndex.FELIX  # we don't do nutin with him
        )
