from typing import TYPE_CHECKING, TypeVar

from BaseClasses import Item, ItemClassification
from .gen.item_data import (
    FillerType,
    ItemData,
    TrapType,
)
from .gen.location_data import LocationType, location_type_to_data
from .gen.location_names import loc_names_by_id
from .gstla_types import ItemCategory, ItemData as NewItemData, ItemType
from .names import ItemName, LocationName
from .new_game_data.loader import load_game_data
from .options import AddDummyItems, AddGs1Items

if TYPE_CHECKING:
    from .world import GSTLAWorld


class GSTLAItem(Item):
    """The GSTLA version of an AP item"""

    game: str = 'Golden Sun The Lost Age'
    item_data: NewItemData

    def __init__(
        self,
        item: NewItemData,
        player: int,
        event: bool = False,
        classification: ItemClassification | None = None,
    ):
        classification = item.classification if classification is None else classification
        if event:
            super().__init__(item.name, classification, None, player)
        else:
            super().__init__(item.name, classification, item.id, player)
        self.item_data = item


AP_USEFUL_PLACEHOLDER_ITEM = NewItemData(
    id=0xA00,
    name='AP Useful Placeholder',
    category=ItemCategory.non_vanilla,
    classification=ItemClassification.useful,
    type=ItemType.Consumable,
)
AP_PROG_PLACEHOLDER_ITEM = NewItemData(
    id=0xA0A,
    name='AP Progression Placeholder',
    category=ItemCategory.non_vanilla,
    classification=ItemClassification.progression,
    type=ItemType.Consumable,
)
AP_PLACEHOLDER_ITEM = NewItemData(
    id=0xA0B,
    name='AP Placeholder',
    category=ItemCategory.non_vanilla,
    classification=ItemClassification.filler,
    type=ItemType.Consumable,
)


OPTION_BASED_ITEMS: dict[type[AddGs1Items | AddDummyItems], tuple[str, ...]] = {
    AddGs1Items: (ItemName.Elven_Shirt, ItemName.Clerics_Ring),
    AddDummyItems: (
        ItemName.Casual_Shirt,
        ItemName.Golden_Boots,
        ItemName.Aroma_Ring,
        ItemName.Golden_Shirt,
        ItemName.Ninja_Sandals,
        ItemName.Golden_Ring,
        ItemName.Herbed_Shirt,
        ItemName.Knights_Greave,
        ItemName.Rainbow_Ring,
        ItemName.Divine_Camisole,
        ItemName.Silver_Greave,
        ItemName.Soul_Ring,
    ),
}


def create_item(
    name: str, player: int, event: bool = False, classification: ItemClassification | None = None
) -> 'GSTLAItem':
    """Creates a GSTLAItem from data populated in this file

    Parameters:
        name (str): The AP name of the item
        player (int): The AP player to create the item for.
        event (bool): Is this item an event?
        classification (ItemClassification): The classification of the item (progression, filler, etc)
    Returns:
        The newly created item
    """
    game_data = load_game_data()
    item = game_data.item_by_name[name]
    return GSTLAItem(item, player, event, classification)


def create_item_direct(
    item: ItemData,
    player: int,
    event: bool = False,
    classification: ItemClassification | None = None,
):
    return GSTLAItem(item, player, event, classification)


# TODO: Is the line below the reason for my missing boots? :')
filler_gear_types = {ItemType.Shield, ItemType.Armor, ItemType.Weapon, ItemType.Helm}


def create_filler(world: 'GSTLAWorld', item: ItemData):
    equipment = load_game_data().equipment
    if (
        world.options.artifacts_are_filler
        and item.id in equipment
        and equipment[item.id].is_rare
        and item.type in filler_gear_types
        or world.options.forge_materials_are_filler
        and item.category == ItemCategory.forge_materials
    ):
        return create_item_direct(item, world.player, False, ItemClassification.filler)
    return create_item_direct(item, world.player)


def create_events(world: 'GSTLAWorld'):
    """Creates all the event items and populates their vanilla locations with them.
    If the option to begin with the starter ship was selected this will be granted to the player

    Parameters:
        world: The world to generate events for
    """
    game_data = load_game_data()
    for event in game_data.events.values():
        event_item = create_item(event.name, world.player, True)

        if event.location_name == LocationName.Lemurian_Ship_Engine_Room and world.options.lemurian_ship == 2:
            # world.multiworld.push_precollected(event_item)
            continue

        if (
            event.location_name == LocationName.Contigo_Wings_of_Anemos
            and world.options.start_with_wings_of_anemos == 1
        ):
            # world.multiworld.push_precollected(event_item)
            continue

        if world.options.omit_locations.value == 2 and event.location_name in [
            LocationName.Islet_Cave_Sentinel,
            LocationName.Treasure_Isle_Star_Magician,
            LocationName.Yampi_Desert_Cave_Valukar,
        ]:
            continue

        if event.location_name == LocationName.Anemos_Inner_Sanctum_Dullahan and world.options.omit_locations.value > 0:
            continue

        event_location = world.get_location(event.location_name)
        event_location.place_locked_item(event_item)


def create_items(world: 'GSTLAWorld', player: int):  # noqa: PLR0912, PLR0915
    """Creates all the items for GSTLA that need to be shuffled into the multiworld, and
    adds them to the multiworld's item pool.
    """
    game_data = load_game_data()
    pool: list[GSTLAItem] = []

    # djinn
    sorted_djinns = sorted(game_data.items_by_category[ItemCategory.djinn], key=lambda djinn: djinn.id)
    sorted_djinn_locs = sorted(location_type_to_data[LocationType.Djinn], key=lambda loc: loc.id)

    if world.options.shuffle_djinn == 1:
        for i in range(0, 4):
            slice_start = 0 + i * 18
            sub_djinns = sorted_djinns[slice_start : slice_start + 18]
            sub_locs = sorted_djinn_locs[slice_start : slice_start + 18]

            world.random.shuffle(sub_djinns)
            world.random.shuffle(sub_locs)

            sorted_djinns[slice_start : slice_start + 18] = sub_djinns
            sorted_djinn_locs[slice_start : slice_start + 18] = sub_locs
    elif world.options.shuffle_djinn > 1:
        world.random.shuffle(sorted_djinns)
        world.random.shuffle(sorted_djinn_locs)

    for item in sorted_djinns:
        ap_item = create_item_direct(item, player, True)
        location = sorted_djinn_locs.pop(0)
        ap_loc = world.get_location(loc_names_by_id[location.ap_id])
        ap_loc.address = None
        ap_loc.place_locked_item(ap_item)

    # char shuffle
    char_locs = {
        loc_names_by_id[char_lock.ap_id]: char_lock for char_lock in location_type_to_data[LocationType.Character]
    }
    char_items = {char.name: char for char in game_data.items_by_category[ItemCategory.characters]}

    # if not vanilla character shuffle we can do special things
    if world.options.shuffle_characters > 0:
        char_opt = world.options.second_starting_character
        char_name = [
            ItemName.Jenna,
            ItemName.Sheba,
            ItemName.Piers,
            ItemName.Isaac,
            ItemName.Garet,
            ItemName.Ivan,
            ItemName.Mia,
        ][char_opt]
        character = char_items.pop(char_name)
        ap_item = create_item_direct(character, player)
        ap_location = world.get_location(LocationName.Idejima_Jenna)
        ap_location.place_locked_item(ap_item)
        char_locs.pop(LocationName.Idejima_Jenna)

        # if we are not starting with the ship and it is a vanilla shuffled character shuffle we have to enforce
        # piers in initial 3 chars to avoid soft lock. when vanilla piers is locked in kibombo on his vanilla
        # location and when in the item pool the shuffler will take care of things for us
        if ItemName.Piers in char_items and world.options.lemurian_ship < 2 and world.options.shuffle_characters == 1:
            character = char_items.pop(ItemName.Piers)
            starting_char_locs = [LocationName.Idejima_Sheba, LocationName.Kibombo_Piers]
            starting_char_loc = world.random.choice(starting_char_locs)
            location = char_locs.pop(starting_char_loc)
            ap_item = create_item_direct(character, player)
            ap_location = world.get_location(starting_char_loc)
            ap_location.place_locked_item(ap_item)

    sorted_chars = sorted(char_items.values(), key=lambda char: char.id)
    sorted_char_locs = sorted(char_locs.values(), key=lambda loc: loc.id)

    if world.options.shuffle_characters > 0:
        world.random.shuffle(sorted_chars)
        world.random.shuffle(sorted_char_locs)

    for character in sorted_chars:
        ap_item = create_item_direct(character, player)

        # Vanilla (Shuffled)
        if world.options.shuffle_characters < 2:
            location = sorted_char_locs.pop(0)
            ap_loc = world.get_location(loc_names_by_id[location.ap_id])
            ap_loc.place_locked_item(ap_item)

        else:
            # Anywhere
            pool.append(ap_item)

    unfilled = len(world.multiworld.get_unfilled_locations(player))

    for item in game_data.items_by_category[ItemCategory.psynergy_items]:
        # Ignore cloak ball and halt gem, they are not required for anything
        if item.name == ItemName.Cloak_Ball or item.name == ItemName.Halt_Gem:
            # TODO: already handled in item.in_pool
            continue

        ap_item = create_item_direct(item, player)
        pool.append(ap_item)
    for item in game_data.items_by_category[ItemCategory.learned_psynergy]:
        ap_item = create_item_direct(item, player)
        pool.append(ap_item)
    summon_classification = None
    if 'Summon Hunt' in world.goal_conditions:
        summon_classification = ItemClassification.progression_deprioritized_skip_balancing
    for item in game_data.items_by_category[ItemCategory.summons]:
        # Ignore summons that are obtained by gaining X djinn
        if item.id < 3856:
            # TODO: already handled in item.in_pool
            continue
        ap_item = create_item_direct(item, player, classification=summon_classification)
        pool.append(ap_item)

    for item in game_data.items_by_category[ItemCategory.other_progression]:
        if world.options.lemurian_ship != 0 and item.name == ItemName.Black_Crystal:
            # The black crystal is unnecessary when the ship door is not closed
            continue
        ap_item = create_item_direct(item, player)
        pool.append(ap_item)

    if world.options.item_shuffle == 3:
        # Adding one progressive lucky medal
        pool.append(create_item_direct(game_data.item_by_id[229], player, False, ItemClassification.progression))

    for item in game_data.items_by_category[ItemCategory.class_change_items]:
        ap_item = create_item_direct(item, player)
        pool.append(ap_item)

    for item in game_data.items_by_category[ItemCategory.useful_remainder]:
        ap_item = create_filler(world, item)
        pool.append(ap_item)

    for option_type, names in OPTION_BASED_ITEMS.items():
        if getattr(world.options, option_type.internal_name):
            pool.extend([create_item(name, player) for name in names])

    ap_item = create_item(ItemName.Laughing_Fungus, player)
    pool.append(ap_item)

    # We guarentee a number of filler items when item shuffle all is on, it adds a hefty amount of hidden locations
    # that do not support having a mimic and fail generation. On repeated generations it results into 65-70 mimics
    # failing to be placed, otherwise it works fine.
    # TODO: Can't we place a mimic trap for ourselves there instead then?
    if world.options.trap_chance > 0 and world.options.mimic_trap_weight > 0:
        for _ in range(40):
            item = get_filler_item(world, False)
            ap_item = create_item_direct(item, player)
            pool.append(ap_item)

    if world.options.item_shuffle > 2 and world.options.trap_chance > 0 and world.options.mimic_trap_weight > 0:
        for _ in range(60):
            item = get_filler_item(world, False)
            ap_item = create_item_direct(item, player)
            pool.append(ap_item)

    for _ in range(unfilled - len(pool)):
        item = get_filler_item(world)
        ap_item = create_filler(world, item)
        pool.append(ap_item)

    world.multiworld.itempool.extend(pool)


def get_filler_item(world: 'GSTLAWorld', includetraps: bool = True) -> ItemData:  # noqa: PLR0912
    if includetraps and world.options.trap_chance > 0 and world.random.randint(1, 100) <= world.options.trap_chance:
        trap_pool_weights = create_trap_pool_weights(world)
        trap_type = world.random.choices(list(trap_pool_weights.keys()), list(trap_pool_weights.values()))[0]

        if trap_type == TrapType.Mimic:
            item = world.random.choice(mimics)

    else:
        filler_pool_weights = create_filler_pool_weights(world)
        filler_type = world.random.choices(list(filler_pool_weights.keys()), list(filler_pool_weights.values()))[0]

        if filler_type == FillerType.ForgeMaterials:
            item = world.random.choice(forge_materials)

        elif filler_type == FillerType.RustyMaterials:
            item = world.random.choice(rusty_items)

        elif filler_type == FillerType.StatBoosts:
            item = world.random.choice(stat_boosters)

        elif filler_type == FillerType.UsefulConsumables:
            item = world.random.choice(useful_consumables)

        elif filler_type == FillerType.ForgedEquipment:
            item = world.random.choice(forge_only)

        elif filler_type == FillerType.LuckyEquipment:
            item = world.random.choice(lucky_only)

        elif filler_type == FillerType.ShopEquipment:
            item = world.random.choice(shop_only)

        elif filler_type == FillerType.Coins:
            item = world.random.choice(vanilla_coins)

        elif filler_type == FillerType.CommonConsumables:
            item = world.random.choice(remainder)

    # fall back if for some reason we dont have an item
    if not item:
        item = world.random.choice(remainder)

    return item


FILLER_WEIGHT_OPTION_NAMES: dict[FillerType, str] = {
    FillerType.Coins: 'coins_filler_weight',
    FillerType.CommonConsumables: 'common_consumable_filler_weight',
    FillerType.ForgeMaterials: 'forge_material_filler_weight',
    FillerType.ForgedEquipment: 'forged_equipment_filler_weight',
    FillerType.LuckyEquipment: 'lucky_equipment_filler_weight',
    FillerType.RustyMaterials: 'rusty_material_filler_weight',
    FillerType.ShopEquipment: 'shop_equipment_filler_weight',
    FillerType.StatBoosts: 'stat_boost_filler_weight',
    FillerType.UsefulConsumables: 'uncommon_consumable_filler_weight',
}

TRAP_WEIGHT_OPTION_NAMES: dict[TrapType, str] = {
    TrapType.Mimic: 'mimic_trap_weight',
}


PoolType = TypeVar('PoolType', FillerType, TrapType)


def _get_pool_weights(world: 'GSTLAWorld', option_names: dict[PoolType, str]) -> dict[PoolType, int]:
    weights = {pool_type: getattr(world.options, name).value for pool_type, name in option_names.items()}
    return {pool_type: weight for pool_type, weight in weights.items() if weight > 0}


def create_filler_pool_weights(world: 'GSTLAWorld') -> dict[FillerType, int]:
    """Creates a dictionary mapping FillerTypes to weight to be used for rolling filler items in the itempool"""
    return _get_pool_weights(world, FILLER_WEIGHT_OPTION_NAMES)


def create_trap_pool_weights(world: 'GSTLAWorld') -> dict[TrapType, int]:
    """Creates a dictionary mapping TrapTypes to weight to be used for rolling trap items in the itempool"""
    return _get_pool_weights(world, TRAP_WEIGHT_OPTION_NAMES)
