from dataclasses import dataclass
from typing import Self

from worlds.gstla.gstla_types import CharacterIndex, LocationRestriction, LocationType
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

"""

RESTRICTIONS_MAP = {
    'no-empty': LocationRestriction.NoEmpty,
    'no-mimic': LocationRestriction.NoMimic,
    'no-summon': LocationRestriction.NoSummon,
    'no-money': LocationRestriction.NoMoney,
}

# A few locations use different flags than stated in the item_locations.json file
# E.g. character starting inventories
FLAG_OVERWRITES = {
    0xFA00CA: CharacterIndex.FELIX,  # Shaman's Rod
    0xFA00CC: CharacterIndex.SHEBA,  # Mind Read
    0xFA00CE: CharacterIndex.SHEBA,  # Whirlwind
    0xFA00D0: CharacterIndex.FELIX,  # Growth
    0xFA00D2: CharacterIndex.MIA,  # Carry Stone
    0xFA00D4: CharacterIndex.IVAN,  # Lifting Gem
    0xFA00D6: CharacterIndex.GARET,  # Orb of Force
    0xFA00D8: CharacterIndex.ISAAC,  # Catch Beads
    0xFA00DA: CharacterIndex.PIERS,  # Douse Drop
    0xFA00DC: CharacterIndex.PIERS,  # Frost Jewel
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
            flag=FLAG_OVERWRITES.get(entry['addr'], entry['id']),
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
