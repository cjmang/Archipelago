from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from worlds.gstla.names import ItemName
from .base import BaseItem

MIMIC_NAMES: list[str] = [
    ItemName.Milquetoast_Mimic,
    ItemName.Clumsy_Mimic,
    ItemName.Mimic,
    ItemName.Journeyman_Mimic,
    ItemName.Advanced_Mimic,
    ItemName.Sacred_Mimic,
    ItemName.Royal_Mimic,
    ItemName.Imperial_Mimic,
    ItemName.Divine_Mimic,
]


@dataclass(frozen=True, slots=True, kw_only=True)
class Mimic(BaseItem):
    category = ItemCategory.mimics
    classification = ItemClassification.trap
    item_type = ItemType.Mimic

    tier: int  # for now, just based on the order of MIMIC_NAMES
    name: str

    @property
    def ap_id(self) -> int:
        # Agreed upon rando id of 0xA00 + mimic id
        return 0xA01 + self.tier

    @property
    def shuffled(self) -> bool:
        # might be filled in as traps, though
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        # TODO: not entirely sure if we should read item_locations.json here.
        #       if i see correctly, then the mimics IDs are pretty much fixed, anyway
        return tuple(cls(tier=tier, name=name) for tier, name in enumerate(MIMIC_NAMES))
