from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType, PsynergyID
from .base import BaseItem, read_json

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

UNUSED_PSYNERGIES = [
    PsynergyID.CLOAK,
    PsynergyID.HALT,
]

PSYNERGY_ITEM_ID_OFFSET = 0xE00


@dataclass(frozen=True, slots=True, kw_only=True)
class LearnedPsynergy(BaseItem):
    category = ItemCategory.learned_psynergy
    classification = ItemClassification.progression
    item_type = ItemType.Psynergy

    ability_id: PsynergyID
    name: str

    @property
    def ap_id(self) -> int:
        return PSYNERGY_ITEM_ID_OFFSET + self.ability_id

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(ability_id=ability_id, name=name) for ability_id, name in LEARNED_PSYNERGY_MAPPING.items())


@dataclass(frozen=True, slots=True, kw_only=True)
class PsynergyItem(BaseItem):
    category = ItemCategory.psynergy_items
    item_type = ItemType.PsynergyItem

    item_id: int  # items.json id, not the AP id
    name: str
    ability_id: PsynergyID

    @property
    def ap_id(self) -> int:
        return PSYNERGY_ITEM_ID_OFFSET + self.ability_id

    @property
    def shuffled(self) -> bool:
        return self.ability_id not in UNUSED_PSYNERGIES

    @property
    def classification(self) -> ItemClassification:
        if self.ability_id in FILLER_PSYNERGIES:
            return ItemClassification.filler
        return ItemClassification.progression

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        items = read_json('data/items.json').values()
        return tuple(
            cls(item_id=item['id'], name=item['name'], ability_id=PsynergyID(item['useEffect']))
            for item in items
            if item['itemType'] == ItemType.PsynergyItem
        )
