from typing import List, Dict, Optional, TYPE_CHECKING
from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from enum import IntEnum

class RegionData:
    name: str
    locations: List[str]
    exits: List[str]
    gs_name: str
    gs_id: int

    def __init__(self, _name: str, _locations: List[str] = None, _exits: List[str] = None, _gs_name: str = None, _gs_id: int = None):
        if _locations is None:
            _locations = []

        if _exits is None:
            _exits = []

        if _gs_name is None:
            _gs_name = _name

        self.name = _name
        self.locations = _locations
        self.exits = _exits
        self.gs_name = _gs_name
        self.gs_id = _gs_id


class ERTestGroups(IntEnum):
    #Directions
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    UP = 5
    DOWN = 6

    #Overworld
    OW_WALK = 1 << 3
    OW_SHIP = 2 << 3

    #Dungeon/Village
    SCREEN_EDGE_SHIP = 3 << 3
    SCREEN_EDGE_WALK = 4 << 3
    DOOR = 5 << 3
    RISE = 6 << 3
    FALL = 7 << 3
    LADDER = 8 << 3
    TELEPORT = 9 << 3
    CYCLONE = 10 << 3
    GEYSER = 11 << 3

    #Bitmasks
    DIRECTION_MASK = OW_WALK - 1
    TRANSITION_MAST = ~0 << 3


directionally_matched_group_lookup = {
    ERTestGroups.OW_WALK: [ERTestGroups.OW_WALK],
    ERTestGroups.OW_SHIP: [ERTestGroups.OW_SHIP],
    ERTestGroups.SCREEN_EDGE_SHIP: [ERTestGroups.SCREEN_EDGE_SHIP],
    ERTestGroups.SCREEN_EDGE_WALK: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.DOOR: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.RISE: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.FALL: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.LADDER: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.TELEPORT: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.CYCLONE: [ERTestGroups.SCREEN_EDGE_WALK, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE]
}

class EntranceData:
    source_entrance: str
    target: str
    gs_id: str
    rando_group: int
    rando_type: EntranceType

    def __init__(self, _source_entrance: str, _target: str, _gs_id: int = None, _ap_rando_group: int = 0, _ap_rando_type: EntranceType = EntranceType.TWO_WAY ):
        self.source_entrance = _source_entrance
        self.target = _target
        self.gs_id = _gs_id
        self.rando_group = _ap_rando_group
        self.rando_type = _ap_rando_type