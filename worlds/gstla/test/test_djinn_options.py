from worlds.gstla.game_data.loader import load_game_data
from worlds.gstla.gstla_types import LocationType
from worlds.gstla.items import GSTLAItem, ItemType
from worlds.gstla.test import GSTestBase


class TestDjinnOptions(GSTestBase):
    def test_ensure_djinn_in_djinn(self):
        game_data = load_game_data()
        world = self.get_world()
        for djinn in game_data.locations_by_type[LocationType.Djinn]:
            self.assertEqual(LocationType.Djinn, djinn.type)
            ap_loc = world.get_location(djinn.name)
            ap_item = ap_loc.item
            self.assertIsInstance(ap_item, GSTLAItem)
            self.assertEqual(ItemType.Djinn, ap_item.item_data.type)


class TestVanillaDjinn(GSTestBase):
    options = {'shuffle_djinn': 0}

    def test_ensure_vanilla_djinn(self):
        game_data = load_game_data()
        world = self.get_world()
        for djinn in game_data.locations_by_type[LocationType.Djinn]:
            self.assertEqual(LocationType.Djinn, djinn.type)
            ap_loc = world.get_location(djinn.name)
            ap_item = ap_loc.item
            self.assertIsInstance(ap_item, GSTLAItem)
            self.assertEqual(ItemType.Djinn, ap_item.item_data.type)
            self.assertTrue(djinn.name.endswith(ap_item.name), f'Loc Name: {djinn.name} Item Name: {ap_item.name}')
