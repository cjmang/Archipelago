from dataclasses import dataclass
from enum import IntEnum, IntFlag, StrEnum, auto

from BaseClasses import ItemClassification


class RegionData:
    name: str
    locations: list[str]
    exits: list[str]

    def __init__(self, _name: str, _locations: list[str] = None, _exits: list[str] = None):
        if _locations is None:
            _locations = []

        if _exits is None:
            _exits = []

        self.name = _name
        self.locations = _locations
        self.exits = _exits


class EntranceData:
    source_entrance: str
    target: str

    def __init__(self, _source_entrance: str, _target: str):
        self.source_entrance = _source_entrance
        self.target = _target


class ItemCategory(StrEnum):
    # TODO: Capitalize while replacing the auto()
    djinn = auto()
    summons = auto()
    learned_psynergy = auto()
    psynergy_items = auto()
    events = auto()
    characters = auto()
    mimics = auto()
    other_progression = auto()
    useful_consumables = auto()
    forge_materials = auto()
    class_change_items = auto()
    useful_remainder = auto()
    rusty_items = auto()
    stat_boosters = auto()
    shop_only = auto()
    forge_only = auto()
    lucky_only = auto()
    non_vanilla = auto()
    vanilla_coins = auto()
    misc = auto()
    remainder = auto()


class CharacterIndex(IntEnum):
    ISAAC = 0
    GARET = 1
    IVAN = 2
    MIA = 3
    FELIX = 4
    JENNA = 5
    SHEBA = 6
    PIERS = 7


class ItemType(IntEnum):
    Consumable = 0
    Weapon = 1
    Armor = 2
    Shield = 3
    Helm = 4
    Boots = 5
    PsynergyItem = 6
    Trident = 7
    Ring = 8
    Shirt = 9
    Class = 10
    KeyItem = 11
    Psynergy = 12
    Djinn = 13
    Event = 14
    Character = 15
    Mimic = 16
    Summon = 17


class LocationType(StrEnum):
    Item = 'Item'
    Event = 'Event'
    Djinn = 'Djinn'
    Psynergy = 'Psynergy'
    Hidden = 'Hidden'
    Trade = 'Trade'
    Character = 'Character'


class LocationRestriction(IntFlag):
    NONE = 0  # rename to "Unrestricted"
    NoEmpty = auto()
    NoMimic = auto()
    NoSummon = auto()
    NoMoney = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class ItemData:
    id: int  # AP item ID
    name: str
    type: ItemType
    classification: ItemClassification
    category: ItemCategory
    shuffled: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class LocationData:
    id: int  # AP item ID
    name: str  # (or enum?)
    type: LocationType
    flag: int  # EWRAM
    rando_flag: int  # The flag/addr in karanum rando, seems like it can be an ID instead of a flag?
    restrictions: LocationRestriction


class ItemFlag(IntFlag):
    NONE = 0
    Cursed = auto()  # 1 "Curses on pickup"
    Sticky = auto()  # 2 "Unremovable"
    Rare = auto()  # 4 "If dropped, can be bought back from shops"
    Important = auto()  # 8 "Cannot be dropped"
    Stackable = auto()  # 16 "Carry up to 30"
    NoTransfer = auto()  # 32 "Cannot be transfered from GS1 to GS2"
    UnusedOne = auto()
    UnusedTwo = auto()


class PsynergyID(IntEnum):
    GROWTH = 12
    DOUSE = 33
    FROST = 24
    WHIRLWIND = 78
    LASH = 133
    POUND = 134
    TREMOR = 135
    SCOOP = 136
    CYCLONE = 137
    PARCH = 138
    SAND = 139
    MIND_READ = 141
    FORCE = 142
    LIFT = 143
    REVEAL = 144
    HALT = 145
    CLOAK = 146
    CARRY = 147
    CATCH = 148
    BURST = 151
    GRIND = 152
    HOVER = 153
    BLAZE = 154
    TELEPORT = 156


class ElementType(IntEnum):
    Earth = 0
    Water = 1
    Fire = 2
    Air = 3


class TreasureType(IntEnum):
    # matches the eventType in item_locations.json
    JAR = 0x2  # 2
    BARREL = 0x3  # 3
    GRAVE = 0x8  # 8
    BOX = 0xD  # 13
    CHEST = 0x80  # 128
    MIMIC_CHEST = 0x81  # 129
    FIELD_ITEM = 0x83  # 131 (via scoop, cyclone, on a pedestal like the "Center prong", ...)
    PICKUP = 0x84  # 132 (chars, summon tablets, psynergy)
    SUNKEN = 0x85  # 133 (rusty gear)
