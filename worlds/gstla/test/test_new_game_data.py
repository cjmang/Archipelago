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


class TestNewGameData(unittest.TestCase):
    # TODO: useful_consumables, useful_remainder, stat_boosters don't match yet?
    def test_new_matches_old(self):
        data = load_new_game_data()
        for category, old_list_name in LEGACY_CATEGORY_MAPPING.items():
            with self.subTest(category=category):
                expected = [
                    # old rusty stuff
                    (item.id, NAME_OVERRIDES.get(item.id, item.name), item.type, item.progression)
                    for item in getattr(legacy_item_data, old_list_name)
                ]
                actual = [
                    (item.id, item.name, item.type, item.classification)
                    for item in data.item_by_id.values()
                    if item.category == category
                ]
                self.assertEqual(expected, actual)
