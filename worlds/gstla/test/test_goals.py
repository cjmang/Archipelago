from BaseClasses import CollectionState
from worlds.gstla.names import ItemName, LocationName
from worlds.gstla.test import GSTestBase

GOALS = ['Doom Dragon', 'Reunion', 'Briggs', 'Serpent']


class TestRandomGoals(GSTestBase):
    auto_construct = False
    options = {'goal': GOALS, 'random_goals': 2}

    def test_goal_option_matches_randomized_goals(self):
        self.world_setup()
        world = self.get_world()
        slot_goal = world.fill_slot_data()['goal']
        self.assertEqual(2, len(world.options.goal.value))
        self.assertEqual(world.options.goal.value, set(slot_goal['flags']))


class TestDjinnHunt(GSTestBase):
    options = {'goal': ['Djinn Hunt'], 'djinn_hunt_count': 2}

    def test_goal_needs_the_djinn_count(self):
        victory_event = self.get_world().get_location(LocationName.Victory_Event)
        state = CollectionState(self.multiworld)

        state.collect(self.get_item_by_name(ItemName.Flint), prevent_sweep=True)
        self.assertFalse(victory_event.access_rule(state))

        state.collect(self.get_item_by_name(ItemName.Granite), prevent_sweep=True)
        self.assertTrue(victory_event.access_rule(state))


class TestSummonHunt(GSTestBase):
    options = {'goal': ['Summon Hunt'], 'summon_hunt_count': 2}

    def test_goal_needs_the_summon_count(self):
        victory_event = self.get_world().get_location(LocationName.Victory_Event)
        state = CollectionState(self.multiworld)

        state.collect(self.get_item_by_name(ItemName.Zagan), prevent_sweep=True)
        self.assertFalse(victory_event.access_rule(state))

        state.collect(self.get_item_by_name(ItemName.Megaera), prevent_sweep=True)
        self.assertTrue(victory_event.access_rule(state))
