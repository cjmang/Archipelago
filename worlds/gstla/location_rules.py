from __future__ import annotations

import math
from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasAll, HasGroup
from worlds.generic.Rules import add_rule
from .game_data.loader import load_game_data
from .gstla_types import LocationType, TreasureType
from .items import ItemType
from .names import ItemName, LocationName

if TYPE_CHECKING:
    from rule_builder.rules import Rule
    from .world import GSTLAWorld


# Regex gaming:
# Difficulty: ez
# add_rule\(\s*world\.get_location\(LocationName\.(\w+)\),\s*lambda state: state\.has\(ItemName\.(\w+), player\),?\s*\)
# replace with
# LocationName.$1: Has(ItemName.$2),

GOAL_EVENTS: dict[str, str] = {
    # TODO: dedup with EVENTS in events.py?
    # TODO: proper Goal enum?
    'Doom Dragon': ItemName.Doom_Dragon_Defeated,  # lowercase "defeated"?
    'Chestbeaters': ItemName.Chestbeaters_defeated,
    'King Scorpion': ItemName.King_Scorpion_defeated,
    'Briggs': ItemName.Briggs_defeated,
    'Aqua Hydra': ItemName.Aqua_Hydra_defeated,
    'Poseidon': ItemName.Poseidon_defeated,
    'Serpent': ItemName.Serpent_defeated,
    'Avimander': ItemName.Avimander_defeated,
    'Moapa': ItemName.Moapa_defeated,
    'Reunion': ItemName.Reunion,
    'Flame Dragons': ItemName.Flame_Dragons_defeated,
    'Star Magician': ItemName.Star_Magician_defeated,
    'Sentinel': ItemName.Sentinel_defeated,
    'Valukar': ItemName.Valukar_defeated,
    'Dullahan': ItemName.Dullahan_defeated,
}


def set_goal_rules(world: GSTLAWorld) -> None:
    goal_conditions = world.goal_conditions
    required_events: set[str] = set()

    if not goal_conditions:
        required_events.add(ItemName.Doom_Dragon_Defeated)

    required_events.update([GOAL_EVENTS[goal] for goal in goal_conditions if goal in GOAL_EVENTS])
    djinn_needed = world.options.djinn_hunt_count.value if 'Djinn Hunt' in goal_conditions else 0
    summons_needed = world.options.summon_hunt_count.value if 'Summon Hunt' in goal_conditions else 0

    goal_rule = And(
        HasAll(*required_events),
        HasGroup(ItemType.Djinn.name, djinn_needed),
        HasGroup(ItemType.Summon.name, summons_needed),
    )

    world.set_rule(world.get_location(LocationName.Victory_Event), goal_rule)
    world.set_completion_rule(Has(ItemName.Victory))


DJINNS_BY_PARTY_SIZE: dict[int, tuple[str, ...]] = {
    # In vanilla, these are brought by a newly recruited character,
    # but since chars can be shuffled we have to grant them by party size
    2: (
        LocationName.Spring,
        LocationName.Shade,
    ),
    3: (
        LocationName.Flint,
        LocationName.Forge,
        LocationName.Gust,
    ),
    4: (
        LocationName.Granite,
        LocationName.Fizz,
        LocationName.Fever,
        LocationName.Breeze,
    ),
    5: (
        LocationName.Sleet,
        LocationName.Quartz,
        LocationName.Mist,
        LocationName.Corona,
        LocationName.Zephyr,
    ),
    6: (
        LocationName.Vine,
        LocationName.Spritz,
        LocationName.Scorch,
        LocationName.Smog,
        LocationName.Sap,
        LocationName.Hail,
    ),
    7: (
        LocationName.Ember,
        LocationName.Kite,
        LocationName.Ground,
        LocationName.Tonic,
        LocationName.Flash,
        LocationName.Squall,
    ),
}

LOCATION_RULES: dict[str, Rule] = {
    # Chars
    LocationName.Idejima_Mind_Read: Has(ItemName.Sheba),
    LocationName.Idejima_Whirlwind: Has(ItemName.Sheba),
    LocationName.Kibombo_Douse_Drop: Has(ItemName.Piers),
    LocationName.Kibombo_Frost_Jewel: Has(ItemName.Piers),
    LocationName.Contigo_Carry_Stone: Has(ItemName.Mia),
    LocationName.Contigo_Lifting_Gem: Has(ItemName.Ivan),
    LocationName.Contigo_Orb_of_Force: Has(ItemName.Garet),
    LocationName.Contigo_Catch_Beads: Has(ItemName.Isaac),
    # Djinns
    **{
        djinn: HasGroup(ItemType.Character.name, party_size)
        for party_size, djinns in DJINNS_BY_PARTY_SIZE.items()
        for djinn in djinns
    },
    # The Rest
}


def set_location_rules(world: GSTLAWorld) -> None:
    # The rest
    for location in world.get_locations():
        if location.name not in LOCATION_RULES:
            continue

        rule = LOCATION_RULES[location.name]
        world.set_rule(location, rule)


def set_access_rules(world: GSTLAWorld):  # noqa: PLR0912, PLR0915
    game_data = load_game_data()
    player = world.player

    # Daila
    add_rule(
        world.get_location(LocationName.Daila_Sea_Gods_Tear), lambda state: state.has(ItemName.Frost_Jewel, player)
    )

    # Kandorean Temple
    add_rule(world.get_location(LocationName.Fog), lambda state: state.has(ItemName.Lash_Pebble, player))

    # Dehkan Platea
    add_rule(world.get_location(LocationName.Cannon), lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(world.get_location(LocationName.Dehkan_Plateau_Nut), lambda state: state.has(ItemName.Lash_Pebble, player))

    # Shrine of the Sea God
    add_rule(
        world.get_location(LocationName.Shrine_of_the_Sea_God_Rusty_Staff),
        lambda state: state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Shrine_of_the_Sea_God_Right_Prong),
        lambda state: (
            state.has(ItemName.Frost_Jewel, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Sea_Gods_Tear, player)
        ),
    )

    # Indra Cavern
    add_rule(world.get_location(LocationName.Indra_Cavern_Zagan), lambda state: state.has(ItemName.Lash_Pebble, player))

    # Madra
    add_rule(
        world.get_location(LocationName.Madra_Cyclone_Chip),
        lambda state: state.has(ItemName.Gabomba_Statue_Completed, player),
    )

    add_rule(world.get_location(LocationName.Char), lambda state: state.has(ItemName.Healing_Fungus, player))

    # Madra Catacombs
    add_rule(
        world.get_location(LocationName.Madra_Catacombs_Ruin_Key),
        lambda state: (
            state.has(ItemName.Tremor_Bit, player)
            and state.has(ItemName.Lash_Pebble, player)
            and state.has(ItemName.Frost_Jewel, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Madra_Catacombs_Mist_Potion),
        lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Madra_Catacombs_Moloch), lambda state: state.has(ItemName.Ruin_Key, player)
    )

    # Yampi Desert
    add_rule(world.get_location(LocationName.Blitz), lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Guardian_Ring),
        lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player),
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Antidote),
        lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player),
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_King_Scorpion),
        lambda state: state.has(ItemName.Pound_Cube, player),
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Scoop_Gem),
        lambda state: state.has(ItemName.King_Scorpion_defeated, player),
    )

    # Yamp Desert Backside
    add_rule(
        world.get_location(LocationName.Yampi_Desert_Lucky_Medal), lambda state: state.has(ItemName.Reveal, player)
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Trainers_Whip),
        lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Sand, player),
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Blow_Mace), lambda state: state.has(ItemName.Pound_Cube, player)
    )

    add_rule(
        world.get_location(LocationName.Yampi_Desert_Cave_Water_of_Life), lambda state: state.has(ItemName.Sand, player)
    )

    # Yampi Desert Cave
    add_rule(
        world.get_location(LocationName.Yampi_Desert_Cave_Mythril_Silver),
        lambda state: state.has(ItemName.Scoop_Gem, player),
    )

    add_rule(world.get_location(LocationName.Crystal), lambda state: state.has(ItemName.Scoop_Gem, player))

    # Alhafra
    add_rule(world.get_location(LocationName.Alhafra_Psy_Crystal), lambda state: state.has(ItemName.Reveal, player))

    add_rule(
        world.get_location(LocationName.Alhafra_Prison_Briggs),
        lambda state: (
            state.has(ItemName.Briggs_defeated, player)
            and state.has(ItemName.Lash_Pebble, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Pound_Cube, player)
        ),
    )

    # Alhafra Cave
    add_rule(
        world.get_location(LocationName.Alhafran_Cave_123_coins),
        lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player),
    )

    add_rule(
        world.get_location(LocationName.Alhafran_Cave_Ixion_Mail),
        lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player),
    )

    add_rule(
        world.get_location(LocationName.Alhafran_Cave_Lucky_Medal),
        lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player),
    )

    add_rule(
        world.get_location(LocationName.Alhafran_Cave_777_coins),
        lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Alhafran_Cave_Potion),
        lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Alhafran_Cave_Psy_Crystal),
        lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player),
    )

    # Mikasalla
    add_rule(world.get_location(LocationName.Spark), lambda state: state.has(ItemName.Scoop_Gem, player))

    # Osenia Cliffs
    add_rule(
        world.get_location(LocationName.Osenia_Cliffs_Pirates_Sword),
        lambda state: state.has(ItemName.Lash_Pebble, player),
    )

    # Osenia Cavern
    add_rule(
        world.get_location(LocationName.Osenia_Cavern_Megaera), lambda state: state.has(ItemName.Scoop_Gem, player)
    )

    # Garoh
    add_rule(world.get_location(LocationName.Garoh_Hypnos_Sword), lambda state: state.has(ItemName.Reveal, player))

    add_rule(world.get_location(LocationName.Ether), lambda state: state.has(ItemName.Reveal, player))

    # Airs Rock
    add_rule(world.get_location(LocationName.Airs_Rock_Vial), lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(world.get_location(LocationName.Airs_Rock_Psy_Crystal), lambda state: state.has(ItemName.Reveal, player))

    # Gondowan Cliffs
    add_rule(
        world.get_location(LocationName.Gondowan_Cliffs_Healing_Fungus),
        lambda state: state.has(ItemName.Frost_Jewel, player),
    )

    # Naribwe
    add_rule(
        world.get_location(LocationName.Naribwe_Thorn_Crown), lambda state: state.has(ItemName.Lash_Pebble, player)
    )

    add_rule(
        world.get_location(LocationName.Naribwe_Unicorn_Ring),
        lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Reveal, player),
    )

    # Kibombo Mountains
    add_rule(
        world.get_location(LocationName.Kibombo_Mountains_Power_Bread),
        lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Gabomba_Statue_Completed, player),
    )

    add_rule(
        world.get_location(LocationName.Kibombo_Mountains_Tear_Stone),
        lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Gabomba_Statue_Completed, player),
    )

    add_rule(
        world.get_location(LocationName.Waft),
        lambda state: state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Growth, player),
    )

    # Kibombo
    add_rule(world.get_location(LocationName.Kibombo_Piers), lambda state: state.has(ItemName.Lash_Pebble, player))

    # Gabomba Statue
    add_rule(
        world.get_location(LocationName.Gabomba_Statue_Ritual), lambda state: state.has(ItemName.Pound_Cube, player)
    )

    add_rule(world.get_location(LocationName.Steel), lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(
        world.get_location(LocationName.Gabomba_Statue_Black_Crystal),
        lambda state: state.has(ItemName.Gabomba_Statue_Completed, player),
    )

    # Gabomba Catacombs
    add_rule(
        world.get_location(LocationName.Gabomba_Catacombs_Tomegathericon),
        lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Frost_Jewel, player),
    )

    # Lemurian Ship
    if world.options.lemurian_ship < 2:
        add_rule(
            world.get_location(LocationName.Lemurian_Ship_Engine_Room),
            lambda state: state.has(ItemName.Aqua_Hydra_defeated, player) and state.has(ItemName.Douse_Drop, player),
        )

    add_rule(
        world.get_location(LocationName.Lemurian_Ship_Potion), lambda state: state.has(ItemName.Frost_Jewel, player)
    )
    add_rule(
        world.get_location(LocationName.Lemurian_Ship_Mist_Potion),
        lambda state: state.has(ItemName.Aqua_Hydra_defeated, player) and state.has(ItemName.Parch, player),
    )
    add_rule(
        world.get_location(LocationName.Lemurian_Ship_Aqua_Hydra),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 2 and state.has(ItemName.Frost_Jewel, player)
        ),
    )

    # East Tunderia Islet N/A

    # SouthEast Angara Islet
    add_rule(
        world.get_location(LocationName.SE_Angara_Islet_Red_Cloth),
        lambda state: (
            state.has(ItemName.Pretty_Stone, player)
            and state.has(ItemName.Frost_Jewel, player)
            and state.has(ItemName.Mind_Read, player)
        ),
    )

    # North Osenia Islet
    add_rule(
        world.get_location(LocationName.N_Osenia_Islet_Milk),
        lambda state: (
            state.has(ItemName.Red_Cloth, player)
            and state.has(ItemName.Sand, player)
            and state.has(ItemName.Mind_Read, player)
        ),
    )

    # West Indra Islet
    add_rule(
        world.get_location(LocationName.W_Indra_Islet_Lil_Turtle),
        lambda state: state.has(ItemName.Milk, player) and state.has(ItemName.Mind_Read, player),
    )

    # Sea of Time Islet N/A

    # Islet Cave
    add_rule(
        world.get_location(LocationName.Serac),
        lambda state: state.has(ItemName.Teleport_Lapis, player) and state.has(ItemName.Tremor_Bit, player),
    )

    # Apoji Islands
    add_rule(
        world.get_location(LocationName.Haze),
        lambda state: (
            state.has(ItemName.Sand, player)
            and state.has(ItemName.Whirlwind, player)
            and state.has(ItemName.Lash_Pebble, player)
        ),
    )

    # Aqua Rock
    add_rule(
        world.get_location(LocationName.Aqua_Rock_Water_of_Life), lambda state: state.has(ItemName.Frost_Jewel, player)
    )

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Parch),
        lambda state: (
            state.has(ItemName.Aquarius_Stone, player)
            and (state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player))
        ),
    )

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Mimic),
        lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Mist_Sabre), lambda state: state.has(ItemName.Frost_Jewel, player)
    )

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Aquarius_Stone),
        lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Lucky_Pepper),
        lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(world.get_location(LocationName.Aqua_Rock_Rusty_Sword), lambda state: state.has(ItemName.Parch, player))

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Crystal_Powder), lambda state: state.has(ItemName.Frost_Jewel, player)
    )

    add_rule(world.get_location(LocationName.Aqua_Rock_Vial), lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(
        world.get_location(LocationName.Aqua_Rock_Tear_Stone),
        lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player),
    )

    add_rule(world.get_location(LocationName.Steam), lambda state: state.has(ItemName.Parch, player))

    # Izumo
    add_rule(
        world.get_location(LocationName.Izumo_Ulysses),
        lambda state: (
            state.has(ItemName.Reveal, player)
            and state.has(ItemName.Sand, player)
            and state.has(ItemName.Frost_Jewel, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Parch, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Izumo_Phantasmal_Mail),
        lambda state: (
            state.has(ItemName.Reveal, player)
            and state.has(ItemName.Sand, player)
            and state.has(ItemName.Frost_Jewel, player)
            and state.has(ItemName.Pound_Cube, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Coal),
        lambda state: state.has(ItemName.Dancing_Idol, player) and state.has(ItemName.Serpent_defeated, player),
    )

    # Gaia Rock
    add_rule(
        world.get_location(LocationName.Gaia_Rock_Sand), lambda state: state.has(ItemName.Serpent_defeated, player)
    )

    add_rule(world.get_location(LocationName.Gaia_Rock_Mimic), lambda state: state.has(ItemName.Growth, player))

    add_rule(world.get_location(LocationName.Gaia_Rock_Rusty_Mace), lambda state: state.has(ItemName.Growth, player))

    add_rule(
        world.get_location(LocationName.Gaia_Rock_Dancing_Idol),
        lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Whirlwind, player),
    )

    add_rule(world.get_location(LocationName.Gaia_Rock_Apple), lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(
        world.get_location(LocationName.Gaia_Rock_Serpent),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 2
            and state.has(ItemName.Cyclone_Chip, player)
            and state.has(ItemName.Dancing_Idol, player)
            and state.has(ItemName.Growth, player)
        ),
    )

    # Tundaria Tower
    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Center_Prong),
        lambda state: state.has(ItemName.Burst_Brooch, player),
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Burst_Brooch),
        lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Reveal, player),
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Sylph_Feather),
        lambda state: state.has(ItemName.Burst_Brooch, player),
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Lucky_Medal),
        lambda state: state.has(ItemName.Burst_Brooch, player),
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Vial), lambda state: state.has(ItemName.Burst_Brooch, player)
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Lightning_Sword),
        lambda state: state.has(ItemName.Burst_Brooch, player),
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Hard_Nut), lambda state: state.has(ItemName.Pound_Cube, player)
    )

    add_rule(
        world.get_location(LocationName.Tundaria_Tower_Crystal_Powder),
        lambda state: state.has(ItemName.Pound_Cube, player),
    )

    # Ankohl Ruins
    add_rule(world.get_location(LocationName.Ankohl_Ruins_Left_Prong), lambda state: state.has(ItemName.Reveal, player))

    # Champa
    add_rule(
        world.get_location(LocationName.Champa_Avimander),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 2
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Briggs_escaped, player)
            and state.has(ItemName.Left_Prong, player)
            and state.has(ItemName.Center_Prong, player)
            and state.has(ItemName.Right_Prong, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Champa_Trident), lambda state: state.has(ItemName.Avimander_defeated, player)
    )

    add_rule(world.get_location(LocationName.Champa_Viking_Helm), lambda state: state.has(ItemName.Reveal, player))

    # Yallam
    add_rule(
        world.get_location(LocationName.Yallam_Masamune),
        lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Orb_of_Force, player),
    )

    # Taopo Swamp
    add_rule(
        world.get_location(LocationName.Taopo_Swamp_Tear_Stone),
        lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Scoop_Gem, player),
    )

    add_rule(
        world.get_location(LocationName.Taopo_Swamp_Tear_Stone_Two),
        lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Scoop_Gem, player),
    )

    add_rule(
        world.get_location(LocationName.Taopo_Swamp_Vial),
        lambda state: (
            state.has(ItemName.Whirlwind, player)
            and state.has(ItemName.Growth, player)
            and state.has(ItemName.Douse_Drop, player)
            and state.has(ItemName.Frost_Jewel, player)
        ),
    )

    # Sea Of Time
    add_rule(
        world.get_location(LocationName.Sea_of_Time_Poseidon),
        lambda state: state.count_group(ItemType.Character.name, player) >= 3 and state.has(ItemName.Trident, player),
    )

    # Lemuria
    add_rule(
        world.get_location(LocationName.Rime),
        lambda state: (
            state.has(ItemName.Grindstone, player)
            and state.has(ItemName.Cyclone_Chip, player)
            and state.has(ItemName.Tremor_Bit, player)
        ),
    )

    # If item shuffle everything is on a lucky medal is guaranteed in the pool,
    # otherwise there are guarenteed lucky medals in Lemuria
    if world.options.item_shuffle == 3:
        add_rule(
            world.get_location(LocationName.Lemuria_Eclipse), lambda state: state.has(ItemName.Lucky_Medal, player)
        )
    else:
        # If hidden items are enabled make sure Reveal is in logic as the guarenteed medals are hidden,
        # one in the castle barrel, one dug up with scoop. We can assume for now just Reveal is enough
        if world.options.reveal_hidden_item == 1:
            add_rule(world.get_location(LocationName.Lemuria_Eclipse), lambda state: state.has(ItemName.Reveal, player))

    # Western Sea

    # SW Atteka Islet
    add_rule(world.get_location(LocationName.Luff), lambda state: state.has(ItemName.Lifting_Gem, player))

    # Hesperia Settlement
    add_rule(
        world.get_location(LocationName.Hesperia_Settlement_166_coins), lambda state: state.has(ItemName.Growth, player)
    )

    add_rule(world.get_location(LocationName.Tinder), lambda state: state.has(ItemName.Growth, player))

    # Shaman Village Cave
    add_rule(
        world.get_location(LocationName.Eddy),
        lambda state: (
            state.has(ItemName.Whirlwind, player)
            and state.has(ItemName.Lifting_Gem, player)
            and state.has(ItemName.Frost_Jewel, player)
        ),
    )

    # Shaman Village
    add_rule(
        world.get_location(LocationName.Shaman_Village_Hover_Jade),
        lambda state: state.has(ItemName.Moapa_defeated, player),
    )

    add_rule(
        world.get_location(LocationName.Shaman_Village_Hard_Nut),
        lambda state: state.has_all([ItemName.Shamans_Rod, ItemName.Whirlwind], player),
    )

    add_rule(
        world.get_location(LocationName.Shaman_Village_Spirit_Gloves), lambda state: state.has(ItemName.Growth, player)
    )

    add_rule(
        world.get_location(LocationName.Aroma),
        lambda state: state.has(ItemName.Moapa_defeated, player) and state.has(ItemName.Lash_Pebble, player),
    )

    add_rule(
        world.get_location(LocationName.Gasp),
        lambda state: (
            state.has(ItemName.Shamans_Rod, player)
            and state.has(ItemName.Whirlwind, player)
            and state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Lifting_Gem, player)
            and state.has(ItemName.Reveal, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Shaman_Village_Elixir_Two),
        lambda state: (
            state.has(ItemName.Shamans_Rod, player)
            and state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Lifting_Gem, player)
            and state.has(ItemName.Whirlwind, player)
            and state.has(ItemName.Reveal, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Shaman_Village_Moapa),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 3
            and state.has_all([ItemName.Shamans_Rod, ItemName.Whirlwind], player)
        ),
    )

    # Atteka Inlet
    add_rule(
        world.get_location(LocationName.Geode),
        lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Lifting_Gem, player),
    )

    # Contigo
    add_rule(world.get_location(LocationName.Contigo_Dragon_Skin), lambda state: state.has(ItemName.Reveal, player))

    add_rule(world.get_location(LocationName.Salt), lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(world.get_location(LocationName.Shine), lambda state: state.has(ItemName.Orb_of_Force, player))

    # Jupiter Lighthouse
    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Mimic),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Erinyes_Tunic),
        lambda state: state.has(ItemName.Hover_Jade, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Potion),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Psy_Crystal),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Meditation_Rod),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Red_Key),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Blue_Key),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Mist_Potion),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_306_coins),
        lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Water_of_Life),
        lambda state: (
            state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Blue_Key, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Phaetons_Blade),
        lambda state: (
            state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Blue_Key, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Whorl),
        lambda state: (
            state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Blue_Key, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst),
        lambda state: (
            state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Blue_Key, player)
            and state.has(ItemName.Red_Key, player)
        ),
    )

    # Atteka Cavern
    add_rule(world.get_location(LocationName.Atteka_Cavern_Coatlicue), lambda state: state.has(ItemName.Parch, player))

    # Gondowan Settlement
    add_rule(
        world.get_location(LocationName.Gondowan_Settlement_Star_Dust),
        lambda state: state.has(ItemName.Cyclone_Chip, player),
    )

    # Magma Rock
    add_rule(
        world.get_location(LocationName.Magma_Rock_Oil_Drop), lambda state: state.has(ItemName.Burst_Brooch, player)
    )

    add_rule(
        world.get_location(LocationName.Magma_Rock_383_coins),
        lambda state: state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Growth, player),
    )

    add_rule(
        world.get_location(LocationName.Magma_Rock_Salamander_Tail),
        lambda state: (
            state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Growth, player)
            and state.has(ItemName.Lash_Pebble, player)
        ),
    )

    # Magma Rock Interior
    add_rule(world.get_location(LocationName.Magma_Rock_Magma_Ball), lambda state: state.has(ItemName.Blaze, player))

    add_rule(
        world.get_location(LocationName.Magma_Rock_Golem_Core), lambda state: state.has(ItemName.Whirlwind, player)
    )

    if world.options.shortcut_magma_rock:
        add_rule(
            world.get_location(LocationName.Magma_Rock_Lucky_Medal),
            lambda state: state.has(ItemName.Burst_Brooch, player),
        )
        add_rule(
            world.get_location(LocationName.Magma_Rock_Mist_Potion),
            lambda state: state.has(ItemName.Burst_Brooch, player),
        )
        add_rule(
            world.get_location(LocationName.Magma_Rock_Salamander_Tail_Two),
            lambda state: state.has(ItemName.Burst_Brooch, player),
        )
        add_rule(
            world.get_location(LocationName.Magma_Rock_Golem_Core),
            lambda state: state.has(ItemName.Burst_Brooch, player),
        )
    else:
        add_rule(
            world.get_location(LocationName.Magma_Rock_Salamander_Tail_Two),
            lambda state: state.has(ItemName.Whirlwind, player),
        )
        add_rule(world.get_location(LocationName.Magma_Rock_Blaze), lambda state: state.has(ItemName.Whirlwind, player))
        add_rule(
            world.get_location(LocationName.Magma_Rock_Magma_Ball), lambda state: state.has(ItemName.Whirlwind, player)
        )

    # Loho
    add_rule(world.get_location(LocationName.Loho_Ship_Cannon), lambda state: state.has(ItemName.Magma_Ball, player))
    add_rule(
        world.get_location(LocationName.Loho_Golem_Core),
        lambda state: state.has(ItemName.Ship_Cannon, player) and state.has(ItemName.Scoop_Gem, player),
    )
    add_rule(
        world.get_location(LocationName.Loho_Golem_Core_Two),
        lambda state: (
            state.has(ItemName.Ship_Cannon, player)
            and state.has(ItemName.Scoop_Gem, player)
            and state.has(ItemName.Lifting_Gem, player)
        ),
    )
    add_rule(world.get_location(LocationName.Lull), lambda state: state.has(ItemName.Ship_Cannon, player))

    # Angara Cavern
    add_rule(
        world.get_location(LocationName.Angara_Cavern_Haures), lambda state: state.has(ItemName.Carry_Stone, player)
    )

    # Kalt Island
    add_rule(world.get_location(LocationName.Gel), lambda state: state.has(ItemName.Lash_Pebble, player))

    # Prox
    add_rule(
        world.get_location(LocationName.Prox_Dark_Matter),
        lambda state: state.has(ItemName.Scoop_Gem, player) and state.has(ItemName.Lifting_Gem, player),
    )

    add_rule(world.get_location(LocationName.Mold), lambda state: state.has(ItemName.Scoop_Gem, player))

    # Mars Lighthouse
    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Mimic), lambda state: state.has(ItemName.Pound_Cube, player)
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Teleport_Lapis),
        lambda state: (
            state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Grindstone, player)
            and (state.has(ItemName.Blaze, player) or state.has(ItemName.Teleport_Lapis, player))
        ),
    )

    add_rule(
        world.get_location(LocationName.Balm),
        lambda state: (
            state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Grindstone, player)
            and (state.has(ItemName.Blaze, player) or state.has(ItemName.Teleport_Lapis, player))
        ),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Mars_Star),
        lambda state: state.has(ItemName.Flame_Dragons_defeated, player),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Heated),
        lambda state: state.has(ItemName.Flame_Dragons_defeated, player) and state.has(ItemName.Mars_Star, player),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Orihalcon),
        lambda state: (
            state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Blaze, player)
            and state.has(ItemName.Grindstone, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Valkyrie_Mail),
        lambda state: (
            state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Blaze, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Teleport_Lapis, player)
            and state.has(ItemName.Grindstone, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Sol_Blade),
        lambda state: (
            state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Blaze, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Teleport_Lapis, player)
            and state.has(ItemName.Grindstone, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Flame_Dragons),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 3
            and state.has(ItemName.Teleport_Lapis, player)
            and state.has(ItemName.Pound_Cube, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Grindstone, player)
            and state.has(ItemName.Blaze, player)
            and state.has(ItemName.Reveal, player)
        ),
    )

    # Mars Lighthouse activated
    if world.options.shortcut_mars_lighthouse == 0:
        add_rule(
            world.get_location(LocationName.Fugue), lambda state: state.has(ItemName.Mars_Lighthouse_Heated, player)
        )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Psy_Crystal),
        lambda state: (
            state.has(ItemName.Cyclone_Chip, player)
            and state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Reveal, player)
        ),
    )

    add_rule(
        world.get_location(LocationName.Mars_Lighthouse_Doom_Dragon),
        lambda state: (
            state.count_group(ItemType.Character.name, player) >= 3
            and state.has(ItemName.Cyclone_Chip, player)
            and state.has(ItemName.Hover_Jade, player)
            and state.has(ItemName.Frost_Jewel, player)
            and state.has(ItemName.Burst_Brooch, player)
            and state.has(ItemName.Blaze, player)
            and state.has(ItemName.Carry_Stone, player)
            and state.has(ItemName.Sand, player)
            and state.has(ItemName.Reveal, player)
            and state.has(ItemName.Teleport_Lapis, player)
        ),
    )

    # djinn logic
    if world.options.djinn_logic > 0:
        djinn_percentage = world.options.djinn_logic / 100

        add_rule(
            world.get_location(LocationName.Yampi_Desert_King_Scorpion),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(3 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Alhafra_Briggs),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(6 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Lemurian_Ship_Aqua_Hydra),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(10 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Gaia_Rock_Serpent),
            lambda state: (
                state.count_group(ItemType.Djinn.name, player) >= math.ceil(24 * djinn_percentage)
                or (
                    state.count_group(ItemType.Djinn.name, player) >= math.ceil(16 * djinn_percentage)
                    and state.has(ItemName.Whirlwind, player)
                )
            ),
        )

        add_rule(
            world.get_location(LocationName.Champa_Avimander),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(20 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Sea_of_Time_Poseidon),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(24 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Shaman_Village_Moapa),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(28 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Mars_Lighthouse_Flame_Dragons),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(48 * djinn_percentage),
        )

        add_rule(
            world.get_location(LocationName.Mars_Lighthouse_Doom_Dragon),
            lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(56 * djinn_percentage),
        )

    else:
        # Force whirldwind to be able to get all 4 light orbs to make serpent as weak as possible
        # to beat it logically without djinn
        add_rule(
            world.get_location(LocationName.Gaia_Rock_Serpent), lambda state: state.has(ItemName.Whirlwind, player)
        )

    # Optional Super Boss content
    if world.options.omit_locations < 2:
        add_rule(
            world.get_location(LocationName.Yampi_Desert_Cave_Valukar),
            lambda state: (
                state.count_group(ItemType.Character.name, player) >= 7 and state.has(ItemName.Pound_Cube, player)
            ),
        )
        add_rule(
            world.get_location(LocationName.Islet_Cave_Sentinel),
            lambda state: (
                state.count_group(ItemType.Character.name, player) >= 7 and state.has(ItemName.Teleport_Lapis, player)
            ),
        )
        add_rule(
            world.get_location(LocationName.Treasure_Isle_Star_Magician),
            lambda state: state.count_group(ItemType.Character.name, player) >= 7,
        )

        add_rule(
            world.get_location(LocationName.Yampi_Desert_Cave_Daedalus),
            lambda state: state.has(ItemName.Valukar_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Islet_Cave_Catastrophe),
            lambda state: state.has(ItemName.Sentinel_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Treasure_Isle_Azul),
            lambda state: state.has(ItemName.Star_Magician_defeated, player),
        )
        if world.options.djinn_logic.value > 0:
            add_rule(
                world.get_location(LocationName.Yampi_Desert_Cave_Valukar),
                lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(64 * djinn_percentage),
            )

            add_rule(
                world.get_location(LocationName.Islet_Cave_Sentinel),
                lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(64 * djinn_percentage),
            )

            add_rule(
                world.get_location(LocationName.Treasure_Isle_Star_Magician),
                lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(64 * djinn_percentage),
            )

    if world.options.omit_locations < 1:
        # Anemos Inner Sanctum
        add_rule(
            world.get_location(LocationName.Anemos_Inner_Sanctum_Dullahan),
            lambda state: (
                state.count_group(ItemType.Character.name, player) >= 7
                and state.has(ItemName.Lifting_Gem, player)
                and state.has(ItemName.Sand, player)
                and state.has(ItemName.Hover_Jade, player)
            ),
        )

        add_rule(
            world.get_location(LocationName.Anemos_Inner_Sanctum_Iris),
            lambda state: state.has(ItemName.Dullahan_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Anemos_Inner_Sanctum_Orihalcon),
            lambda state: state.has(ItemName.Lifting_Gem, player),
        )

        if world.options.djinn_logic.value > 0:
            add_rule(
                world.get_location(LocationName.Anemos_Inner_Sanctum_Dullahan),
                lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(72 * djinn_percentage),
            )

    # Hidden Items
    if world.options.item_shuffle > 2:
        add_rule(
            world.get_location(LocationName.Daila_Psy_Crystal), lambda state: state.has(ItemName.Scoop_Gem, player)
        )

        add_rule(
            world.get_location(LocationName.Yampi_Desert_315_coins), lambda state: state.has(ItemName.Scoop_Gem, player)
        )

        add_rule(
            world.get_location(LocationName.Alhafra_Lucky_Medal),
            lambda state: state.has(ItemName.Briggs_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Alhafran_Cave_Power_Bread),
            lambda state: state.has(ItemName.Briggs_escaped, player),
        )

        add_rule(
            world.get_location(LocationName.Kibombo_Mountains_Smoke_Bomb),
            lambda state: (
                state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Gabomba_Statue_Completed, player)
            ),
        )

        add_rule(
            world.get_location(LocationName.Kibombo_Lucky_Medal),
            lambda state: state.has(ItemName.Gabomba_Statue_Completed, player),
        )

        add_rule(
            world.get_location(LocationName.Kibombo_Nut),
            lambda state: state.has(ItemName.Gabomba_Statue_Completed, player),
        )

        add_rule(
            world.get_location(LocationName.Apojii_Islands_Bramble_Seed),
            lambda state: state.has(ItemName.Cyclone_Chip, player),
        )

        add_rule(
            world.get_location(LocationName.Apojii_Islands_Mint), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Apojii_Islands_Herb), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Izumo_Antidote), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Izumo_Antidote_Two), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Izumo_Lucky_Medal), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Gaia_Rock_Cloud_Brand),
            lambda state: state.has(ItemName.Sand, player) and state.has(ItemName.Growth, player),
        )

        add_rule(world.get_location(LocationName.Yallam_Nut), lambda state: state.has(ItemName.Cyclone_Chip, player))

        add_rule(
            world.get_location(LocationName.Yallam_Antidote), lambda state: state.has(ItemName.Cyclone_Chip, player)
        )

        add_rule(
            world.get_location(LocationName.Taopo_Swamp_Star_Dust),
            lambda state: (
                state.has(ItemName.Whirlwind, player)
                and state.has(ItemName.Growth, player)
                and state.has(ItemName.Douse_Drop, player)
                and state.has(ItemName.Frost_Jewel, player)
                and state.has(ItemName.Tremor_Bit, player)
                and state.has(ItemName.Scoop_Gem, player)
            ),
        )

        add_rule(
            world.get_location(LocationName.Taopo_Swamp_Bramble_Seed),
            lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Cyclone_Chip, player),
        )

        add_rule(
            world.get_location(LocationName.Lemuria_Lucky_Medal), lambda state: state.has(ItemName.Scoop_Gem, player)
        )

        add_rule(
            world.get_location(LocationName.Lemuria_Rusty_Sword), lambda state: state.has(ItemName.Scoop_Gem, player)
        )

        add_rule(
            world.get_location(LocationName.Lemuria_Hard_Nut),
            lambda state: state.has(ItemName.Growth, player) and state.has(ItemName.Cyclone_Chip, player),
        )

        add_rule(world.get_location(LocationName.Lemuria_Bone), lambda state: state.has(ItemName.Scoop_Gem, player))

        add_rule(
            world.get_location(LocationName.Lemuria_Star_Dust), lambda state: state.has(ItemName.Scoop_Gem, player)
        )

        add_rule(
            world.get_location(LocationName.Lemurian_Ship_Antidote),
            lambda state: state.has(ItemName.Frost_Jewel, player),
        )

        add_rule(
            world.get_location(LocationName.Lemurian_Ship_Oil_Drop),
            lambda state: state.has(ItemName.Frost_Jewel, player),
        )

        add_rule(
            world.get_location(LocationName.Overworld_Rusty_Sword_Two),
            lambda state: state.has(ItemName.Wings_of_Anemos, player) and state.has(ItemName.Hover_Jade, player),
        )

        add_rule(
            world.get_location(LocationName.Shaman_Village_Weasels_Claw),
            lambda state: state.has(ItemName.Shamans_Rod, player),
        )

        add_rule(
            world.get_location(LocationName.Shaman_Village_Lucky_Medal),
            lambda state: state.has(ItemName.Moapa_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Shaman_Village_Lucky_Pepper),
            lambda state: state.has(ItemName.Moapa_defeated, player),
        )

        add_rule(
            world.get_location(LocationName.Contigo_Bramble_Seed),
            lambda state: state.has(ItemName.Cyclone_Chip, player),
        )

        add_rule(
            world.get_location(LocationName.Loho_Mythril_Silver),
            lambda state: state.has(ItemName.Ship_Cannon, player) and state.has(ItemName.Scoop_Gem, player),
        )

        if world.options.reveal_hidden_item == 1:
            # for all hidden items that are not eventType 131 (TreasureType.FIELD_ITEM)
            # (these include scoopable or cyclone places), we require reveal
            reveal_required_locs = [
                LocationName.Daila_Psy_Crystal,
                LocationName.Loho_Mythril_Silver,
                LocationName.Lemuria_Lucky_Medal,
                LocationName.Lemuria_Rusty_Sword,
                LocationName.Lemuria_Bone,
                LocationName.Lemuria_Star_Dust,
            ]

            for loc in game_data.locations_by_type[LocationType.Hidden]:
                item_treasure_type = game_data.chest_locations[loc.id].treasure_type
                if item_treasure_type != TreasureType.FIELD_ITEM or loc.name in reveal_required_locs:
                    add_rule(world.get_location(loc.name), lambda state: state.has(ItemName.Reveal, player))
