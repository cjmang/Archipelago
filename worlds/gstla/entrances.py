from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, HasAny, HasGroup, Or
from .gstla_types import EntranceData, ItemType
from .items import ItemName
from .names import RegionName
from .options import AnemosAccess, ShortcutMagmaRock, ShortcutMarsLighthouse, StartWithShip

if TYPE_CHECKING:
    from .world import GSTLAWorld


ENTRANCES: list[EntranceData] = [
    # Start
    EntranceData(RegionName.Menu, RegionName.Idejima, None),
    EntranceData(RegionName.Idejima, RegionName.PartyMembers, None),
    EntranceData(RegionName.Idejima, RegionName.Daila, None),
    EntranceData(RegionName.Idejima, RegionName.NorthIndra, None),
    # North Indra
    EntranceData(RegionName.NorthIndra, RegionName.DehkanPlateau, None),
    EntranceData(RegionName.NorthIndra, RegionName.ShrineOfTheSeaGod, Has(ItemName.Lash_Pebble)),  # no glitch handling!
    EntranceData(RegionName.NorthIndra, RegionName.KandoreanTemple, Has(ItemName.Whirlwind)),
    EntranceData(RegionName.DehkanPlateau, RegionName.SouthIndra, None),
    # South Indra
    EntranceData(RegionName.SouthIndra, RegionName.Madra, None),
    EntranceData(RegionName.Madra, RegionName.MadraCatacombs, Has(ItemName.Reveal)),
    EntranceData(RegionName.SouthIndra, RegionName.IndraCavern, None),
    EntranceData(RegionName.SouthIndra, RegionName.GondowanCliffs, HasAny(ItemName.Frost_Jewel, ItemName.Scoop_Gem)),
    EntranceData(
        RegionName.SouthIndra,
        RegionName.Lemurian_Ship,
        HasAll(
            ItemName.Black_Crystal,
            ItemName.Gabomba_Statue_Completed,
            ItemName.Piers,
            options=[OptionFilter(StartWithShip, StartWithShip.option_vanilla)],
            filtered_resolution=True,
        ),
    ),
    EntranceData(RegionName.SouthIndra, RegionName.EasternSea, Has(ItemName.Ship)),
    EntranceData(RegionName.SouthIndra, RegionName.OseniaCliffs, None),
    EntranceData(RegionName.OseniaCliffs, RegionName.SouthOsenia, None),
    # South Osenia
    EntranceData(RegionName.SouthOsenia, RegionName.Mikasalla, None),
    EntranceData(RegionName.SouthOsenia, RegionName.Garoh, None),
    EntranceData(RegionName.SouthOsenia, RegionName.OseniaCavern, None),
    EntranceData(RegionName.SouthOsenia, RegionName.YampiDesertFront, None),
    EntranceData(RegionName.SouthOsenia, RegionName.AirsRock, Has(ItemName.Whirlwind)),
    EntranceData(RegionName.SouthOsenia, RegionName.YampiDesertBack, Has(ItemName.Sand)),
    EntranceData(RegionName.YampiDesertBack, RegionName.NorthOsenia, None),
    # North Osenia (Alhafra)
    EntranceData(RegionName.NorthOsenia, RegionName.Alhafra, None),
    EntranceData(RegionName.NorthOsenia, RegionName.YampiDesertBack, None),  # hm? two way, why explicitly?
    EntranceData(RegionName.EasternSea, RegionName.NorthOsenia, None),
    # TODO
    EntranceData(RegionName.Naribwe, RegionName.KibomboMountains, None),
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
]


def create_entrances(world: GSTLAWorld) -> None:
    for row in ENTRANCES:
        world.create_entrance(world.get_region(row.source), world.get_region(row.target), row.rule)
