from dataclasses import dataclass
from typing import Self

from worlds.gstla.gstla_types import LocationRestriction, LocationType
from worlds.gstla.new_game_data.base import BaseLocation, read_json

"""
Examples:
# Djinn (Flint)
InternalLocationData(
    rando_flag=48,
    flag=48,
    id=16384000,
    ap_id=16384000,
    addresses=[16384000],
    event_type=128,
    vanilla_contents=0,
    is_key=True,
    is_major=True,
    loc_type=LocationType.Djinn,
    restrictions=LocationRestriction.NONE,
    event=False,
)

# Summon tablet (Moloch)
InternalLocationData(
    rando_flag=19,
    flag=19,
    id=19,
    ap_id=992068,
    addresses=[992068],
    event_type=132,
    vanilla_contents=3859,
    is_key=True,
    is_major=True,
    loc_type=LocationType.Item,
    restrictions=LocationRestriction(0),
    event=False,
),

# Psynergy (Reveal)
InternalLocationData(
    rando_flag=2260,
    flag=2260,
    id=2260,
    ap_id=16384190,
    addresses=[16384190],
    event_type=132,
    vanilla_contents=3728,
    is_key=True,
    is_major=True,
    loc_type=LocationType.Psyenergy,
    restrictions=LocationRestriction(11),
    event=False,
)

# Mars Lighthouse - Doom Dragon Doom Dragon Defeated
InternalLocationData(
    rando_flag=1912,
    flag=1912,
    id=5001,
    ap_id=5001,
    addresses=[0],
    event_type=0,
    vanilla_contents=5001,
    is_key=True,
    is_major=True,
    loc_type=LocationType.Event,
    restrictions=LocationRestriction(7),
    event=True,
)


Gotta watch out for this one:
# A few locations use different flags than stated in the item_locations.json file
# E.g. character starting inventories
flag_overwrites = {
    # address: CharacterIndex == hex(address)
    16384202: 0x4,  # Shaman's Rod -> Felix == 0XFA00CA
    16384204: 0x6,  # Mind Read -> Sheba == 0XFA00CC
    16384206: 0x6,  # Whirlwind -> Sheba == 0XFA00CE
    16384208: 0x4,  # Growth -> Felix == 0XFA00D0
    16384210: 0x3,  # Carry Stone -> Mia == 0XFA00D2
    16384212: 0x2,  # Lifting Gem -> Ivan == 0XFA00D4
    16384214: 0x1,  # Orb of Force -> Garet == 0XFA00D6
    16384216: 0x0,  # Catch Beads -> Isaac == 0XFA00D8
    16384218: 0x7,  # Douse Drop -> Piers == 0XFA00DA
    16384220: 0x7,  # Frost Jewel -> Piers == 0XFA00DC
}
"""

RESTRICTIONS_MAP = {
    'no-empty': LocationRestriction.NoEmpty,
    'no-mimic': LocationRestriction.NoMimic,
    'no-summon': LocationRestriction.NoSummon,
    'no-money': LocationRestriction.NoMoney,
}


@dataclass(frozen=True, slots=True, kw_only=True)
class ChestLocation(BaseLocation):
    """

    Note:
        There are some locations that have two entries in item_locations.json.
        For example "0xf57", which is an "Oil Drop" in "Lemurian Ship".
        These are just two different versions of the same chest. We can never open both.
        We're only using the *first* entry. The ap_id is therefore that first entries' "addr".
        If the rando ever decides to swap those values, it'll change the datapackage and break the PopTracker.
        TODO: Maybe we should have some kind of constant values for these?
    """

    restrictions = LocationRestriction.NoEmpty | LocationRestriction.NoMimic | LocationRestriction.NoSummon

    ap_id: int
    event_type: int
    flag: int  # EWRAM
    is_hidden: bool
    is_key: bool
    is_major: bool
    location_type: LocationType = LocationType.Item  # TODO: use the right one
    name: str  # TODO: LocationName?
    rando_flag: int
    vanilla_item_id: int
    # there's more data in the data file, but we currently don't use those

    @classmethod
    def _build_row(cls, entry: dict) -> Self:
        return cls(
            ap_id=entry['addr'],
            event_type=entry['eventType'],
            flag=entry['id'],  # TODO: Pretty sure we need to overwrite some of these
            is_hidden=entry['isHidden'],
            is_key=entry['isKeyItem'],
            is_major=entry['isMajorItem'],
            name=entry['vanillaName'],
            rando_flag=entry['id'],  # also matches the key of the item_locations.json entry
            vanilla_item_id=entry['vanillaContents'],
        )

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        rows = []
        for loc in read_json('data/item_locations.json').values():
            loc = loc[0]  # see docstring
            row = cls._build_row(loc)
            rows.append(row)

        return tuple(rows)
