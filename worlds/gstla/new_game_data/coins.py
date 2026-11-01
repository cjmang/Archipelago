from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from .base import BaseItem

COIN_ID_OFFSET = 0x8000  # ROM stores coin items as 0x8000 + amount


@dataclass(frozen=True, slots=True, kw_only=True)
class Coins(BaseItem):
    ITEM_TYPE = ItemType.Consumable
    CLASSIFICATION = ItemClassification.filler
    CATEGORY = ItemCategory.vanilla_coins

    amount: int

    @property
    def ap_id(self) -> int:
        return COIN_ID_OFFSET + self.amount

    @property
    def name(self) -> str:
        return f'Coins {self.amount}'

    @property
    def in_pool(self) -> bool:
        return False  # only filler

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        # TODO: Theoretically we could just ignore the vanilla contents and roll our own,
        #       since everything above 0x8000 just translates into any number of coins.
        #       We could also just hardcode the vanillaContents, since nobody would change it, anyway.
        #       Or: Just make a single item like "777 coins" and only that one gets filled?
        chests = cls.read_json('data/item_locations.json')
        amounts: list[int] = []
        for chest_variants in chests.values():
            for chest in chest_variants:
                contents = chest['vanillaContents']
                if contents > COIN_ID_OFFSET and contents - COIN_ID_OFFSET not in amounts:
                    amounts.append(contents - COIN_ID_OFFSET)
        return tuple(cls(amount=amount) for amount in amounts)
