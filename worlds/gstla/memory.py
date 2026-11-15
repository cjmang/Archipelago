from enum import StrEnum
from typing import NamedTuple


class MemoryDomain(StrEnum):
    EWRAM = 'EWRAM'
    ROM = 'ROM'


class MemoryRange(NamedTuple):
    """We can pass an instance of this directly into the BizHawk client"""

    address: int
    length: int
    domain: MemoryDomain


class FlagArray:
    """
    The full block of game flags as read by the bizhawk client every tick.

    The client reads the whole array once (via FLAG_ARRAY_RANGE), we put it in self._data,
    and we just check the flags we actually need directly, instead of iterating over everything and categorizing them
    like we did before in `_check_common_flags`.
    At least that's the plan.

    # TODO: Reword? Don't think anyone cares after this actually gets merged x)

    Example:
        "Doom Dragon Defeated" = is_set(0x778)
        "Collected Sol Blade Chest" = is_set(0xE02)
        (djinns are handled a bit different. See game_data/djinns.py)
    """

    def __init__(self, data: bytes) -> None:
        self._data = data

    def is_set(self, flag: int) -> bool:
        byte_idx, bit_idx = divmod(flag, 8)
        return bool(self._data[byte_idx] & (1 << bit_idx))


FLAG_START = 0x40
FLAG_ARRAY_RANGE = MemoryRange(FLAG_START, 0x200, MemoryDomain.EWRAM)  # not sure if 0x200 is enough?

RECRUITMENT_ADDR = FLAG_START
CHARACTER_BLOCK_SIZE = 0x14C
CHARACTER_BLOCK_START = 0x520

IN_BATTLE_ADDR = 0x60
IN_BATTLE_BIT = 0x08

SYSTEM_EVENT_ADDR = 0x3016A
SYSTEM_EVENT_FIELD_DEATH = 0xFFFF

FORCE_ENCOUNTER_ADDR = 0x30164
PREVENT_FLEEING_ADDR = 0x48B

FIELD_DEATH_NARRATION_COUNT_ADDR = 0x3016C
FIELD_DEATH_SURVIVOR_COUNT_ADDR = 0x3016E
FIELD_DEATH_NARRATION_LIST_ADDR = 0x30170

HP_RATIO_OFFSET = 0x14
MAX_HP_OFFSET = 0x34
CURRENT_HP_OFFSET = 0x38

MAX_PP_RATIO_OFFSET = 0x16
MAX_PP_OFFSET = 0x36
CURRENT_PP_OFFSET = 0x3A
CHARACTER_STATUS_BYTE_OFFSET = 0x131  # 0 = none, 1 = poison, 2 = venom, ...

ROM_GAME_NAME = MemoryRange(0xA0, 0x12, MemoryDomain.ROM)
ROM_SLOT_NAME = MemoryRange(0xFFF000, 64, MemoryDomain.ROM)
AUTO_RUN_PATCH_ADDRESSES = (0x26361, 0x270A5, 0x279DD, 0x1007900)
