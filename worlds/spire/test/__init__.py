from test.bases import WorldTestBase
from worlds.spire import SpireWorld


class SpireTestBase(WorldTestBase):
    game = 'Slay the Spire'
    world = SpireWorld

    options = {
        'character': 0,
        'final_act': 1
    }

