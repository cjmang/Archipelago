from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.game_data import ElementType  # TODO: move to gstla_types?
from worlds.gstla.gstla_types import ItemCategory, ItemType
from .base import BaseItem

# TODO: merge the constants below with the stuff from somewhere else:
#       _DataLocations.DJINN_FLAGS, client._load_djinn()
#       also make sure we use these constants everywhere instead of hardcoding "20" or something.


DJINN_PER_ELEMENT = 18  # (0x12), ROM
DJINN_MAPPING_TABLE_ADDR = 0xFA0000  # ROM (the patched table, 4 * 18 * 2 bytes)
DJINN_FLAG_START = 0x30  # 48, EWRAM
DJINN_FLAGS_PER_ELEMENT = 20  # (0x14), EWRAM
DJINN_FLAGS_LENGTH = len(ElementType) * DJINN_FLAGS_PER_ELEMENT // 8  # 10 bytes


def flag_index_to_djinn(flag: int) -> tuple[ElementType, int]:
    # 111 = ElementType.Air + ID 3 = Smog
    # TODO: unused for now. Maybe for _check_djinn_flags?
    offset = flag - DJINN_FLAG_START
    element, index = divmod(offset, DJINN_FLAGS_PER_ELEMENT)
    if index >= DJINN_PER_ELEMENT:
        raise ValueError(f'Djinn flag at {hex(flag)} unused')
    return ElementType(element), index


@dataclass(frozen=True, slots=True, kw_only=True)
class Djinn(BaseItem):
    ITEM_TYPE = ItemType.Djinn
    CLASSIFICATION = ItemClassification.progression_skip_balancing
    CATEGORY = ItemCategory.djinn

    element: ElementType
    index: int
    name: str

    @property
    def rom_index(self) -> int:
        # the index in the patched randomizer table in ROM (0-71)
        return self.element * DJINN_PER_ELEMENT + self.index

    @property
    def flag_index(self) -> int:
        # the index/spot of the "obtained" flag in EWRAM incl. offset
        # also named "rando_flag" in other spots
        return DJINN_FLAG_START + self.element * DJINN_FLAGS_PER_ELEMENT + self.index

    @property
    def ap_id(self) -> int:
        return DJINN_MAPPING_TABLE_ADDR + (2 * self.rom_index)

    @property
    def in_pool(self) -> bool:
        # Custom handling for now. Gotta randomize djinns with each other,
        # not the other stuff in the pool. See `create_items()`
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(
            cls(element=ElementType(djinn['vanillaElement']), index=djinn['vanillaId'], name=djinn['vanillaName'])
            for djinn in cls.read_json('data/djinn.json')
        )
