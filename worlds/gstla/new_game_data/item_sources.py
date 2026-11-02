from functools import cache
from typing import NamedTuple

from .base import BaseItem
from .forgeables import load_forge_mapping

LUCKY_MEDAL_IDS: set[int] = {
    # GS1
    # 23, # Assassin Blade
    # 37, # Burning Axe
    # 48, # Grevious Mace
    # 81, # Spirit Armor
    # 97, # Kimono
    # 108, # Cocktail Dress
    # 124, # Earth Shield
    # 133, # Battle Gloves
    # 142, # Guardian Armlet
    # 152, # Adept's Helm
    # 160, # Ninja Hood
    # 171, # Glittering Tiara
    #
    # GS2
    183,  # Potion
    186,  # Psy Crystal
    189,  # Water of Life
    280,  # Hestia Blade
    302,  # Mighty Axe
    320,  # Fireman's Pole
    327,  # Leda's Bracelet
    335,  # Erebus Armor
    341,  # Wild Coat
    342,  # Floral Dress
    359,  # Aegis Shield
    364,  # Crafted Gloves
    380,  # Minerva Helm
    387,  # Crown of Glory
    395,  # Brilliant Circlet
}
LUCKY_WHEEL_IDS: set[int] = {
    181,  # Nut
    182,  # Vial
    183,  # Potion
    188,  # Elixer
    186,  # Psy Crystal
    189,  # Water of Life
    258,  # Fur Boots
    257,  # Quick Boots
    256,  # Hyper Boots
    252,  # Running Shirt
    251,  # Silk Shirt
    250,  # Mythril Shirt
    264,  # Sleep Ring
    263,  # War Ring
    262,  # Adept Ring
}
GAME_TICKET_ID: int = 228


class ItemSources(NamedTuple):
    chests: frozenset[int]
    shops: frozenset[int]
    forge: frozenset[int]
    lucky: frozenset[int]


@cache
def get_item_sources() -> ItemSources:
    # mainly used for equipment and normal items
    chests = {
        location['vanillaContents']
        for locations in BaseItem.read_json('data/item_locations.json').values()
        for location in locations
        if location['vanillaName'] != 'Mimic'
    }
    chests.add(GAME_TICKET_ID)

    shops = {
        item_id
        for shop in BaseItem.read_json('data/shops.json')
        for item_id in shop['items'] + shop['artifacts']
        if item_id != 0
    }

    # read directly from file (?)
    forge = {result_id for result_ids in load_forge_mapping().values() for result_id in result_ids}

    return ItemSources(
        chests=frozenset(chests),
        forge=frozenset(forge),
        lucky=frozenset(LUCKY_MEDAL_IDS | LUCKY_WHEEL_IDS),
        shops=frozenset(shops),
    )
