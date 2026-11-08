from dataclasses import dataclass
from typing import Self

from worlds.gstla.gstla_types import CharacterIndex, LocationRestriction, LocationType, TreasureType
from worlds.gstla.new_game_data.base import BaseLocation, read_json, read_json_dir
from worlds.gstla.new_game_data.characters import CHARACTER_ITEM_ID_OFFSET
from worlds.gstla.new_game_data.location_names import loc_names_by_id
from worlds.gstla.new_game_data.psynergy import LEARNED_PSYNERGY_MAPPING, PSYNERGY_ITEM_ID_OFFSET

RESTRICTIONS_MAP = {
    'no-empty': LocationRestriction.NoEmpty,
    'no-mimic': LocationRestriction.NoMimic,
    'no-summon': LocationRestriction.NoSummon,
    'no-money': LocationRestriction.NoMoney,
}

# Since some items/psynergies are normally obtained once you recruit a character,
# we'll have to map some of those items to non-vanilla flags.
FLAG_OVERWRITES = {
    0xFA00CA: CharacterIndex.FELIX,  # Shaman's Rod
    0xFA00CC: CharacterIndex.SHEBA,  # Mind Read
    0xFA00CE: CharacterIndex.SHEBA,  # Whirlwind
    0xFA00D0: CharacterIndex.FELIX,  # Growth
    0xFA00D2: CharacterIndex.MIA,  # Carry Stone
    0xFA00D4: CharacterIndex.IVAN,  # Lifting Gem
    0xFA00D6: CharacterIndex.GARET,  # Orb of Force
    0xFA00D8: CharacterIndex.ISAAC,  # Catch Beads
    0xFA00DA: CharacterIndex.PIERS,  # Douse Drop
    0xFA00DC: CharacterIndex.PIERS,  # Frost Jewel
}

FREELY_RANDOMIZEABLE_TREASURE_TYPES = frozenset({TreasureType.CHEST, TreasureType.PICKUP})
RANDO_SLOT_ADDRESS_START = 0xFA0000  # anything above this address are rando-only locations
TRADE_ITEM_IDS = frozenset(
    {
        452,  # Pretty Stone
        453,  # Red Cloth
        454,  # Milk
        455,  # Li'l Turtle
    }
)


def _load_restrictions() -> dict[int, LocationRestriction]:
    restrictions: dict[int, LocationRestriction] = {}
    for area_data in read_json_dir('data/location_logic').values():
        for loc in area_data['Treasure']:
            rando_flag = int(loc['Addr'], 16)
            restrictions[rando_flag] = LocationRestriction(
                sum(RESTRICTIONS_MAP[res] for res in loc.get('Restriction', []))
            )
    return restrictions


def _implicit_restrictions(ap_id: int, treasure_type: TreasureType) -> LocationRestriction:
    restrictions = LocationRestriction.NONE
    if treasure_type not in FREELY_RANDOMIZEABLE_TREASURE_TYPES:
        restrictions |= LocationRestriction.NoEmpty | LocationRestriction.NoMimic
    if ap_id > RANDO_SLOT_ADDRESS_START:
        restrictions |= LocationRestriction.NoMoney
    if ap_id in FLAG_OVERWRITES:
        # TODO: I think the previous "loc['id'] < 0x10 or (loc['id'] | 0xF00) == 0x100" line before never fully worked?
        #       Wouldn't (loc['id'] | 0xF00) always equal loc['id']?
        restrictions |= LocationRestriction.NoEmpty | LocationRestriction.NoMimic | LocationRestriction.NoMoney
    return restrictions


@dataclass(frozen=True, slots=True, kw_only=True)
class ChestLocation(BaseLocation):
    """

    Note:
        There are some locations that have two entries in item_locations.json.
        For example "0xf57", which is an "Oil Drop" in "Lemurian Ship".
        These are just two different versions of the same chest. We can never open both.
        We're only using the *first* entry. The ap_id is therefore that first entries' "addr".
        If the rando ever decides to swap those values, it'll change the datapackage and break the PopTracker.
        TODO: Maybe we should have some kind of constant values for these?
    """

    ap_id: int
    flag: int  # EWRAM
    is_hidden: bool
    name: str
    rando_flag: int
    restrictions: LocationRestriction
    treasure_type: TreasureType
    vanilla_item_id: int
    # there's more data in the data file, but we currently don't use those

    @property
    def location_type(self) -> LocationType:
        if self.vanilla_item_id - PSYNERGY_ITEM_ID_OFFSET in LEARNED_PSYNERGY_MAPPING:
            return LocationType.Psynergy
        if self.is_hidden:
            return LocationType.Hidden
        if self.vanilla_item_id in TRADE_ITEM_IDS:
            return LocationType.Trade
        if CHARACTER_ITEM_ID_OFFSET <= self.vanilla_item_id < CHARACTER_ITEM_ID_OFFSET + len(CharacterIndex):
            return LocationType.Character
        return LocationType.Item

    @classmethod
    def _build_row(cls, entry: dict, explicit_restrictions: LocationRestriction) -> Self:
        ap_id = entry['addr']
        rando_flag = entry['id']  # also matches the key of the item_locations.json entry
        treasure_type = TreasureType(entry['eventType'])
        return cls(
            ap_id=ap_id,
            flag=FLAG_OVERWRITES.get(ap_id, rando_flag),
            is_hidden=entry['isHidden'],
            name=loc_names_by_id[ap_id],
            rando_flag=rando_flag,
            restrictions=explicit_restrictions | _implicit_restrictions(ap_id, treasure_type),
            treasure_type=treasure_type,
            vanilla_item_id=entry['vanillaContents'],
        )

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        restrictions = _load_restrictions()
        rows = []
        for loc in read_json('data/item_locations.json').values():
            loc = loc[0]  # see docstring
            row = cls._build_row(loc, restrictions[loc['id']])
            rows.append(row)

        return tuple(rows)
