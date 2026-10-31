from dataclasses import dataclass
from enum import IntEnum, StrEnum, auto

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
    # TODO: Merge with deathlink.CharacterIndex after deathlink merge
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
    PsyenergyItem = 6
    Trident = 7
    Ring = 8
    Shirt = 9
    Class = 10
    KeyItem = 11
    Psyenergy = 12
    Djinn = 13
    Event = 14
    Character = 15
    Mimic = 16
    Summon = 17


@dataclass(frozen=True, slots=True, kw_only=True)
class ItemData:
    id: int  # AP item ID
    name: str
    type: ItemType
    classification: ItemClassification
    category: ItemCategory
