from typing import TYPE_CHECKING

from worlds.generic.Rules import add_item_rule
from .game_data.coins import COIN_ID_OFFSET
from .game_data.loader import load_game_data
from .gstla_types import LocationRestriction, LocationType
from .items import ItemType
from .names import ItemName, LocationName

if TYPE_CHECKING:
    from .items import GSTLAItem
    from .world import GSTLAWorld


class _RestrictionRule:
    summon_names = {summon.name for summon in load_game_data().summons.values()}

    def __init__(self, player: int, loc_restrictions: LocationRestriction):
        self.player = player
        self.loc_restrictions = loc_restrictions

    def __call__(self, item: 'GSTLAItem') -> bool:
        # Really the type should be 'GSTLAItem' -> bool, but I dunno how to get around python typing
        if item.player != self.player:
            return True
        ret = True
        if self.loc_restrictions & LocationRestriction.NoMimic > 0:
            ret &= item.item_data.type != ItemType.Mimic
        if self.loc_restrictions & LocationRestriction.NoEmpty > 0:
            ret &= item.name != ItemName.Empty
        if self.loc_restrictions & LocationRestriction.NoSummon > 0:
            ret &= (
                item.item_data.type != ItemType.Character
                and item.item_data.type != ItemType.Mimic
                and item.name not in _RestrictionRule.summon_names
            )
        if self.loc_restrictions & LocationRestriction.NoMoney > 0:
            ret &= item.item_data.id < COIN_ID_OFFSET
        return ret


def set_item_rules(world: 'GSTLAWorld'):
    player = world.player
    game_data = load_game_data()
    characters: set[str] = {item.name for item in game_data.characters.values()}
    djinn: set[str] = {item.name for item in game_data.djinn.values()}

    for loc in game_data.locations_by_type[LocationType.Djinn]:
        add_item_rule(world.get_location(loc.name), lambda item: item.player == player and item.name in djinn)

    if world.options.shuffle_characters < 2:
        for loc in game_data.locations_by_type[LocationType.Character]:
            add_item_rule(
                world.get_location(loc.name),
                lambda item: item.player == player and item.name in characters,
            )
    else:
        add_item_rule(
            world.get_location(LocationName.Idejima_Jenna),
            lambda item: item.player == player and item.name in characters,
        )

    # Starting character inventories can't handle remote items right now
    add_item_rule(world.get_location(LocationName.Idejima_Shamans_Rod), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Idejima_Growth), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Idejima_Whirlwind), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Idejima_Mind_Read), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Kibombo_Douse_Drop), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Kibombo_Frost_Jewel), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Contigo_Catch_Beads), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Contigo_Carry_Stone), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Contigo_Lifting_Gem), lambda item: item.player == player)
    add_item_rule(world.get_location(LocationName.Contigo_Orb_of_Force), lambda item: item.player == player)

    for loc in [
        x.location_data
        for x in world.multiworld.get_locations(world.player)
        if x.location_data.type != LocationType.Event
    ]:
        if loc.restrictions > 0:
            add_item_rule(world.get_location(loc.name), _RestrictionRule(player, loc.restrictions))
