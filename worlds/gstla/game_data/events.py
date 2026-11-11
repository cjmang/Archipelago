from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType, LocationRestriction, LocationType
from worlds.gstla.names import ItemName
from .base import BaseItem, BaseLocation
from .location_names import loc_names_by_id

EVENTS: tuple[tuple[int, int, str], ...] = (
    # TODO: dedup the other events lists
    # (ap_id, flag_index, name)
    (5001, 0x778, ItemName.Doom_Dragon_Defeated),
    (5002, 0x8AB, ItemName.Briggs_defeated),
    (5003, 0x97F, ItemName.Briggs_escaped),
    (5004, 0x8FF, ItemName.Gabomba_Statue_Completed),
    (5005, 0x9EE, ItemName.Serpent_defeated),
    (5006, 0x665, ItemName.Poseidon_defeated),
    (5007, 0x93F, ItemName.Aqua_Hydra_defeated),
    (5008, 0x94D, ItemName.Moapa_defeated),
    (5009, 0xA21, ItemName.Jupiter_Beacon_Lit),
    (5010, 0xA4B, ItemName.Flame_Dragons_defeated),
    (5011, 0x8DE, ItemName.Ship),
    (5012, 0x8DF, ItemName.Wings_of_Anemos),
    (5013, 0x64A, ItemName.Chestbeaters_defeated),
    (5014, 0x64D, ItemName.King_Scorpion_defeated),
    (5015, 0x662, ItemName.Avimander_defeated),
    (5016, 0x6A4, ItemName.Star_Magician_defeated),
    (5017, 0x6DD, ItemName.Sentinel_defeated),
    (5018, 0x6D1, ItemName.Valukar_defeated),
    (5019, 0x6DA, ItemName.Dullahan_defeated),
    # Flag for 5020 is really the Jupiter Lighthouse flag. Base rando with PC shuffle
    # seems to do something weird with the reunion flag.
    (5020, 0xA21, ItemName.Reunion),
    (5021, 0x1, ItemName.Victory),
    (5022, 0xA5F, ItemName.Ship_Cannon),
    (5023, 0xA30, ItemName.Mars_Lighthouse_Heated),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Event(BaseItem):
    category = ItemCategory.events
    classification = ItemClassification.progression
    item_type = ItemType.Event

    ap_id: int  # same as the corresponding location
    flag_index: int
    name: str

    @property
    def location_name(self) -> str:
        return loc_names_by_id[self.ap_id]

    @property
    def shuffled(self) -> bool:
        # events have their own fixed location, see `items.create_events()`
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(ap_id=ap_id, flag_index=flag_index, name=name) for ap_id, flag_index, name in EVENTS)


@dataclass(frozen=True, slots=True, kw_only=True)
class EventLocation(BaseLocation):
    """
    Everything here uses the exact same values as the Event item but uses .as_location().
    Maybe we'll just merge these two in the future.
    """

    location_type = LocationType.Event

    # TODO: Why LocationRestriction(7)? wasn't there a NoMoney when this was created?
    #       see internal_location_data.py
    restrictions = LocationRestriction.NoEmpty | LocationRestriction.NoMimic | LocationRestriction.NoSummon

    ap_id: int
    flag: int

    @property
    def name(self) -> str:
        return loc_names_by_id[self.ap_id]

    @property
    def rando_flag(self) -> int:
        return self.flag

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(cls(ap_id=ap_id, flag=flag) for ap_id, flag, _ in EVENTS)
