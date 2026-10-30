# Whew. So: from json files upwards towards the world/client
# game_data: has more Datums than a calendar, loads them each with their respective json
# generate_cody: sort the game_data stuff into buckets, does the classifications and then renders the jinja templates
# internal_item_data.py: the generated *Internal* ItemData, DjinnItemData & EventItemData classes and objects
# item_data: has more wrappers and converts things and overrides and filler stuff
# items: is then another layer on top of that?
#
#
# The masterplan:
# json files -> data.py (or data pkg) -> some build() step so that it's somewhat lazy -> items/world/client/whatever
# At the same time, we still need some names.py (or names pkg) so that we can use enums/constants without going crazy
# I want to have the build step in between so that we can more easily just import and build what I really need.
# Maybe build() can live in worlds directly, or somewhere else, idk yet.
# So overall we should reduce the overall layers by 2 or 3 or 2.5.
# Also need a test to compare the names.py (or names pkg) with the json files.
# Just in case something changes in those on updates.



import json
from dataclasses import dataclass
from enum import IntEnum
from typing import Self

from BaseClasses import ItemClassification


# TODO: Move this somewhere else like gstla_types
class NewItemType(IntEnum):
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


@dataclass(frozen=True, kw_only=True)
class NewItemData:
    _file_path = 'data/items.json'
    _raw_data = {}

    def _load_from_file(self):
        with open(self._file_path, 'r') as f:
            self.raw_data = json.load(f)

    def _serizalize_data(self) -> list[Self]:
        # do something to return a list of Self or something
        return []

    # the vanilla stuff like consumables, gear, key items
    # items.json
    # excluding EXCLUDED_ITEMS
    # id: normal game ids
    # generate_code.CLASSIFICATION_OVERRIDES
    # for name:, there is also SPECIAL_NAMES

    # also somewhat contains Psy(e)nergyItem
    # but id is "item['useEffect'] + 0xE00"
    # this is the stuff that's learned by an item
    # like Frost Jewel, Pound Cube, etc

    # there's also inherent Psy(e)nergies that the chars have by default
    # like Whirlwind, Mind Read, etc

    # also contains djinn, which makes sense but what is DjinnItemData for? events?

    # summons:
    # summons.json

    # chars
    # also see GameData._setup_characters

    # mimics

    # coins


@dataclass(frozen=True, kw_only=True)
class NewDjinnItemData(NewItemData):
    # djinns, obviously
    # djinn.json
    # internal_item_data.djinn_items
    # id: mem address
    pass


@dataclass(frozen=True, kw_only=True)
class NewEventItemData(NewItemData):
    pass


@dataclass(frozen=True, kw_only=True)
class NewCharacterItemData:
    id: int
    name: str
    flag: int
    addr: int
    item_type: NewItemType = NewItemType.Character
