from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from .base import BaseItem


@dataclass(frozen=True, slots=True, kw_only=True)
class Summon(BaseItem):
    category = ItemCategory.summons
    classification = ItemClassification.useful  # progression on "Summon Hunt", see items.py
    item_type = ItemType.Summon

    index: int
    name: str

    @property
    def ap_id(self) -> int:
        return 0xF00 + self.index

    @property
    def in_pool(self) -> bool:
        # since we can only randomize the summon tablets,
        # we'll have to ignore the others here
        return self.index >= 16

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(index=summon['id'], name=summon['name']) for summon in cls.read_json('data/summons.json'))
