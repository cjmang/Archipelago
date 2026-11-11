from typing import cast

from test.bases import WorldTestBase
from worlds.gstla.world import GSTLAWorld


class GSTestBase(WorldTestBase):
    game = 'Golden Sun The Lost Age'

    def _check_for_unknown_option_keys(self):
        unknown_options = self.options.keys() - GSTLAWorld.options_dataclass.type_hints.keys()
        self.assertFalse(
            unknown_options, f'{type(self).__name__}.options has unknown option names: {sorted(unknown_options)}'
        )

    def world_setup(self, seed: int | None = None) -> None:
        self._check_for_unknown_option_keys()
        super().world_setup(seed)

    def get_world(self) -> GSTLAWorld:
        # Can't just retype world in this class
        return cast('GSTLAWorld', self.world)
