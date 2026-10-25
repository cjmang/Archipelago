# TODO:
#  - Evaluate if CachedRuleBuilderWorld would do anything useful for us
#  - Import ItemName as Item, EntranceName as Entrance after adding all of them
#  - Why not use the rando logic from game_code? (asked Platano)

from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, HasAny, HasGroup, Or, Rule
from .game_data import ItemType
from .items import ItemName
from .options import AnemosAccess, ShortcutMagmaRock, ShortcutMarsLighthouse, StartWithShip
from .regions import EntranceName

if TYPE_CHECKING:
    from .world import GSTLAWorld

# TODO:
#  Rather use operators like "|" and "&" or HasAll/HasAny/Or/And?
#  HasAll/HasAny/Or/And make formatting look bit nicer, imo
#  Also: Replace EntranceNames with tuples?: `(Daila, ShrineOfTheSeaGod): Has(XYZ)`

ENTRANCE_RULES: dict[str, Rule] = {
    EntranceName.DailaToShrineOfTheSeaGod: Has(ItemName.Lash_Pebble),
    EntranceName.DailaToKandoreanTemple: Has(ItemName.Whirlwind),
    EntranceName.MadraToMadraCatacombs: Has(ItemName.Reveal),
    EntranceName.YampiDesertFrontToYampiDesertBack: Has(ItemName.Scoop_Gem),
    EntranceName.YampiDesertBackToYampiDesertCave: HasAll(
        ItemName.Sand, ItemName.Teleport_Lapis, ItemName.Burst_Brooch
    ),
    EntranceName.AlhafraToAlhafraCave: Or(
        Has(ItemName.Briggs_escaped),
        HasAll(ItemName.Briggs_defeated, ItemName.Tremor_Bit),
    ),
    EntranceName.GarohToAirsRock: Has(ItemName.Whirlwind),
    EntranceName.GarohToYampiDesertBack: Has(ItemName.Sand),
    EntranceName.MadraToGondowanCliffs: HasAny(ItemName.Frost_Jewel, ItemName.Scoop_Gem),
    EntranceName.GondowanCliffsToNaribwe: Has(ItemName.Briggs_defeated),
    EntranceName.KibomboMountainsToKibombo: Or(
        Has(ItemName.Frost_Jewel),
        HasAll(ItemName.Lash_Pebble, ItemName.Whirlwind),
    ),
    EntranceName.KibomboToGabombaStatue: HasAll(ItemName.Lash_Pebble, ItemName.Scoop_Gem),
    EntranceName.GabombaStatueToGabombaCatacombs: HasAll(ItemName.Gabomba_Statue_Completed, ItemName.Cyclone_Chip),
    EntranceName.MadraToEasternSea: Has(ItemName.Ship),
    EntranceName.SeaOfTimeIsletToIsletCave: HasAll(ItemName.Mind_Read, ItemName.Lil_Turtle),
    EntranceName.SeaOfTimeToLemuria: HasAny(ItemName.Poseidon_defeated, ItemName.Grindstone),
    EntranceName.TreasureIslandToTreasureIsland_Grindstone: Has(ItemName.Grindstone),
    EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion: Has(ItemName.Lifting_Gem),
    EntranceName.EasternSeaToAnkohlRuins: Has(ItemName.Whirlwind),
    EntranceName.AnkohlRuinsToAnkohlRuins_Sand: Has(ItemName.Sand),
    EntranceName.EasternSeaToAquaRock: Has(ItemName.Douse_Drop),
    EntranceName.TundariaTowerToTundariaTower_Parched: Has(ItemName.Parch),
    EntranceName.EasternSeaToWesternSea: Or(
        Has(ItemName.Grindstone),
        HasAll(ItemName.Wings_of_Anemos, ItemName.Hover_Jade),
    ),
    EntranceName.WesternSeaToAttekaCavern: HasAll(ItemName.Wings_of_Anemos, ItemName.Hover_Jade),
    EntranceName.WesternSeaToMagmaRock: Has(ItemName.Lifting_Gem),
    EntranceName.ContigoToAnemosInnerSanctum: And(
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
    EntranceName.ContigoToJupiterLighthouse: Has(ItemName.Cyclone_Chip),
    EntranceName.ContigoToReunion: Has(ItemName.Jupiter_Beacon_Lit),
    EntranceName.ShamanVillageCaveToShamanVillage: Or(
        Has(ItemName.Whirlwind),
        HasAll(ItemName.Lifting_Gem, ItemName.Frost_Jewel),
    ),
    EntranceName.WesternSeaToProx: Has(ItemName.Ship_Cannon),
    EntranceName.MagmaRockToMagmaRockInterior: HasAll(
        ItemName.Burst_Brooch,
        ItemName.Growth,
        ItemName.Lash_Pebble,
        options=[OptionFilter(ShortcutMagmaRock, ShortcutMagmaRock.option_false)],
        filtered_resolution=True,
    ),
    EntranceName.MarsLighthouseToMarsLighthouse_Activated: Or(
        Has(ItemName.Mars_Star, options=[OptionFilter(ShortcutMarsLighthouse, ShortcutMarsLighthouse.option_true)]),
        Has(
            ItemName.Mars_Lighthouse_Heated,
            options=[OptionFilter(ShortcutMarsLighthouse, ShortcutMarsLighthouse.option_false)],
        ),
    ),
    EntranceName.MadraToLemurianShip: HasAll(
        ItemName.Black_Crystal,
        ItemName.Gabomba_Statue_Completed,
        ItemName.Piers,
        options=[OptionFilter(StartWithShip, StartWithShip.option_vanilla)],
        filtered_resolution=True,
    ),
}


def set_entrance_rules(world: GSTLAWorld) -> None:
    for entrance, rule in ENTRANCE_RULES.items():
        world.set_rule(world.get_entrance(entrance), rule)
