# TODO: delete this together with gen/, etc

import unittest

from worlds.gstla.gen import item_data as legacy_item_data
from worlds.gstla.gstla_types import ItemCategory
from worlds.gstla.new_game_data.equipment import NAME_OVERRIDES
from worlds.gstla.new_game_data.loader import load_game_data as load_new_game_data

LEGACY_CATEGORY_MAPPING: dict[ItemCategory, str] = {
    ItemCategory.characters: 'characters',
    ItemCategory.class_change_items: 'class_change_items',
    ItemCategory.djinn: 'djinn_items',
    ItemCategory.events: 'events',
    ItemCategory.forge_materials: 'forge_materials',
    ItemCategory.forge_only: 'forge_only',
    ItemCategory.learned_psynergy: 'psyenergy_list',
    ItemCategory.lucky_only: 'lucky_only',
    ItemCategory.mimics: 'mimics',
    ItemCategory.misc: 'misc',
    ItemCategory.non_vanilla: 'non_vanilla',
    ItemCategory.other_progression: 'other_progression',
    ItemCategory.psynergy_items: 'psyenergy_as_item_list',
    ItemCategory.remainder: 'remainder',
    ItemCategory.rusty_items: 'rusty_items',
    ItemCategory.shop_only: 'shop_only',
    ItemCategory.stat_boosters: 'stat_boosters',
    ItemCategory.summons: 'summon_list',
    ItemCategory.useful_consumables: 'useful_consumables',
    ItemCategory.useful_remainder: 'useful_remainder',
    ItemCategory.vanilla_coins: 'vanilla_coins',
}

IGNORE_ORDERS_FOR_CATEGORIES = [
    # in these 3 categories the order changed, but that is a-okay.
    # datapackage will change, but oh well.
    ItemCategory.stat_boosters,  # [192, 193, 194, 195, 196, 191] != [191, 192, 193, 194, 195, 196]
    ItemCategory.useful_consumables,  # [186, 189, 190, 183] != [183, 186, 189, 190]
    #
    # [384, 259, 388, 7, 10, 266, 394, 279, 281,[124 chars] 383]
    # !=
    # [7, 10, 26, 259, 266, 279, 281, 283, 287, [124 chars] 414]
    ItemCategory.useful_remainder,
]


class TestNewGameData(unittest.TestCase):
    maxDiff = None

    def test_new_matches_old(self):
        data = load_new_game_data()
        for category, old_list_name in LEGACY_CATEGORY_MAPPING.items():
            with self.subTest(category=category.name):
                expected = {
                    # old rusty stuff
                    item.id: (NAME_OVERRIDES.get(item.id, item.name), item.type.name, item.progression.name)
                    for item in getattr(legacy_item_data, old_list_name)
                }
                actual = {
                    item.id: (item.name, item.type.name, item.classification.name)
                    for item in data.item_by_id.values()
                    if item.category == category
                }

                self.assertEqual(expected, actual)
                if category.name in IGNORE_ORDERS_FOR_CATEGORIES:
                    self.assertEqual(sorted(expected), sorted(actual))
                else:
                    self.assertEqual(list(expected), list(actual))
