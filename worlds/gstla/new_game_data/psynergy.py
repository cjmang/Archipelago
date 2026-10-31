from dataclasses import dataclass, replace
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemData, ItemType, PsynergyID
from .base import BaseItem

# we don't have an easy 1:1 mapping in the data files from
# item name to psynergy, so this is just static in code for now.
LEARNED_PSYNERGY_MAPPING: dict[PsynergyID, str] = {
    PsynergyID.GROWTH: 'Growth',
    PsynergyID.WHIRLWIND: 'Whirlwind',
    PsynergyID.PARCH: 'Parch',
    PsynergyID.SAND: 'Sand',
    PsynergyID.MIND_READ: 'Mind Read',
    PsynergyID.REVEAL: 'Reveal',
    PsynergyID.BLAZE: 'Blaze',
}

FILLER_PSYNERGIES = [
    PsynergyID.CATCH,
]


@dataclass(frozen=True, slots=True, kw_only=True)
class LearnedPsynergy(BaseItem):
    ITEM_TYPE = ItemType.Psynergy
    CLASSIFICATION = ItemClassification.progression
    CATEGORY = ItemCategory.learned_psynergy

    ability_id: PsynergyID
    name: str

    @property
    def ap_id(self) -> int:
        return 0xE00 + self.ability_id

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(ability_id=ability_id, name=name) for ability_id, name in LEARNED_PSYNERGY_MAPPING.items())


@dataclass(frozen=True, slots=True, kw_only=True)
class PsynergyItem(BaseItem):
    ITEM_TYPE = ItemType.PsynergyItem
    CLASSIFICATION = ItemClassification.progression
    CATEGORY = ItemCategory.psynergy_items

    item_id: int  # items.json id, not the AP id
    name: str
    ability_id: PsynergyID

    @property
    def ap_id(self) -> int:
        return 0xE00 + self.ability_id

    def as_item(self) -> ItemData:
        item = BaseItem.as_item(self)
        if self.ability_id in FILLER_PSYNERGIES:
            return replace(item, classification=ItemClassification.filler)
        return item

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        items = cls.read_json('data/items.json').values()
        return tuple(
            cls(item_id=item['id'], name=item['name'], ability_id=PsynergyID(item['useEffect']))
            for item in items
            if item['itemType'] == ItemType.PsynergyItem
        )
