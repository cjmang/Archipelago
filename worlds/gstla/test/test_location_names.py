import unittest

from worlds.gstla.new_game_data.loader import load_game_data
from worlds.gstla.new_game_data.location_names import loc_names_by_id


class TestLocationNames(unittest.TestCase):
    def test_matching_locations(self):
        game_data = load_game_data()
        loader_ids = set(game_data.chest_locations) | set(game_data.djinn_locations) | set(game_data.event_locations)
        hardcoded_ids = set(loc_names_by_id)
        self.assertEqual(set(), loader_ids - hardcoded_ids, 'loc_names_by_id is missing entries')
        self.assertEqual(set(), hardcoded_ids - loader_ids, 'loc_names_by_id has unused entries')
