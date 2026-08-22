from __future__ import annotations

import unittest

from worlds.gstla.DeathLink import get_current_hp_address, get_current_hp_ratio_address


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
