from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import CharacterIndex, ItemCategory, ItemType
from .base import BaseItem


@dataclass(frozen=True, slots=True, kw_only=True)
class Character(BaseItem):
    category = ItemCategory.characters
    classification = ItemClassification.progression
    item_type = ItemType.Character

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
