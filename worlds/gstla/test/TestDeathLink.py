from __future__ import annotations

import unittest
from collections.abc import Sequence

from worlds.gstla.DeathLink import (
    FIELD_DEATH_NARRATION_COUNT_ADDR,
    FIELD_DEATH_NARRATION_LIST_ADDR,
    FIELD_DEATH_REQUEST_ADDR,
    FIELD_DEATH_REQUEST_VALUE,
    FIELD_DEATH_SURVIVOR_COUNT_ADDR,
    GAME_STATE_READS,
    IN_BATTLE_BIT,
    GameState,
    MemoryWrite,
    _build_field_death_request_writes,
    _build_multi_zero_hp_writes,
    get_current_hp_address,
    get_current_hp_ratio_address,
)
from worlds.gstla.DeathLink import (
    CharacterIndex as Character,
)


def _little_endian_u16(value: int) -> bytes:
    return value.to_bytes(2, "little")


def _recruited(*characters: Character) -> int:
    return sum(1 << character for character in characters)


def _hp_values(*dead: Character) -> tuple[int, ...]:
    return tuple(0 if character in dead else _LIVE_HP[character] for character in Character)


def _hp_reads(*dead: Character) -> list[bytes]:
    return [_little_endian_u16(hp) for hp in _hp_values(*dead)]


_LIVE_HP = (11, 22, 33, 44, 55, 66, 77, 88)  # just arbitry HP values corresponding to each char
_ZERO_BYTES = _little_endian_u16(0)
_ARMED_REQUEST_BYTES = _little_endian_u16(FIELD_DEATH_REQUEST_VALUE)

_DEFAULT_PARTY = _recruited(Character.FELIX, Character.SHEBA)
_EVERYONE = tuple(Character)
_NOBODY = _recruited()


def _game_state(
    recruitment: int,
    in_battle: int = 0x00,
    field_death_request: int = 0x00,
    survivor_count: int = 0,
    dead: Sequence[Character] = (),
) -> GameState:
    return GameState(
        recruitment=recruitment,
        in_battle=in_battle,
        field_death_request=field_death_request,
        survivor_count=survivor_count,
        hp=_hp_values(*dead),
    )


class TestCharacterHPAddresses(unittest.TestCase):
    def test_current_hp(self):
        self.assertEqual(0x558, get_current_hp_address(Character.ISAAC))
        self.assertEqual(0xA88, get_current_hp_address(Character.FELIX))
        self.assertEqual(0xD20, get_current_hp_address(Character.SHEBA))

    def test_current_hp_ratio(self):
        self.assertEqual(0x534, get_current_hp_ratio_address(Character.ISAAC))
        self.assertEqual(0xA64, get_current_hp_ratio_address(Character.FELIX))
        self.assertEqual(0xCFC, get_current_hp_ratio_address(Character.SHEBA))

    def test_current_hp_to_ratio_address_offset(self):
        self.assertEqual(0x24, get_current_hp_address(Character.ISAAC) - get_current_hp_ratio_address(Character.ISAAC))


class TestRecruitedCharacters(unittest.TestCase):
    _NO_BITS_SET = 0x00
    _BITS_4_AND_6 = 0x50

    def test_nobody_recruited(self):
        self.assertEqual((), _game_state(recruitment=self._NO_BITS_SET).recruited_characters)

    def test_felix_and_sheba(self):
        self.assertEqual(
            (Character.FELIX, Character.SHEBA),
            _game_state(recruitment=self._BITS_4_AND_6).recruited_characters,
        )


class TestIsPartyWiped(unittest.TestCase):
    def test_nobody_recruited(self):
        self.assertFalse(_game_state(recruitment=_NOBODY).is_party_wiped)

    def test_nobody_recruited_all_zero(self):
        self.assertFalse(_game_state(recruitment=_NOBODY, dead=_EVERYONE).is_party_wiped)

    def test_wiped_unrecruited_alive(self):
        self.assertTrue(_game_state(recruitment=_DEFAULT_PARTY, dead=[Character.FELIX, Character.SHEBA]).is_party_wiped)

    def test_wiped_unrecruited_also_zero(self):
        self.assertTrue(_game_state(recruitment=_DEFAULT_PARTY, dead=_EVERYONE).is_party_wiped)

    def test_all_alive(self):
        self.assertFalse(_game_state(recruitment=_DEFAULT_PARTY).is_party_wiped)

    def test_benched_survivor(self):
        self.assertFalse(
            _game_state(
                recruitment=_recruited(Character.FELIX, Character.SHEBA, Character.PIERS),
                dead=[Character.FELIX, Character.SHEBA],
            ).is_party_wiped
        )

    def test_one_recruited_alive(self):
        self.assertFalse(_game_state(recruitment=_recruited(Character.FELIX)).is_party_wiped)

    def test_one_recruited_dead(self):
        self.assertTrue(_game_state(recruitment=_recruited(Character.FELIX), dead=[Character.FELIX]).is_party_wiped)


class TestIsInBattle(unittest.TestCase):
    CONTEXT_BYTES = (
        (0x00, False),  # world map, outdoor field
        (0x10, False),  # shop, dialogue, field death
        (0x50, False),  # interior field, main menu open
        (0x18, True),  # in battle
    )

    def test_only_battle_bit_valid(self):
        for context_byte, expected in self.CONTEXT_BYTES:
            with self.subTest(context_byte=hex(context_byte)):
                state = _game_state(recruitment=_DEFAULT_PARTY, in_battle=context_byte)
                self.assertEqual(expected, state.is_in_battle)


class TestIsDeathObserved(unittest.TestCase):
    @staticmethod
    def _observe(dead: Sequence[Character], **kwargs):
        return _game_state(recruitment=_DEFAULT_PARTY, dead=dead, **kwargs).is_death_observed

    def test_battle_wipe_is_death(self):
        self.assertTrue(self._observe([Character.FELIX, Character.SHEBA], in_battle=IN_BATTLE_BIT))

    def test_battle_with_survivor_is_not_death(self):
        self.assertFalse(self._observe([Character.FELIX], in_battle=IN_BATTLE_BIT))

    def test_field_wipe_is_death(self):
        self.assertTrue(
            self._observe(
                [Character.FELIX, Character.SHEBA],
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=0,
            )
        )

    def test_single_down_is_not_death(self):
        self.assertFalse(
            self._observe(
                [Character.FELIX],
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=1,
            )
        )

    def test_fully_downed_party_with_survivors_is_not_death(self):
        # should *theoretically* never happen unless we write some bogus (I think)
        self.assertFalse(
            self._observe(
                [Character.FELIX, Character.SHEBA],
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=1,
            )
        )

    def test_field_death_request_with_living_party_is_not_death(self):
        self.assertFalse(
            self._observe(
                [],
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=0,
            )
        )

    def test_all_zero_party_with_no_request_is_not_death(self):
        # All chars at zero HP and no field death request should not equate to death.
        # Happens when loading a save for example.
        self.assertFalse(self._observe([Character.FELIX, Character.SHEBA]))

    def test_another_system_event_is_not_death(self):
        map_and_menu_event = 0xFC83  # just some other valid value the request slot can have
        self.assertFalse(
            self._observe([Character.FELIX, Character.SHEBA], field_death_request=map_and_menu_event, survivor_count=0)
        )

    def test_nobody_recruited_is_not_death(self):
        # RECRUITMENT_ADDR reads 0x10 at the title screen while the character blocks are at their default.
        self.assertFalse(
            _game_state(
                recruitment=_NOBODY,
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=0,
                dead=_EVERYONE,
            ).is_death_observed
        )


class TestGameStateReads(unittest.TestCase):
    def setUp(self):
        self.width_by_address = dict(GAME_STATE_READS)

    def test_every_address_is_read_once(self):
        self.assertEqual(len(GAME_STATE_READS), len(self.width_by_address))

    def test_every_character_hp_is_u16(self):
        for character in Character:
            with self.subTest(character=character.name):
                self.assertEqual(2, self.width_by_address[get_current_hp_address(character)])

    def test_reads_and_writes_width(self):
        writes = [
            *_build_multi_zero_hp_writes(_EVERYONE),
            *_build_field_death_request_writes(_EVERYONE),
        ]
        overlapping = [write for write in writes if write.address in self.width_by_address]
        for write in overlapping:
            with self.subTest(address=hex(write.address)):
                self.assertEqual(self.width_by_address[write.address], len(write.data))


class TestGameStateFromReadResult(unittest.TestCase):
    BATTLE_BIT_CLEAR_BYTE = 0x10

    def test_field_death_with_real_data_is_death(self):
        state = GameState.from_read_result(
            [
                bytes([_DEFAULT_PARTY]),
                bytes([self.BATTLE_BIT_CLEAR_BYTE]),
                _ARMED_REQUEST_BYTES,
                _ZERO_BYTES,
                *_hp_reads(Character.FELIX, Character.SHEBA),
            ]
        )
        self.assertEqual(
            GameState(
                recruitment=_DEFAULT_PARTY,
                in_battle=self.BATTLE_BIT_CLEAR_BYTE,
                field_death_request=FIELD_DEATH_REQUEST_VALUE,
                survivor_count=0,
                hp=_hp_values(Character.FELIX, Character.SHEBA),
            ),
            state,
        )
        self.assertTrue(state.is_death_observed)


class TestPartyWipeWrites(unittest.TestCase):
    def test_every_hp_zero_is_accompanied_by_its_ratio(self):
        writes = _build_multi_zero_hp_writes((Character.FELIX, Character.SHEBA))
        self.assertEqual(
            {
                get_current_hp_address(Character.FELIX),
                get_current_hp_ratio_address(Character.FELIX),
                get_current_hp_address(Character.SHEBA),
                get_current_hp_ratio_address(Character.SHEBA),
            },
            {write.address for write in writes},
        )
        self.assertEqual([_ZERO_BYTES] * 4, [write.data for write in writes])


class TestFieldDeathRequestWrites(unittest.TestCase):
    _RECRUITED = (Character.FELIX, Character.JENNA, Character.SHEBA)
    _EXPECTED_COUNT = _little_endian_u16(len(_RECRUITED))
    _EXPECTED_SLOTS = tuple(_little_endian_u16(character) for character in _RECRUITED)

    def setUp(self):
        self.writes = _build_field_death_request_writes(self._RECRUITED)
        self.by_address = {write.address: write.data for write in self.writes}

    def test_death_request_last_write(self):
        self.assertEqual(MemoryWrite(FIELD_DEATH_REQUEST_ADDR, _ARMED_REQUEST_BYTES), self.writes[-1])

    def test_the_narration_list_covers_every_recruited_character(self):
        # TODO: might be a feature? see TODO in DeathLink.py
        self.assertEqual(self._EXPECTED_COUNT, self.by_address[FIELD_DEATH_NARRATION_COUNT_ADDR])
        for slot, expected in enumerate(self._EXPECTED_SLOTS):
            self.assertEqual(expected, self.by_address[FIELD_DEATH_NARRATION_LIST_ADDR + 2 * slot])
        self.assertNotIn(FIELD_DEATH_NARRATION_LIST_ADDR + 2 * len(self._EXPECTED_SLOTS), self.by_address)

    def test_survivor_count_is_zero_and_game_continues(self):
        # TODO: still gotta confirm this
        self.assertEqual(_ZERO_BYTES, self.by_address[FIELD_DEATH_SURVIVOR_COUNT_ADDR])
