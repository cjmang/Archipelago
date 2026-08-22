from __future__ import annotations

import unittest
from io import BytesIO, StringIO

from worlds.gstla.DeathLink import get_current_hp_address, get_current_hp_ratio_address
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


class TestCharacterHPAddresses(unittest.TestCase):
    """Indexes here are static. They won't get shuffled by the randomizer."""

    def test_index_0_isaac(self):
        self.assertEqual(0x558, get_current_hp_address(0))

    def test_index_2_ivan(self):
        self.assertEqual(0x7F0, get_current_hp_address(2))

    def test_index_4_felix(self):
        self.assertEqual(0xA88, get_current_hp_address(4))

    def test_index_6_sheba(self):
        self.assertEqual(0xD20, get_current_hp_address(6))


class TestCharacterHPRatioAddresses(unittest.TestCase):
    def test_index_0_isaac(self):
        self.assertEqual(0x534, get_current_hp_ratio_address(0))

    def test_index_2_ivan(self):
        self.assertEqual(0x7CC, get_current_hp_ratio_address(2))

    def test_index_4_felix(self):
        self.assertEqual(0xA64, get_current_hp_ratio_address(4))

    def test_index_6_sheba(self):
        self.assertEqual(0xCFC, get_current_hp_ratio_address(6))
