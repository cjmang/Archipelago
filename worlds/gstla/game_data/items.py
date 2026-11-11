from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from worlds.gstla.names import ItemName
from .base import BaseItem, read_json
from .item_sources import get_item_sources

VANILLA_ITEM_TYPES = [
    ItemType.Consumable,
    ItemType.KeyItem,
    ItemType.Class,
    ItemType.Trident,
]

EXCLUDED_ITEMS = {
    184,  # Hermes' Water
    185,  # Empty Bottle
    220,  # Venus Star
    221,  # Mercury Star
    223,  # Mythril Bag (Jupiter)
    224,  # Mythril Bag (Empty)
    225,  # Small Jewel
    230,  # Dragon's Eye
    232,  # Anchor Charm
    234,  # Cell Key
    235,  # Boat Ticket
    237,  # Mystic Draught
    245,  # Mythril Bag (Mars & Jupiter)
    246,  # Jupiter Star
    247,  # Mars Star (222, "Mythril Bag (Mars)" is the one actually used in game)
    450,  # Signal Whistle
    457,  # Large Bread
}
NAME_OVERRIDES: dict[int, str] = {
    0: ItemName.Empty,
    222: ItemName.Mars_Star,  # Mythril Bag (Mars)
}
CLASSIFICATION_OVERRIDES: dict[str, ItemClassification] = {
    ItemName.Sea_Gods_Tear: ItemClassification.progression,
    ItemName.Right_Prong: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Healing_Fungus: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Black_Crystal: ItemClassification.progression,
    ItemName.Pretty_Stone: ItemClassification.progression,
    ItemName.Red_Cloth: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Milk: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Lil_Turtle: ItemClassification.progression,
    ItemName.Aquarius_Stone: ItemClassification.progression,
    ItemName.Left_Prong: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Dancing_Idol: ItemClassification.progression,
    ItemName.Center_Prong: ItemClassification.progression_deprioritized_skip_balancing,
    ItemName.Magma_Ball: ItemClassification.progression,
    ItemName.Trident: ItemClassification.progression,
    ItemName.Blue_Key: ItemClassification.progression,
    ItemName.Red_Key: ItemClassification.progression,
    ItemName.Mars_Star: ItemClassification.progression,
    ItemName.Ruin_Key: ItemClassification.progression,
    ItemName.Mysterious_Card: ItemClassification.useful,
    ItemName.Trainers_Whip: ItemClassification.useful,
    ItemName.Tomegathericon: ItemClassification.useful,
    ItemName.Potion: ItemClassification.useful,
    ItemName.Psy_Crystal: ItemClassification.useful,
    ItemName.Water_of_Life: ItemClassification.useful,
    ItemName.Mist_Potion: ItemClassification.useful,
    ItemName.Tear_Stone: ItemClassification.useful,
    ItemName.Star_Dust: ItemClassification.useful,
    ItemName.Sylph_Feather: ItemClassification.useful,
    ItemName.Dragon_Skin: ItemClassification.useful,
    ItemName.Salamander_Tail: ItemClassification.useful,
    ItemName.Golem_Core: ItemClassification.useful,
    ItemName.Mythril_Silver: ItemClassification.useful,
    ItemName.Dark_Matter: ItemClassification.useful,
    ItemName.Orihalcon: ItemClassification.useful,
}

OTHER_ITEM_GROUPS: dict[ItemCategory, set[int]] = {
    ItemCategory.stat_boosters: set(range(191, 197)),  # Power Bread through Lucky Pepper
    ItemCategory.useful_consumables: {183, 186, 189, 190},  # Potion, Psy Crystal, Water of Life, Mist Potion
    ItemCategory.forge_materials: set(range(429, 438)),  # Tear Stone through Orihalcon
    ItemCategory.class_change_items: set(range(443, 446)),  # Mysterious Card, Trainer's Whip, Tomegathericon
    ItemCategory.misc: {0, 231, 449},  # Empty, Bone, Laughing Fungus
}


@dataclass(frozen=True, slots=True, kw_only=True)
class VanillaItem(BaseItem):
    """Consumables, Key items, and basically everything else that's not in the other game_data modules."""

    ap_id: int  # the same as the ROM item id
    rom_name: str
    item_type: ItemType = ItemType.Consumable  # just a default

    @property
    def name(self) -> str:
        return NAME_OVERRIDES.get(self.ap_id, self.rom_name)

    @property
    def classification(self) -> ItemClassification:
        return CLASSIFICATION_OVERRIDES.get(self.name, ItemClassification.filler)

    @property
    def category(self) -> ItemCategory:
        if ItemClassification.progression in self.classification:
            return ItemCategory.other_progression
        for category, item_ids in OTHER_ITEM_GROUPS.items():
            if self.ap_id in item_ids:
                return category
        if self.classification == ItemClassification.useful:
            return ItemCategory.useful_remainder

        sources = get_item_sources()
        if self.ap_id in sources.chests:
            return ItemCategory.remainder
        if self.ap_id in sources.shops:
            return ItemCategory.shop_only
        if self.ap_id in sources.forge:
            return ItemCategory.forge_only
        if self.ap_id in sources.lucky:
            return ItemCategory.lucky_only
        return ItemCategory.non_vanilla

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        vanilla_items = [
            item
            for item in read_json('data/items.json').values()
            if item['id'] not in EXCLUDED_ITEMS and item['itemType'] in VANILLA_ITEM_TYPES
        ]

        return tuple(
            cls(
                ap_id=item['id'],
                rom_name=item['name'],
                item_type=ItemType(item['itemType']),
            )
            for item in vanilla_items
        )
