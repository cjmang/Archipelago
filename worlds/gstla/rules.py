# TODO:
#  - Evaluate if CachedRuleBuilderWorld would do anything useful for us
#  - Import ItemName as Item, EntranceName as Entrance after adding all of them
#  - Why not use the rando logic from game_code? (asked Platano) - DECISION: Do python-only, but test against rando
#  - We might actually be able to do to_dict() with the data-json format (Reqs) and compare that to the rando data

from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, HasAny, HasGroup, Or
from worlds.gstla.names import RegionName
from .gstla_types import EntranceData, ItemType
from .items import ItemName
from .options import AnemosAccess, ShortcutMagmaRock, ShortcutMarsLighthouse, StartWithShip

if TYPE_CHECKING:
    from .world import GSTLAWorld


ENTRANCES: list[EntranceData] = [
    EntranceData(RegionName.Menu, RegionName.Idejima, None),
    EntranceData(RegionName.Idejima, RegionName.PartyMembers, None),
    EntranceData(RegionName.Idejima, RegionName.Daila, None),
    EntranceData(RegionName.Daila, RegionName.DehkanPlateau, None),
    EntranceData(RegionName.DehkanPlateau, RegionName.Madra, None),
    EntranceData(RegionName.Madra, RegionName.IndraCavern, None),
    EntranceData(RegionName.Madra, RegionName.OseniaCliffs, None),
    EntranceData(RegionName.OseniaCliffs, RegionName.Mikasalla, None),
    EntranceData(RegionName.YampiDesertBack, RegionName.Alhafra, None),
    EntranceData(RegionName.Alhafra, RegionName.YampiDesertBack, None),
    EntranceData(RegionName.Mikasalla, RegionName.Garoh, None),
    EntranceData(RegionName.Mikasalla, RegionName.OseniaCavern, None),
    EntranceData(RegionName.Mikasalla, RegionName.YampiDesertFront, None),
    EntranceData(RegionName.Naribwe, RegionName.KibomboMountains, None),
    EntranceData(RegionName.EasternSea, RegionName.Alhafra, None),
    EntranceData(RegionName.EasternSea, RegionName.Kibombo, None),
    EntranceData(RegionName.EasternSea, RegionName.Naribwe, None),
    EntranceData(RegionName.EasternSea, RegionName.WestIndraIslet, None),
    EntranceData(RegionName.EasternSea, RegionName.NorthOseniaIslet, None),
    EntranceData(RegionName.EasternSea, RegionName.SouthEastAngaraIslet, None),
    EntranceData(RegionName.EasternSea, RegionName.SeaOfTimeIslet, None),
    EntranceData(RegionName.EasternSea, RegionName.SeaOfTime, None),
    EntranceData(RegionName.EasternSea, RegionName.TreasureIsland, None),
    EntranceData(RegionName.EasternSea, RegionName.Champa, None),
    EntranceData(RegionName.EasternSea, RegionName.Izumo, None),
    EntranceData(RegionName.EasternSea, RegionName.GaiaRock, None),
    EntranceData(RegionName.EasternSea, RegionName.Yallam, None),
    EntranceData(RegionName.EasternSea, RegionName.EastTundariaIslet, None),
    EntranceData(RegionName.EasternSea, RegionName.TundariaTower, None),
    EntranceData(RegionName.EasternSea, RegionName.ApojiiIslands, None),
    EntranceData(RegionName.Yallam, RegionName.TaopoSwamp, None),
    EntranceData(RegionName.Lemuria, RegionName.Lemurian_Ship_Revisit, None),
    EntranceData(RegionName.WesternSea, RegionName.SouthWestAttekaIslet, None),
    EntranceData(RegionName.WesternSea, RegionName.HesperiaSettlement, None),
    EntranceData(RegionName.WesternSea, RegionName.ShamanVillageCave, None),
    EntranceData(RegionName.WesternSea, RegionName.AttekaInlet, None),
    EntranceData(RegionName.WesternSea, RegionName.GondowanSettlement, None),
    EntranceData(RegionName.WesternSea, RegionName.Loho, None),
    EntranceData(RegionName.WesternSea, RegionName.AngaraCavern, None),
    EntranceData(RegionName.WesternSea, RegionName.KaltIsland, None),
    EntranceData(RegionName.AttekaInlet, RegionName.Contigo, None),
    EntranceData(RegionName.AttekaInlet, RegionName.Lemurian_Ship_Revisit, None),
    EntranceData(RegionName.Prox, RegionName.MarsLighthouse, None),
    EntranceData(RegionName.Daila, RegionName.ShrineOfTheSeaGod, Has(ItemName.Lash_Pebble)),
    EntranceData(RegionName.Daila, RegionName.KandoreanTemple, Has(ItemName.Whirlwind)),
    EntranceData(RegionName.Madra, RegionName.MadraCatacombs, Has(ItemName.Reveal)),
    EntranceData(RegionName.YampiDesertFront, RegionName.YampiDesertBack, Has(ItemName.Scoop_Gem)),
    EntranceData(
        RegionName.YampiDesertBack,
        RegionName.YampiDesertCave,
        HasAll(ItemName.Sand, ItemName.Teleport_Lapis, ItemName.Burst_Brooch),
    ),
    EntranceData(
        RegionName.Alhafra,
        RegionName.AlhafraCave,
        Or(
            Has(ItemName.Briggs_escaped),
            HasAll(ItemName.Briggs_defeated, ItemName.Tremor_Bit),
        ),
    ),
    EntranceData(RegionName.Garoh, RegionName.AirsRock, Has(ItemName.Whirlwind)),
    EntranceData(RegionName.Garoh, RegionName.YampiDesertBack, Has(ItemName.Sand)),
    EntranceData(RegionName.Madra, RegionName.GondowanCliffs, HasAny(ItemName.Frost_Jewel, ItemName.Scoop_Gem)),
    EntranceData(RegionName.GondowanCliffs, RegionName.Naribwe, Has(ItemName.Briggs_defeated)),
    EntranceData(
        RegionName.KibomboMountains,
        RegionName.Kibombo,
        Or(
            Has(ItemName.Frost_Jewel),
            HasAll(ItemName.Lash_Pebble, ItemName.Whirlwind),
        ),
    ),
    EntranceData(RegionName.Kibombo, RegionName.GabombaStatue, HasAll(ItemName.Lash_Pebble, ItemName.Scoop_Gem)),
    EntranceData(
        RegionName.GabombaStatue,
        RegionName.GabombaCatacombs,
        HasAll(ItemName.Gabomba_Statue_Completed, ItemName.Cyclone_Chip),
    ),
    EntranceData(RegionName.Madra, RegionName.EasternSea, Has(ItemName.Ship)),
    EntranceData(RegionName.SeaOfTimeIslet, RegionName.IsletCave, HasAll(ItemName.Mind_Read, ItemName.Lil_Turtle)),
    EntranceData(RegionName.SeaOfTime, RegionName.Lemuria, HasAny(ItemName.Poseidon_defeated, ItemName.Grindstone)),
    EntranceData(RegionName.TreasureIsland, RegionName.TreasureIsland_Grindstone, Has(ItemName.Grindstone)),
    EntranceData(
        RegionName.TreasureIsland_Grindstone, RegionName.TreasureIsland_PostReunion, Has(ItemName.Lifting_Gem)
    ),
    EntranceData(RegionName.EasternSea, RegionName.AnkohlRuins, Has(ItemName.Whirlwind)),
    EntranceData(RegionName.AnkohlRuins, RegionName.AnkohlRuins_Sand, Has(ItemName.Sand)),
    EntranceData(RegionName.EasternSea, RegionName.AquaRock, Has(ItemName.Douse_Drop)),
    EntranceData(RegionName.TundariaTower, RegionName.TundariaTower_Parched, Has(ItemName.Parch)),
    EntranceData(
        RegionName.EasternSea,
        RegionName.WesternSea,
        Or(
            Has(ItemName.Grindstone),
            HasAll(ItemName.Wings_of_Anemos, ItemName.Hover_Jade),
        ),
    ),
    EntranceData(RegionName.WesternSea, RegionName.AttekaCavern, HasAll(ItemName.Wings_of_Anemos, ItemName.Hover_Jade)),
    EntranceData(RegionName.WesternSea, RegionName.MagmaRock, Has(ItemName.Lifting_Gem)),
    EntranceData(
        RegionName.Contigo,
        RegionName.AnemosSanctum,
        And(
            Has(ItemName.Teleport_Lapis),
            HasGroup(
                ItemType.Djinn.name,
                72,
                options=[OptionFilter(AnemosAccess, AnemosAccess.option_vanilla)],
                filtered_resolution=True,
            ),
            HasGroup(
                ItemType.Djinn.name,
                28,
                options=[OptionFilter(AnemosAccess, AnemosAccess.option_randomized)],
                filtered_resolution=True,
            ),
        ),
    ),
    EntranceData(RegionName.Contigo, RegionName.JupiterLighthouse, Has(ItemName.Cyclone_Chip)),
    EntranceData(RegionName.Contigo, RegionName.Reunion, Has(ItemName.Jupiter_Beacon_Lit)),
    EntranceData(
        RegionName.ShamanVillageCave,
        RegionName.ShamanVillage,
        Or(
            Has(ItemName.Whirlwind),
            HasAll(ItemName.Lifting_Gem, ItemName.Frost_Jewel),
        ),
    ),
    EntranceData(RegionName.WesternSea, RegionName.Prox, Has(ItemName.Ship_Cannon)),
    EntranceData(
        RegionName.MagmaRock,
        RegionName.MagmaRockInterior,
        HasAll(
            ItemName.Burst_Brooch,
            ItemName.Growth,
            ItemName.Lash_Pebble,
            options=[OptionFilter(ShortcutMagmaRock, ShortcutMagmaRock.option_false)],
            filtered_resolution=True,
        ),
    ),
    EntranceData(
        RegionName.MarsLighthouse,
        RegionName.MarsLighthouse_Activated,
        Or(
            Has(ItemName.Mars_Star, options=[OptionFilter(ShortcutMarsLighthouse, ShortcutMarsLighthouse.option_true)]),
            Has(
                ItemName.Mars_Lighthouse_Heated,
                options=[OptionFilter(ShortcutMarsLighthouse, ShortcutMarsLighthouse.option_false)],
            ),
        ),
    ),
    EntranceData(
        RegionName.Madra,
        RegionName.Lemurian_Ship,
        HasAll(
            ItemName.Black_Crystal,
            ItemName.Gabomba_Statue_Completed,
            ItemName.Piers,
            options=[OptionFilter(StartWithShip, StartWithShip.option_vanilla)],
            filtered_resolution=True,
        ),
    ),
]


def create_entrances(world: GSTLAWorld) -> None:
    for row in ENTRANCES:
        world.create_entrance(world.get_region(row.source), world.get_region(row.target), row.rule)
