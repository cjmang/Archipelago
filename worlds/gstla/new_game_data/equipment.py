from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemFlag, ItemType
from worlds.gstla.names import ItemName
from .base import BaseItem

# TODO: I (draca) have a feeling that the balancing on these is off.
#       From the 7-8 runs I've played now, it seems like Shirts and Boots are extremely rare?
#       I get so many weapons not knowing what to do with them, but seemingly no Shirts & Boots?
ALWAYS_USEFUL_EQUIPMENT_TYPES = {ItemType.Shirt, ItemType.Boots, ItemType.Ring}
USEFUL_IF_RARE_EQUIPMENT_TYPES = {ItemType.Weapon, ItemType.Armor, ItemType.Shield, ItemType.Helm}

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
CLASSIFICATION_OVERRIDES = {}  # generate_code.CLASSIFICATION_OVERRIDES
EXCLUDED_ITEMS = []  # generate_code.EXCLUDED_ITEMS
EQUIPMENT_TYPES = [
    ItemType.Weapon,
    ItemType.Armor,
    ItemType.Shield,
    ItemType.Helm,
    ItemType.Boots,
    ItemType.Ring,
    ItemType.Shirt,
    # ItemType.Trident,  should we?
]


@dataclass(frozen=True, slots=True, kw_only=True)
class EquipmentItem(BaseItem):
    """
    All the gear: Weapons, armor, shirts, shields, helms, boots and rings

    This has historically been treated as a normal item, like key items or consumables,
    but they should probably be in their own dataclass.
    Especially if we want to do more things with gear progression in the future.

    # TODO: progression stuff in other_progression (+ Trident?)
    # TODO: rusty items?
    """

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
        # TODO: hm. we'd have to read item_location.json here, too.
        #       Should we rather have some categorizer centralized somewhere?
        #       Maybe via a contextvar?
        #       No idea if AP would like that, generation time and all that.
        pass

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
