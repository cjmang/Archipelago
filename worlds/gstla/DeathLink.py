from __future__ import annotations  # TODO: pretty sure we dont need this for >= 3.11?

from collections.abc import Sequence
from enum import Enum, auto
from typing import NamedTuple

MAX_CHARACTER_COUNT: int = 8
RECRUITMENT_ADDR = 0x40  # also BizClient.FLAG_START
CHARACTER_BLOCK_SIZE = 0x14C
CHARACTER_BLOCK_START = 0x520

IN_BATTLE_ADDR = 0x60  # TODO: duplicated in BizClient.py
IN_BATTLE_BIT = 0x08

# Addresses to trigger the field death. Similar to what happens on poison death.
# This triggers the "<character>'s strength is exhausted..." textboxes for each character
# plus the "Felix's party has been annihilated".
# TODO: Can we somehow skip the individual narrations? Having to spam through 8 text boxes is a bit annoying
FIELD_DEATH_REQUEST_ADDR = 0x3016A
FIELD_DEATH_NARRATION_COUNT_ADDR = 0x3016C
FIELD_DEATH_SURVIVOR_COUNT_ADDR = 0x3016E
FIELD_DEATH_NARRATION_LIST_ADDR = 0x30170
FIELD_DEATH_REQUEST_VALUE = 0xFFFF

HP_RATIO_OFFSET = 0x14
MAX_HP_OFFSET = 0x34
CURRENT_HP_OFFSET = 0x38

# TODO: Obsolete for deathlink, but maybe useful to store somewhere?
MAX_PP_RATIO_OFFSET = 0x16
MAX_PP_OFFSET = 0x36
CURRENT_PP_OFFSET = 0x3A
CHARACTER_STATUS_BYTE_OFFSET = 0x131  # 0 = none, 1 = poison, 2 = venom, ...


def get_character_block_address(index: int) -> int:
    return CHARACTER_BLOCK_START + index * CHARACTER_BLOCK_SIZE


def get_current_hp_address(index: int) -> int:
    return get_character_block_address(index) + CURRENT_HP_OFFSET


def get_current_hp_ratio_address(index: int) -> int:
    """
    The "HP ratio" here is very likely just the way the game draws the HP bar.
    For some reason, the devs decided that bar should also double as a check
    against a (intentional or accidental) HP manipulation.

    Current HP and ratio have always have to be in sync.
    Setting the current HP to 0 without changing the ratio might result in
    a mismatch the game then corrects by setting that character to max HP/PP.
    Writing to these addresses should therefore always be done together
    in one single operation. Having them even just a few frames apart while someone spams
    their way through the battle actions can introduce a sudden full-heal.
    """
    return get_character_block_address(index) + HP_RATIO_OFFSET


GAME_STATE_READS: tuple[tuple[int, int], ...] = (
    (RECRUITMENT_ADDR, 1),
    (IN_BATTLE_ADDR, 1),
    (FIELD_DEATH_REQUEST_ADDR, 2),
    (FIELD_DEATH_SURVIVOR_COUNT_ADDR, 2),
    *tuple((get_current_hp_address(index), 2) for index in range(MAX_CHARACTER_COUNT)),
)


class GameState(NamedTuple):
    recruitment: int
    in_battle: int
    field_death_request: int
    survivor_count: int
    hp: tuple[int, ...]

    @classmethod
    def from_read_result(cls, results: Sequence[bytes]) -> GameState:
        values = {}
        for (address, _width), result in zip(GAME_STATE_READS, results, strict=True):
            values[address] = int.from_bytes(result, "little")

        return cls(
            recruitment=values[RECRUITMENT_ADDR],
            in_battle=values[IN_BATTLE_ADDR],
            field_death_request=values[FIELD_DEATH_REQUEST_ADDR],
            survivor_count=values[FIELD_DEATH_SURVIVOR_COUNT_ADDR],
            hp=tuple(values[get_current_hp_address(index)] for index in range(MAX_CHARACTER_COUNT)),
        )

    @property
    def recruited_characters(self) -> tuple[int, ...]:
        """
        The indexes of all currently recruited characters.

        The character blocks of unrecruited chars are not empty,
        they just have their default stats set and look like a
        fully healed character.
        So every HP read has to first go through this function.
        """
        return tuple(i for i in range(MAX_CHARACTER_COUNT) if self.recruitment & (1 << i))

    @property
    def is_in_battle(self) -> bool:
        return bool(self.in_battle & IN_BATTLE_BIT)

    @property
    def is_field_death_armed(self) -> bool:
        return self.field_death_request == FIELD_DEATH_REQUEST_VALUE

    @property
    def is_party_wiped(self) -> bool:
        """
        True when every recruited character is at 0 HP, False when nobody is recruited.
        Important: This does not automatically mean the full party died (yet).

        Note:
        This also returns True when the game has just booted up.
        In that case the recruitment byte is already 0x10 while character HP is 0.
        So just relying on this to detect a wipe is not enough and
        a caller also has to check that a save is actually loaded.
        """
        recruited = self.recruited_characters
        return bool(recruited) and all(self.hp[i] == 0 for i in recruited)

    @property
    def is_field_death_in_progress(self) -> bool:
        """
        True when a field death is running and the game counts nobody as still standing.

        We trigger a field death by writing FIELD_DEATH_REQUEST_VALUE into field_death_request,
        but just doing that alone does not automatically mean that we triggered a death.
        The game also writes that same FIELD_DEATH_REQUEST_VALUE every time a character goes down
        on the field, like when they're poisoned and take their last step.
        But as long as the survivor count is not 0, it just shows the
        "character is exhausted" text and the game continues normally.

        Also note:
        Since we'll also be writing both of these values ourselves to wipe the party,
        just checking these values only tells us that a field death is happening,
        but not if it's caused by us or just dying "naturally" via poison or something.
        """
        return self.is_field_death_armed and self.survivor_count == 0

    @property
    def is_death_observed(self) -> bool:
        """
        True when every recruited character reads 0 HP *and* the game has acted on it,
        so this is an actual death and not just a party that happens to be at zero.

        This is an important distinction because "everyone at 0 HP" can occur in other places
        like booting up the game or when we write 0 HP ourselves to trigger the deathlink.

        So how does the proper confirmation actually look like?
        - In battle:
          Relatively straight-forward. Since the game checks on every action/input,
          it'll just play the defeat dialogue after we've set the HP to 0.

        - On the field/overworld:
          There's no loop like the one in battle that checks for HP, so without any trigger
          we could just stay on the field forever. Only when we'd get into a battle,
          it would then check for HP and play the defeat dialogue.
          However, it does have a loop that is checking for registered events like a poison tick.
          TODO: Add reference to poison handler
          Also see `is_field_death_in_progress`.
        """
        return self.is_party_wiped and (self.is_in_battle or self.is_field_death_in_progress)


