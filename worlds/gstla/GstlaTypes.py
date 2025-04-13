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
    SCREEN_EDGE_WALK = 3 << 3
    SCREEN_EDGE_SHIP = 4 << 3
    FALL = 5 << 3
    LADDER = 6 << 3
    TELEPORT = 7 << 3
    CYCLONE = 8 << 3
    GEYSER = 9 << 3

    #Connectors
    CONNECTOR1 = 1 << 7 #Daila
    CONNECTOR2 = 2 << 7 #Madra Drawbridge
    CONNECTOR3 = 3 << 7 #Naribwe
    CONNECTOR4 = 4 << 7 #Yallam
    CONNECTOR5 = 5 << 7 #Prox
    CONNECTOR6 = 6 << 7 #Atteka Inlet, alteast 1 connection requires ship
    CONNECTOR7 = 7 << 7 #Sea of Time, atleast 1 connection requires ship
    CONNECTOR8 = 8 << 7 #Gondowan Cliffs (Sea), atleast 1 connection requires ship
    CONNECTOR9 = 9 << 7 #Dehkan Plateau
    CONNECTOR10 = 10 << 7 #Osenia Cliffs
    CONNECTOR11 = 11 << 7 #Yampi Desert
    CONNECTOR12 = 12 << 7 #Gondown Cliffs (Land)
    CONNECTOR13 = 13 << 7 #Kibombo Mountains
    CONNECTOR14 = 14 << 7 #Shaman Villaga Cave

    #Bitmasks
    DIRECTION_MASK = 7
    TRANSITION_MASK = 15 << 3
    CONNECTORS_MASK = 15 << 7

class EntranceData:
    source_entrance: str
    target: str
    gs_id: str
    rando_group: int
    rando_type: EntranceType
    target_rando_group: int
    target_name: str

    def __init__(self, _source_entrance: str, _target: str, _gs_id: int = None, _ap_rando_group: int = 0, _ap_target_rando_group: int = 0, _ap_target_name: str = None, _ap_rando_type: EntranceType = EntranceType.TWO_WAY ):
        self.source_entrance = _source_entrance
        self.target = _target
        self.gs_id = _gs_id
        self.rando_group = _ap_rando_group
        self.rando_type = _ap_rando_type
        self.target_rando_group = _ap_target_rando_group
        self.target_name = _ap_target_name
