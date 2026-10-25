# TODO:
#  - Evaluate if CachedRuleBuilderWorld would do anything useful for us
#  - Import ItemName as Item, EntranceName as Entrance after adding all of them

from rule_builder.rules import Has, HasAll, HasAny, Or, Rule
from .items import ItemName
from .regions import EntranceName

# TODO:
#  Rather use operators like "|" and "&" or HasAll/HasAny/Or/And?
#  HasAll/HasAny/Or/And make formatting look bit nicer, imo
#  Also: Replace EntranceNames with tuples?: `(Daila, ShrineOfTheSeaGod): Has(XYZ)`

ENTRANCE_RULES: dict[str, Rule] = {
    # L23-99 first
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
    # L100-200
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
    # TODO: Here are some conditional ones
    EntranceName.ContigoToAnemosInnerSanctum: Has(ItemName.Teleport_Lapis),
    EntranceName.ContigoToJupiterLighthouse: Has(ItemName.Cyclone_Chip),
    EntranceName.ContigoToReunion: Has(ItemName.Jupiter_Beacon_Lit),
    EntranceName.ShamanVillageCaveToShamanVillage: Or(
        Has(ItemName.Whirlwind),
        HasAll(ItemName.Lifting_Gem, ItemName.Frost_Jewel),
    ),
    EntranceName.WesternSeaToProx: Has(ItemName.Ship_Cannon),
    # TODO: More conditional ones
}
