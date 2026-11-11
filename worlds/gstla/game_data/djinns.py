from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ElementType, ItemCategory, ItemType, LocationRestriction, LocationType
from .base import BaseItem, BaseLocation, read_json
from .location_names import loc_names_by_id

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
    category = ItemCategory.djinn
    classification = ItemClassification.progression_skip_balancing
    item_type = ItemType.Djinn

    element: ElementType
    index: int
    name: str

    @property
    def ap_id(self) -> int:
        return DJINN_MAPPING_TABLE_ADDR + (2 * self.rom_index)

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
    def shuffled(self) -> bool:
        # Custom handling for now. Gotta randomize djinns with each other,
        # not the other stuff in the pool. See `create_items()`
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(
            cls(element=ElementType(djinn['vanillaElement']), index=djinn['vanillaId'], name=djinn['vanillaName'])
            for djinn in read_json('data/djinn.json')
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DjinnLocation(BaseLocation):
    """
    The AP id and the flag is the same as the djinn that is at that location in vanilla.

    Same as EventLocation: Maybe merge these?
    """

    location_type = LocationType.Djinn
    restrictions = LocationRestriction.NONE

    djinn: Djinn

    @property
    def ap_id(self) -> int:
        return self.djinn.ap_id

    @property
    def flag(self) -> int:
        return self.djinn.flag_index

    @property
    def rando_flag(self) -> int:
        return self.djinn.flag_index

    @property
    def name(self) -> str:
        # Note: Item and Location names are a bit different:
        # Item name: "Flint"
        # Location name: "4th Party Member - Venus Djinni Flint" (from LocationName.Flint)
        return loc_names_by_id[self.ap_id]

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(djinn=djinn) for djinn in Djinn.load())
