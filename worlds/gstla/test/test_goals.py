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
