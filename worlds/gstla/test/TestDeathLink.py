from io import BytesIO, StringIO

from worlds.gstla.test import GSTestBase


class TestDeathLinkEnabled(GSTestBase):
    options = {"death_link": 1}  # noqa: RUF012

    def test_deathlink_enabled(self):
        world = self.get_world()
        self.assertEqual(1, world.fill_slot_data()["options"]["death_link"])


class TestDeathLinkDoesNotAffectRandoData(GSTestBase):
    """
    Our DeathLink implementation only uses the BizHawk bridge and does not
    change anything in the ROM itself.
    So we just make sure the actual ROM bytes stay the same.
    """

    auto_construct = False

    def test_rom_bytes_unchanged(self):
        self.options = {"death_link": 0}
        self.world_setup(seed=1)
        rando_off = BytesIO()
        self.get_world()._generate_rando_data(rando_off, StringIO())

        self.options = {"death_link": 1}
        self.world_setup(seed=1)
        rando_on = BytesIO()
        self.get_world()._generate_rando_data(rando_on, StringIO())

        self.assertEqual(rando_off.getvalue(), rando_on.getvalue())

