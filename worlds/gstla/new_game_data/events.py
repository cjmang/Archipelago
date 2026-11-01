from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from .base import BaseItem

EVENTS: tuple[tuple[int, int, str, str], ...] = (
    # TODO: Use the proper LocationName enums
    #       Also dedup the other events lists
    # (ap_id, flag_index, location_name, name)
    (5001, 0x778, 'Mars Lighthouse - Doom Dragon', 'Doom Dragon Defeated'),
    (5002, 0x8AB, 'Alhafra Briggs', 'Briggs defeated'),
    (5003, 0x97F, 'Alhafra Prison Briggs', 'Briggs escaped'),
    (5004, 0x8FF, 'Gabomba Statue Ritual', 'Gabomba Statue Completed'),
    (5005, 0x9EE, 'Gaia Rock - Serpent', 'Serpent defeated'),
    (5006, 0x665, 'Sea of Time - Poseidon', 'Poseidon defeated'),
    (5007, 0x93F, 'Lemurian Ship - Aqua Hydra', 'Aqua Hydra defeated'),
    (5008, 0x94D, 'Shaman Village - Moapa', 'Moapa defeated'),
    (5009, 0xA21, 'Jupiter_Lighthouse Aeri - Agatio and Karst', 'Jupiter Beacon Lit'),
    (5010, 0xA4B, 'Mars Lighthouse - Flame Dragons', 'Flame Dragons - defeated'),
    (5011, 0x8DE, 'Lemurian Ship - Engine Room', 'Ship'),
    (5012, 0x8DF, 'Contigo - Wings of Anemos', 'Wings of Anemos'),
    (5013, 0x64A, 'Kandorean Temple - Chestbeaters', 'Chestbeaters defeated'),
    (5014, 0x64D, 'Yampi Desert - King Scorpion', 'King Scorpion defeated'),
    (5015, 0x662, 'Champa - Avimander', 'Avimander defeated'),
    (5016, 0x6A4, 'Treasure Isle - Star Magician', 'Star Magician defeated'),
    (5017, 0x6DD, 'Islet Cave - Sentinel', 'Sentinel defeated'),
    (5018, 0x6D1, 'Yampi Desert Cave - Valukar', 'Valukar defeated'),
    (5019, 0x6DA, 'Anemos Inner Sanctum - Dullahan', 'Dullahan defeated'),
    # Flag for 5020 is really the Jupiter Lighthouse flag. Base rando with PC shuffle
    # seems to do something weird with the reunion flag.
    (5020, 0xA21, 'Contigo - Reunion', 'Reunion'),
    (5021, 0x1, 'Victory Event', 'Victory'),
    (5022, 0xA5F, 'Loho - Ship Cannon', 'Ship Cannon'),
    (5023, 0xA30, 'Mars Lighthouse - Heated', 'Mars Lighthouse Heated'),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Event(BaseItem):
    ITEM_TYPE = ItemType.Event
    CLASSIFICATION = ItemClassification.progression
    CATEGORY = ItemCategory.events

    ap_id: int  # same as the corresponding location
    flag_index: int
    location_name: str
    name: str

    @property
    def in_pool(self) -> bool:
        # events have their own fixed location, see `items.create_events()`
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(
            cls(ap_id=ap_id, flag_index=flag_index, location_name=location_name, name=name)
            for ap_id, flag_index, location_name, name in EVENTS
        )
