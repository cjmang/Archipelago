import json
from dataclasses import fields

from NetUtils import convert_to_base_types
from worlds.gstla.options import (
    AnemosAccess,
    DjinnLogic,
    GSTLAOptions,
    ItemShuffle,
    OmitLocations,
    RevealHiddenItem,
    ShipWings,
    ShortcutMagmaRock,
    ShortcutMarsLighthouse,
    StartWithShip,
)
from worlds.gstla.test import GSTestBase
from worlds.gstla.world import SLOT_DATA_FIELDS


class TestUniversalTrackerSlotData(GSTestBase):
    auto_construct = False
    options = {
        'item_shuffle': ItemShuffle.option_all_chests_and_tablets,
        'reveal_hidden_item': RevealHiddenItem.option_false,
        'omit_locations': OmitLocations.option_omit_superbosses_and_inner_sanctum,
        'lemurian_ship': StartWithShip.option_available_from_start,
        'start_with_wings_of_anemos': ShipWings.option_true,
        'shortcut_mars_lighthouse': ShortcutMarsLighthouse.option_true,
        'shortcut_magma_rock': ShortcutMagmaRock.option_true,
        'anemos_inner_sanctum_access': AnemosAccess.option_randomized,
        'djinn_logic': DjinnLogic.special_range_names['hard'],
        'goal': ['Briggs', 'Dullahan', 'Djinn Hunt', 'Summon Hunt'],
        'djinn_hunt_count': 30,
        'summon_hunt_count': 5,
    }

    def test_slot_data_is_applied_to_options(self):
        # see `_apply_fake_universal_tracker_slot_data()` for how this works
        self.world_setup()
        original = self.get_world()
        expected_options = {
            option.name: getattr(original.options, option.name).value
            for option in fields(GSTLAOptions)
            if option.name in SLOT_DATA_FIELDS
        }
        expected_goal = set(original.options.goal.value)
        slot_data = json.loads(json.dumps(convert_to_base_types(original.fill_slot_data())))

        self.options = {}
        self.world_setup()
        regenerated_world = self.get_world()
        setattr(self.multiworld, 're_gen_passthrough', {regenerated_world.game: slot_data})  # noqa: B010

        regenerated_world._apply_fake_universal_tracker_slot_data()

        for name, expected_opt in expected_options.items():
            self.assertEqual(expected_opt, getattr(regenerated_world.options, name).value)
        self.assertEqual(expected_goal, regenerated_world.options.goal.value)
        self.assertEqual(0, regenerated_world.options.random_goals.value)
