from abc import ABC
from collections.abc import Callable
from typing import NamedTuple

from BaseClasses import MultiWorld
from worlds.gstla.gen.internal_location_data import always_on
from worlds.gstla.gstla_types import LocationRestriction, LocationType


class LocationDatum(NamedTuple):
    flag: int
    map_id: int
    locked: bool
    is_summon: bool
    is_key_item: bool
    is_major_item: bool
    is_hidden: bool
    addr: list[int]
    event_type: int
    location_id: int
    id: int
    vanilla_contents: int
    vanilla_name: str
    map_name: str
    restrictions: int


class InternalLocationData(NamedTuple):
    flag: int
    id: int | None
    ap_id: int
    addresses: list[int]
    event_type: int
    vanilla_contents: int
    is_key: bool
    is_major: bool
    loc_type: LocationType = LocationType.Item
    restrictions: LocationRestriction = LocationRestriction.NONE
    event: bool = False
    included: Callable[[MultiWorld, int], bool] = always_on


class BaseLocation(ABC):
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

    # the index/spot of the "obtained" flag in EWRAM incl. offset
    # also named "rando_flag" in other spots
    rando_flag: int  # previously "rando_flag" (rename to flag_index?)
