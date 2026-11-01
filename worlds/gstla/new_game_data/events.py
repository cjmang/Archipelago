from dataclasses import dataclass
from typing import Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemType
from worlds.gstla.names import ItemName, LocationName
from .base import BaseItem

EVENTS: tuple[tuple[int, int, str, str], ...] = (
    # TODO: dedup the other events lists
    # (ap_id, flag_index, location_name, name)
    (5001, 0x778, LocationName.Mars_Lighthouse_Doom_Dragon, ItemName.Doom_Dragon_Defeated),
    (5002, 0x8AB, LocationName.Alhafra_Briggs, ItemName.Briggs_defeated),
    (5003, 0x97F, LocationName.Alhafra_Prison_Briggs, ItemName.Briggs_escaped),
    (5004, 0x8FF, LocationName.Gabomba_Statue_Ritual, ItemName.Gabomba_Statue_Completed),
    (5005, 0x9EE, LocationName.Gaia_Rock_Serpent, ItemName.Serpent_defeated),
    (5006, 0x665, LocationName.Sea_of_Time_Poseidon, ItemName.Poseidon_defeated),
    (5007, 0x93F, LocationName.Lemurian_Ship_Aqua_Hydra, ItemName.Aqua_Hydra_defeated),
    (5008, 0x94D, LocationName.Shaman_Village_Moapa, ItemName.Moapa_defeated),
    (5009, 0xA21, LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst, ItemName.Jupiter_Beacon_Lit),
    (5010, 0xA4B, LocationName.Mars_Lighthouse_Flame_Dragons, ItemName.Flame_Dragons_defeated),
    (5011, 0x8DE, LocationName.Lemurian_Ship_Engine_Room, ItemName.Ship),
    (5012, 0x8DF, LocationName.Contigo_Wings_of_Anemos, ItemName.Wings_of_Anemos),
    (5013, 0x64A, LocationName.Kandorean_Temple_Chestbeaters, ItemName.Chestbeaters_defeated),
    (5014, 0x64D, LocationName.Yampi_Desert_King_Scorpion, ItemName.King_Scorpion_defeated),
    (5015, 0x662, LocationName.Champa_Avimander, ItemName.Avimander_defeated),
    (5016, 0x6A4, LocationName.Treasure_Isle_Star_Magician, ItemName.Star_Magician_defeated),
    (5017, 0x6DD, LocationName.Islet_Cave_Sentinel, ItemName.Sentinel_defeated),
    (5018, 0x6D1, LocationName.Yampi_Desert_Cave_Valukar, ItemName.Valukar_defeated),
    (5019, 0x6DA, LocationName.Anemos_Inner_Sanctum_Dullahan, ItemName.Dullahan_defeated),
    # Flag for 5020 is really the Jupiter Lighthouse flag. Base rando with PC shuffle
    # seems to do something weird with the reunion flag.
    (5020, 0xA21, LocationName.Contigo_Reunion, ItemName.Reunion),
    (5021, 0x1, LocationName.Victory_Event, ItemName.Victory),
    (5022, 0xA5F, LocationName.Loho_Ship_Cannon, ItemName.Ship_Cannon),
    (5023, 0xA30, LocationName.Mars_Lighthouse_Heated, ItemName.Mars_Lighthouse_Heated),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Event(BaseItem):
    ITEM_TYPE = ItemType.Event
    CLASSIFICATION = ItemClassification.progression
    CATEGORY = ItemCategory.events

    ap_id: int  # same as the corresponding location
    flag_index: int
    location_name: str
    name: str

    @property
    def in_pool(self) -> bool:
        # events have their own fixed location, see `items.create_events()`
        return False

    @classmethod
    def load(cls) -> tuple[Self, ...]:
        return tuple(
            cls(ap_id=ap_id, flag_index=flag_index, location_name=location_name, name=name)
            for ap_id, flag_index, location_name, name in EVENTS
        )
