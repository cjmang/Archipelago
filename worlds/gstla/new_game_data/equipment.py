from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemFlag, ItemType
from worlds.gstla.names import ItemName
from .base import BaseItem
from .item_sources import get_item_sources

# TODO: I (draca) have a feeling that the balancing on these is off.
#       From the 7-8 runs I've played now, it seems like Shirts and Boots are extremely rare?
#       I get so many weapons not knowing what to do with them, but seemingly no Shirts & Boots?
ALWAYS_USEFUL_EQUIPMENT_TYPES = {ItemType.Shirt, ItemType.Boots, ItemType.Ring}
USEFUL_IF_RARE_EQUIPMENT_TYPES = {ItemType.Weapon, ItemType.Armor, ItemType.Shield, ItemType.Helm}
RUSTY_ITEM_IDS = {417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427}
NAME_OVERRIDES: dict[int, str] = {
    # some of the item names in the json are duplicated, gotta make 'em unique
    123: ItemName.Dragon_Shield_GS,
    132: ItemName.Spirit_Gloves_GS,
    417: ItemName.Rusty_Sword_CorsairsEdge,
    418: ItemName.Rusty_Sword_RobbersBlade,
    419: ItemName.Rusty_Sword_PiratesSabre,
    420: ItemName.Rusty_Sword_SoulBrand,
    421: ItemName.Rusty_Axe_CaptainsAxe,
    422: ItemName.Rusty_Axe_VikingAxe,
    423: ItemName.Rusty_Mace_DemonMace,
    424: ItemName.Rusty_Mace_HagboneMace,
    425: ItemName.Rusty_Staff_Dracomace,
    426: ItemName.Rusty_Staff_GlowerStaff,
    427: ItemName.Rusty_Staff_GoblinsRod,
}
CLASSIFICATION_OVERRIDES: dict[str, ItemClassification] = {
    ItemName.Shamans_Rod: ItemClassification.progression,
}
EXCLUDED_ITEMS = []  # empty, might want to change in the future for balancing
EQUIPMENT_TYPES = [
    ItemType.Weapon,
    ItemType.Armor,
    ItemType.Shield,
    ItemType.Helm,
    ItemType.Boots,
    ItemType.Ring,
    ItemType.Shirt,
]


@dataclass(frozen=True, slots=True, kw_only=True)
class EquipmentItem(BaseItem):
    """Weapons, armor, shirts, shields, helms, boots and rings"""

    ap_id: int  # the same as the ROM item id
    rom_name: str
    item_type: ItemType = ItemType.Weapon  # just a default
    flags: ItemFlag

    @property
    def name(self) -> str:
        return NAME_OVERRIDES.get(self.ap_id, self.rom_name)

    @property
    def is_rare(self) -> bool:
        return ItemFlag.Rare in self.flags

    @property
    def classification(self) -> ItemClassification:
        if self.name in CLASSIFICATION_OVERRIDES:
            return CLASSIFICATION_OVERRIDES[self.name]
        if self.item_type in ALWAYS_USEFUL_EQUIPMENT_TYPES:
            return ItemClassification.useful
        if self.item_type in USEFUL_IF_RARE_EQUIPMENT_TYPES and self.is_rare:
            return ItemClassification.useful
        return ItemClassification.filler

    @property
    def category(self) -> ItemCategory:
        if self.classification == ItemClassification.progression:
            return ItemCategory.other_progression
        if self.ap_id in RUSTY_ITEM_IDS:
            return ItemCategory.rusty_items

        sources = get_item_sources()
        if self.ap_id in sources.chests:
            if self.classification == ItemClassification.useful:
                return ItemCategory.useful_remainder
            return ItemCategory.misc  # shouldn't happen
        if self.ap_id in sources.shops:
            return ItemCategory.shop_only
        if self.ap_id in sources.forge:
            return ItemCategory.forge_only
        if self.ap_id in sources.lucky:
            return ItemCategory.lucky_only
        return ItemCategory.non_vanilla

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        equipment_items = [
            item
            for item in BaseItem.read_json('data/items.json').values()
            if item['id'] not in EXCLUDED_ITEMS and item['itemType'] in EQUIPMENT_TYPES
        ]

        return tuple(
            cls(
                ap_id=item['id'],
                rom_name=item['name'],
                item_type=ItemType(item['itemType']),
                flags=ItemFlag(item['flags']),
                # we could extract a lot more, but for now not necessary
            )
            for item in equipment_items
        )
