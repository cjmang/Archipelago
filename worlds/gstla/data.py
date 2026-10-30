# Whew. So:
# game_data: has more Datums than a calendar, loads them each with their respective json
# generate_cody: sort the game_data stuff into buckets, does the classifications and then renders the jinja templates
# internal_item_data.py: the generated *Internal* ItemData, DjinnItemData & EventItemData classes and objects
# item_data: has more wrappers and converts things and overrides and filler stuff
# items: is then another layer on top of that?

from dataclasses import dataclass

from BaseClasses import ItemClassification


@dataclass(frozen=True, kw_only=True)
class NewItemData:
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
    pass


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
