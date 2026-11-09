import unittest

from worlds.gstla.gen.location_data import event_name_to_data, location_id_to_data, location_name_to_data
from worlds.gstla.gstla_types import LocationRestriction
from worlds.gstla.names import LocationName
from worlds.gstla.new_game_data.loader import load_game_data

IGNORE_RESTRICTIONS = [
    # these are the ones where the line
    # (loc['id'] | 0xF00) == 0x100
    # never worked, so let's ignore 'em.
    # Everything else is fine with them.
    LocationName.Contigo_Carry_Stone,
    LocationName.Contigo_Lifting_Gem,
    LocationName.Contigo_Orb_of_Force,
    LocationName.Contigo_Catch_Beads,
    LocationName.Kibombo_Douse_Drop,
    LocationName.Kibombo_Frost_Jewel,
]


class TestLocationMigration(unittest.TestCase):
    """
    TODO: Delete this once we migrated everything over to the new stuff
    """

    def test_same_ids_and_names(self):
        game_data = load_game_data()
        self.assertEqual(set(location_id_to_data), set(game_data.location_by_id))
        self.assertEqual(set(location_name_to_data), set(game_data.location_by_name))
        self.assertEqual(set(event_name_to_data), set(game_data.event_by_name))

    def test_fields_match(self):
        game_data = load_game_data()
        for name, new in game_data.location_by_name.items():
            old = location_name_to_data[name]
            with self.subTest(name):
                self.assertEqual(old.ap_id, new.id)
                self.assertEqual(old.loc_type, new.type)
                self.assertEqual(old.flag, new.flag)
                self.assertEqual(old.rando_flag, new.rando_flag)
                if name in IGNORE_RESTRICTIONS:
                    continue
                old_res = LocationRestriction(int(old.restrictions))
                new_res = LocationRestriction(int(new.restrictions))
                self.assertEqual(old_res, new_res, f"Restrictions for {name} don't match.")

    def test_event_fields_match(self):
        game_data = load_game_data()
        for name, new in game_data.event_by_name.items():
            old = event_name_to_data[name]
            with self.subTest(name):
                self.assertEqual(old.ap_id, new.id)
                self.assertEqual(old.flag, new.flag)
                old_res = LocationRestriction(int(old.restrictions))
                new_res = LocationRestriction(int(new.restrictions))
                self.assertEqual(old_res, new_res, f"Restrictions for {name} don't match.")
