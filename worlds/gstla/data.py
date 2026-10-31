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


from dataclasses import dataclass

from worlds.gstla.gstla_types import ItemData, ItemType

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
class NewDjinnItemData(ItemData):
    # djinns, obviously
    # djinn.json
    # internal_item_data.djinn_items
    # id: mem address
    pass


@dataclass(frozen=True, kw_only=True)
class NewEventItemData(ItemData):
    pass


@dataclass(frozen=True, kw_only=True)
class NewCharacterItemData:
    id: int
    name: str
    flag: int
    addr: int
    item_type: ItemType = ItemType.Character
