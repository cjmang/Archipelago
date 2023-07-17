import typing
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from worlds.gstla.Locations import GSTLALocation, location_name_to_id
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName
from .Names.ItemName import ItemName
def create_region(multiworld: MultiWorld, player: int, name: str, locations: typing.List[str]):
    region = Region(name, player, multiworld)
    for location in locations:
        loc = GSTLALocation(player, location, location_name_to_id.get(location, None), region)
        region.locations.append(loc)
    multiworld.regions.append(region)


def create_connect(world: MultiWorld, player: int, source: str, target: str, rule: callable = lambda state: True, one_way=False, name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        create_connect(world, player, target, source, rule, True)


def create_regions(multiworld: MultiWorld, player: int):
    create_region(multiworld, player, RegionName.Menu, [])

    create_region(multiworld, player, RegionName.Idejima, [])

    create_region(multiworld, player, RegionName.EasternSea, [])

    create_region(multiworld, player, RegionName.Daila,
    [
        LocationName.Daila_Herb,
        LocationName.Daila_3_coins,
        LocationName.Daila_12_coins,
        LocationName.Daila_Psy_Crystal,
        LocationName.Daila_Sleep_Bomb,
        LocationName.Daila_Sea_Gods_Tear,
        LocationName.Daila_Smoke_Bomb
    ])

    create_region(multiworld, player, RegionName.KandoreamTemple,
    [
        LocationName.Kandorean_Temple_Mimic,
        LocationName.Kandorean_Temple_Lash_Pebble,
        LocationName.Kandorean_Temple_Mysterious_Card
    ])

    create_region(multiworld, player, RegionName.DehkanPlateau,
    [
        LocationName.Dehkan_Plateau_Elixir,
        LocationName.Dehkan_Plateau_Pound_Cube,
        LocationName.Dehkan_Plateau_Themis_Axe,
        LocationName.Dehkan_Plateau_Full_Metal_Vest,
        LocationName.Dehkan_Plateau_Mint,
        LocationName.Dehkan_Plateau_Nut
    ])

    create_region(multiworld, player, RegionName.Madra,
    [
                      LocationName.Madra_Elixir,
                      LocationName.Madra_Antidote,
                      LocationName.Madra_Cyclone_Chip,
                      LocationName.Madra_15_coins,
                      LocationName.Madra_Nurses_Cap
    ])

    create_region(multiworld, player, RegionName.MadraCatacombs,
    [
        LocationName.Madra_Catacombs_Moloch,
        LocationName.Madra_Catacombs_Ruin_Key,
        LocationName.Madra_Catacombs_Tremor_Bit,
        LocationName.Madra_Catacombs_Apple,
        LocationName.Madra_Catacombs_Lucky_Medal,
        LocationName.Madra_Catacombs_Mist_Potion,
        LocationName.DoomDragonDefeated
    ])

    create_connect(multiworld, player, RegionName.Menu, RegionName.Idejima)
    create_connect(multiworld, player, RegionName.Idejima, RegionName.EasternSea)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Daila)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.KandoreamTemple)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.DehkanPlateau)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Madra)
    create_connect(multiworld, player, RegionName.Madra, RegionName.MadraCatacombs, lambda state: state.has(ItemName.Sea_Gods_Tear, player))