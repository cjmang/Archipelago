from __future__ import annotations  # TODO: pretty sure we dont need this for >= 3.11?

from collections.abc import Sequence
from enum import Enum, IntEnum, auto
from typing import NamedTuple

RECRUITMENT_ADDR = 0x40  # also BizClient.FLAG_START
CHARACTER_BLOCK_SIZE = 0x14C
CHARACTER_BLOCK_START = 0x520

IN_BATTLE_ADDR = 0x60  # TODO: duplicated in BizClient.py
IN_BATTLE_BIT = 0x08

# Writing the SYSTEM_EVENT_FIELD_DEATH to SYSTEM_EVENT_ADDR triggers a death similar
# to a death by poison. This results in the "<character>'s strength is exhausted..."
# textboxes for each character plus the "Felix's party has been annihilated".
SYSTEM_EVENT_ADDR = 0x3016A
SYSTEM_EVENT_FIELD_DEATH = 0xFFFF

FIELD_DEATH_NARRATION_COUNT_ADDR = 0x3016C
FIELD_DEATH_SURVIVOR_COUNT_ADDR = 0x3016E
FIELD_DEATH_NARRATION_LIST_ADDR = 0x30170

HP_RATIO_OFFSET = 0x14
MAX_HP_OFFSET = 0x34
CURRENT_HP_OFFSET = 0x38

# TODO: Obsolete for deathlink, but maybe useful to store somewhere?
MAX_PP_RATIO_OFFSET = 0x16
MAX_PP_OFFSET = 0x36
CURRENT_PP_OFFSET = 0x3A
CHARACTER_STATUS_BYTE_OFFSET = 0x131  # 0 = none, 1 = poison, 2 = venom, ...


class CharacterIndex(IntEnum):
    ISAAC = 0
    GARET = 1
    IVAN = 2
    MIA = 3
    FELIX = 4
    JENNA = 5
    SHEBA = 6
    PIERS = 7


def get_character_block_address(character: CharacterIndex) -> int:
    return CHARACTER_BLOCK_START + character * CHARACTER_BLOCK_SIZE


def get_current_hp_address(character: CharacterIndex) -> int:
    return get_character_block_address(character) + CURRENT_HP_OFFSET


def get_current_hp_ratio_address(character: CharacterIndex) -> int:
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
    return get_character_block_address(character) + HP_RATIO_OFFSET


GAME_STATE_READS: tuple[tuple[int, int], ...] = (
    (RECRUITMENT_ADDR, 1),
    (IN_BATTLE_ADDR, 1),
    (SYSTEM_EVENT_ADDR, 2),
    (FIELD_DEATH_SURVIVOR_COUNT_ADDR, 2),
    *tuple((get_current_hp_address(character), 2) for character in CharacterIndex),
)


class GameState(NamedTuple):
    recruitment: int
    in_battle: int
    system_event: int
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
            system_event=values[SYSTEM_EVENT_ADDR],
            survivor_count=values[FIELD_DEATH_SURVIVOR_COUNT_ADDR],
            hp=tuple(values[get_current_hp_address(character)] for character in CharacterIndex),
        )

    @property
    def recruited_characters(self) -> tuple[CharacterIndex, ...]:
        """
        The indexes of all currently recruited characters.

        The character blocks of unrecruited chars are not empty,
        they just have their default stats set and look like a
        fully healed character.
        So every HP read has to first go through this function.
        """
        return tuple(character for character in CharacterIndex if self.recruitment & (1 << character))

    @property
    def is_in_battle(self) -> bool:
        return bool(self.in_battle & IN_BATTLE_BIT)

    @property
    def is_field_death_armed(self) -> bool:
        return self.field_death_request == FIELD_DEATH_REQUEST_VALUE
        return self.system_event == SYSTEM_EVENT_FIELD_DEATH

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
        return bool(recruited) and all(self.hp[character] == 0 for character in recruited)

    @property
    def is_field_death_in_progress(self) -> bool:
        """
        True when a field death is running and the game counts nobody as still standing.

        We trigger a field death by writing SYSTEM_EVENT_FIELD_DEATH into the system event slot,
        but just doing that alone does not automatically mean that we triggered a death.
        The game also writes that same SYSTEM_EVENT_FIELD_DEATH every time a character goes down
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

        How the proper confirmation looks like:
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


class MemoryWrite(NamedTuple):
    address: int
    data: bytes

    @classmethod
    def u16(cls, address: int, value: int) -> MemoryWrite:
        return cls(address, value.to_bytes(2, "little"))


def _build_zero_hp_writes(character: CharacterIndex) -> tuple[MemoryWrite, MemoryWrite]:
    """
    HP writes should *always* only happen together. If the game sees a mismatch
    between HP and HP ratio, it will try to correct it when it runs some kind of
    loop on that character. Just setting HP *can* theoretically work but
    it's extremely inconsistant.

    Example:
        1. Start a fight, click through enemy textboxes
        2. Write HP to 0 without the ratio
        3. Select the first option  # TODO: what's the name again? I don't mean the "Attack" but the one next to flee
        4. In *most* cases, this is when the loop runs and a characters HP (+PP) get corrected to max.
    """

    return (
        MemoryWrite.u16(get_current_hp_address(character), 0),
        MemoryWrite.u16(get_current_hp_ratio_address(character), 0),
    )


def _build_multi_zero_hp_writes(characters: Sequence[CharacterIndex]) -> list[MemoryWrite]:
    return [write for character in characters for write in _build_zero_hp_writes(character)]


def _build_field_death_request_writes(recruited: Sequence[CharacterIndex]) -> list[MemoryWrite]:
    """
    These writes just use the default ingame way of handling something like poison deaths

    (FIELD_DEATH_NARRATION_LIST_ADDR + slot * 2) here is just the individual slot
    of their own "XYZ is exhausted" textbox

    TODO:
     Can we somehow skip the individual narrations?
     Having to spam through 8 text boxes is a bit annoying
    """
    narration_list = [
        MemoryWrite.u16(FIELD_DEATH_NARRATION_LIST_ADDR + slot * 2, character)
        for slot, character in enumerate(recruited)
    ]
    return [
        MemoryWrite.u16(FIELD_DEATH_NARRATION_COUNT_ADDR, len(recruited)),
        *narration_list,
        MemoryWrite.u16(FIELD_DEATH_SURVIVOR_COUNT_ADDR, 0),
        MemoryWrite.u16(SYSTEM_EVENT_ADDR, SYSTEM_EVENT_FIELD_DEATH),
    ]
