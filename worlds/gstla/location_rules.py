from __future__ import annotations

import math
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, HasAny, HasGroup, Or
from worlds.generic.Rules import add_rule
from worlds.gstla.options import ItemShuffle, RevealHiddenItem, ShortcutMagmaRock, ShortcutMarsLighthouse, StartWithShip
from .game_data.loader import load_game_data
from .gstla_types import LocationType, TreasureType
from .items import ItemType
from .names import ItemName, LocationName
from .options import DjinnLogic
from .resolvers import DjinnLogicCount, has_djinn

if TYPE_CHECKING:
    from collections.abc import Mapping

    from rule_builder.rules import Rule
    from .world import GSTLAWorld


MAGMA_SHORTCUT = [OptionFilter(ShortcutMagmaRock, 1)]
NO_MAGMA_SHORTCUT = [OptionFilter(ShortcutMagmaRock, 0)]

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


# Character-brought djinns
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
PARTY_DJINN_RULES: Mapping[str, Rule] = {
    djinn: HasGroup(ItemType.Character.name, party_size)
    for party_size, djinns in DJINNS_BY_PARTY_SIZE.items()
    for djinn in djinns
}

# Characters
CHARACTER_RULES: dict[str, Rule] = {
    LocationName.Idejima_Mind_Read: Has(ItemName.Sheba),
    LocationName.Idejima_Whirlwind: Has(ItemName.Sheba),
    LocationName.Kibombo_Douse_Drop: Has(ItemName.Piers),
    LocationName.Kibombo_Frost_Jewel: Has(ItemName.Piers),
    LocationName.Contigo_Carry_Stone: Has(ItemName.Mia),
    LocationName.Contigo_Lifting_Gem: Has(ItemName.Ivan),
    LocationName.Contigo_Orb_of_Force: Has(ItemName.Garet),
    LocationName.Contigo_Catch_Beads: Has(ItemName.Isaac),
}


LOCATION_RULES: dict[str, Rule] = {**PARTY_DJINN_RULES, **CHARACTER_RULES}


def set_location_rules(world: GSTLAWorld) -> None:
    # The rest
    for location in world.get_locations():
        if location.name not in LOCATION_RULES:
            continue

        rule = LOCATION_RULES[location.name]
        world.set_rule(location, rule)


AREA_RULES: dict[str, Rule] = {
    # TODO: Should we prefix djinns? Like LocationName.Kandorean_Fog?
    # TODO: Are there some missing? Like Madra_Catacombs_Apple?
    # Daila
    LocationName.Daila_Sea_Gods_Tear: Has(ItemName.Frost_Jewel),
    # Kandorean Temple
    LocationName.Fog: Has(ItemName.Lash_Pebble),
    # Dehkan Platea
    LocationName.Cannon: Has(ItemName.Pound_Cube),
    LocationName.Dehkan_Plateau_Nut: Has(ItemName.Lash_Pebble),
    # Shrine of the Sea God
    LocationName.Shrine_of_the_Sea_God_Rusty_Staff: Has(ItemName.Frost_Jewel),
    LocationName.Shrine_of_the_Sea_God_Right_Prong: HasAll(
        ItemName.Frost_Jewel, ItemName.Reveal, ItemName.Sea_Gods_Tear
    ),
    # Indra Cavern
    LocationName.Indra_Cavern_Zagan: Has(ItemName.Lash_Pebble),
    # Madra
    LocationName.Madra_Cyclone_Chip: Has(ItemName.Gabomba_Statue_Completed),
    LocationName.Char: Has(ItemName.Healing_Fungus),
    # Madra Catacombs
    LocationName.Madra_Catacombs_Ruin_Key: HasAll(ItemName.Tremor_Bit, ItemName.Lash_Pebble, ItemName.Frost_Jewel),
    LocationName.Madra_Catacombs_Mist_Potion: HasAll(ItemName.Lash_Pebble, ItemName.Frost_Jewel),
    LocationName.Madra_Catacombs_Moloch: Has(ItemName.Ruin_Key),
    # Yampi Desert
    LocationName.Blitz: Has(ItemName.Pound_Cube),
    LocationName.Yampi_Desert_Guardian_Ring: HasAny(ItemName.Pound_Cube, ItemName.Sand),
    LocationName.Yampi_Desert_Antidote: HasAny(ItemName.Pound_Cube, ItemName.Sand),
    LocationName.Yampi_Desert_King_Scorpion: And(Has(ItemName.Pound_Cube), has_djinn(3)),
    LocationName.Yampi_Desert_Scoop_Gem: Has(ItemName.King_Scorpion_defeated),
    # Yamp Desert Backside
    LocationName.Yampi_Desert_Lucky_Medal: Has(ItemName.Reveal),
    LocationName.Yampi_Desert_Trainers_Whip: HasAny(ItemName.Lash_Pebble, ItemName.Sand),
    LocationName.Yampi_Desert_Blow_Mace: Has(ItemName.Pound_Cube),
    LocationName.Yampi_Desert_Cave_Water_of_Life: Has(ItemName.Sand),
    # Yampi Desert Cave
    LocationName.Yampi_Desert_Cave_Mythril_Silver: Has(ItemName.Scoop_Gem),
    LocationName.Crystal: Has(ItemName.Scoop_Gem),
    # Alhafra
    LocationName.Alhafra_Psy_Crystal: Has(ItemName.Reveal),
    LocationName.Alhafra_Briggs: has_djinn(6),
    LocationName.Alhafra_Prison_Briggs: HasAll(
        ItemName.Briggs_defeated, ItemName.Lash_Pebble, ItemName.Burst_Brooch, ItemName.Pound_Cube
    ),
    # Alhafra Cave
    LocationName.Alhafran_Cave_123_coins: HasAll(ItemName.Lash_Pebble, ItemName.Pound_Cube),
    LocationName.Alhafran_Cave_Ixion_Mail: HasAll(ItemName.Lash_Pebble, ItemName.Pound_Cube),
    LocationName.Alhafran_Cave_Lucky_Medal: HasAll(ItemName.Lash_Pebble, ItemName.Pound_Cube),
    LocationName.Alhafran_Cave_777_coins: HasAll(ItemName.Briggs_escaped, ItemName.Frost_Jewel),
    LocationName.Alhafran_Cave_Potion: HasAll(ItemName.Briggs_escaped, ItemName.Frost_Jewel),
    LocationName.Alhafran_Cave_Psy_Crystal: HasAll(ItemName.Briggs_escaped, ItemName.Frost_Jewel),
    # Mikasalla
    LocationName.Spark: Has(ItemName.Scoop_Gem),
    # Osenia Cliffs
    LocationName.Osenia_Cliffs_Pirates_Sword: Has(ItemName.Lash_Pebble),
    # Osenia Cavern
    LocationName.Osenia_Cavern_Megaera: Has(ItemName.Scoop_Gem),
    # Garoh
    LocationName.Garoh_Hypnos_Sword: Has(ItemName.Reveal),
    LocationName.Ether: Has(ItemName.Reveal),
    # Airs Rock
    LocationName.Airs_Rock_Vial: Has(ItemName.Frost_Jewel),
    LocationName.Airs_Rock_Psy_Crystal: Has(ItemName.Reveal),
    # Gondowan Cliffs
    LocationName.Gondowan_Cliffs_Healing_Fungus: Has(ItemName.Frost_Jewel),
    # Naribwe
    LocationName.Naribwe_Thorn_Crown: Has(ItemName.Lash_Pebble),
    LocationName.Naribwe_Unicorn_Ring: HasAll(ItemName.Whirlwind, ItemName.Reveal),
    # Kibombo Mountains
    LocationName.Kibombo_Mountains_Power_Bread: HasAny(ItemName.Lash_Pebble, ItemName.Gabomba_Statue_Completed),
    LocationName.Kibombo_Mountains_Tear_Stone: HasAny(ItemName.Lash_Pebble, ItemName.Gabomba_Statue_Completed),
    LocationName.Waft: HasAll(ItemName.Frost_Jewel, ItemName.Growth),
    # Kibombo
    LocationName.Kibombo_Piers: Has(ItemName.Lash_Pebble),
    # Gabomba Statue
    LocationName.Gabomba_Statue_Ritual: Has(ItemName.Pound_Cube),
    LocationName.Steel: Has(ItemName.Pound_Cube),
    LocationName.Gabomba_Statue_Black_Crystal: Has(ItemName.Gabomba_Statue_Completed),
    # Gabomba Catacombs
    LocationName.Gabomba_Catacombs_Tomegathericon: HasAll(ItemName.Reveal, ItemName.Frost_Jewel),
    # Lemurian Ship
    LocationName.Lemurian_Ship_Engine_Room: HasAll(
        ItemName.Aqua_Hydra_defeated,
        ItemName.Douse_Drop,
        options=[OptionFilter(StartWithShip, StartWithShip.option_available_from_start, 'lt')],
        filtered_resolution=True,
    ),
    LocationName.Lemurian_Ship_Potion: Has(ItemName.Frost_Jewel),
    LocationName.Lemurian_Ship_Mist_Potion: HasAll(ItemName.Aqua_Hydra_defeated, ItemName.Parch),
    LocationName.Lemurian_Ship_Aqua_Hydra: And(
        HasGroup(ItemType.Character.name, 2), Has(ItemName.Frost_Jewel), has_djinn(10)
    ),
    # East Tunderia Islet N/A
    # SouthEast Angara Islet
    LocationName.SE_Angara_Islet_Red_Cloth: HasAll(ItemName.Pretty_Stone, ItemName.Frost_Jewel, ItemName.Mind_Read),
    # North Osenia Islet
    LocationName.N_Osenia_Islet_Milk: HasAll(ItemName.Red_Cloth, ItemName.Sand, ItemName.Mind_Read),
    # West Indra Islet
    LocationName.W_Indra_Islet_Lil_Turtle: HasAll(ItemName.Milk, ItemName.Mind_Read),
    # Sea of Time Islet N/A
    # Islet Cave
    LocationName.Serac: HasAll(ItemName.Teleport_Lapis, ItemName.Tremor_Bit),
    # Apoji Islands
    LocationName.Haze: HasAll(ItemName.Sand, ItemName.Whirlwind, ItemName.Lash_Pebble),
    # Aqua Rock
    LocationName.Aqua_Rock_Water_of_Life: Has(ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Parch: And(Has(ItemName.Aquarius_Stone), HasAny(ItemName.Parch, ItemName.Frost_Jewel)),
    LocationName.Aqua_Rock_Mimic: HasAny(ItemName.Parch, ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Mist_Sabre: Has(ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Aquarius_Stone: HasAny(ItemName.Parch, ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Lucky_Pepper: HasAny(ItemName.Parch, ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Rusty_Sword: Has(ItemName.Parch),
    LocationName.Aqua_Rock_Crystal_Powder: Has(ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Vial: Has(ItemName.Frost_Jewel),
    LocationName.Aqua_Rock_Tear_Stone: HasAny(ItemName.Parch, ItemName.Frost_Jewel),
    LocationName.Steam: Has(ItemName.Parch),
    # Izumo
    LocationName.Izumo_Ulysses: HasAll(
        ItemName.Reveal, ItemName.Sand, ItemName.Frost_Jewel, ItemName.Pound_Cube, ItemName.Parch
    ),
    LocationName.Izumo_Phantasmal_Mail: HasAll(
        ItemName.Reveal, ItemName.Sand, ItemName.Frost_Jewel, ItemName.Pound_Cube
    ),
    LocationName.Coal: HasAll(ItemName.Dancing_Idol, ItemName.Serpent_defeated),
    # Gaia Rock
    LocationName.Gaia_Rock_Sand: Has(ItemName.Serpent_defeated),
    LocationName.Gaia_Rock_Mimic: Has(ItemName.Growth),
    LocationName.Gaia_Rock_Rusty_Mace: Has(ItemName.Growth),
    LocationName.Gaia_Rock_Dancing_Idol: HasAll(ItemName.Reveal, ItemName.Whirlwind),
    LocationName.Gaia_Rock_Apple: Has(ItemName.Whirlwind),
    LocationName.Gaia_Rock_Serpent: And(
        HasGroup(ItemType.Character.name, 2),
        Has(ItemName.Cyclone_Chip),
        Has(ItemName.Dancing_Idol),
        Has(ItemName.Growth),
        Or(
            HasGroup(ItemType.Djinn.name, DjinnLogicCount(24), options=[OptionFilter(DjinnLogic, 0, 'gt')]),
            # Force whirlwind to be able to get all 4 light orbs to make serpent as weak as possible
            # to beat it logically without djinn
            And(has_djinn(16), Has(ItemName.Whirlwind)),
        ),
    ),
    # Tundaria Tower
    LocationName.Tundaria_Tower_Center_Prong: Has(ItemName.Burst_Brooch),
    LocationName.Tundaria_Tower_Burst_Brooch: HasAll(ItemName.Pound_Cube, ItemName.Reveal),
    LocationName.Tundaria_Tower_Sylph_Feather: Has(ItemName.Burst_Brooch),
    LocationName.Tundaria_Tower_Lucky_Medal: Has(ItemName.Burst_Brooch),
    LocationName.Tundaria_Tower_Vial: Has(ItemName.Burst_Brooch),
    LocationName.Tundaria_Tower_Lightning_Sword: Has(ItemName.Burst_Brooch),
    LocationName.Tundaria_Tower_Hard_Nut: Has(ItemName.Pound_Cube),
    LocationName.Tundaria_Tower_Crystal_Powder: Has(ItemName.Pound_Cube),
    # Ankohl Ruins
    LocationName.Ankohl_Ruins_Left_Prong: Has(ItemName.Reveal),
    # Champa
    LocationName.Champa_Avimander: And(
        HasGroup(ItemType.Character.name, 2),
        Has(ItemName.Reveal),
        Has(ItemName.Briggs_escaped),
        Has(ItemName.Left_Prong),
        Has(ItemName.Center_Prong),
        Has(ItemName.Right_Prong),
        has_djinn(20),
    ),
    LocationName.Champa_Trident: Has(ItemName.Avimander_defeated),
    LocationName.Champa_Viking_Helm: Has(ItemName.Reveal),
    # Yallam
    LocationName.Yallam_Masamune: HasAll(ItemName.Cyclone_Chip, ItemName.Orb_of_Force),
    # Taopo Swamp
    LocationName.Taopo_Swamp_Tear_Stone: HasAll(ItemName.Whirlwind, ItemName.Scoop_Gem),
    LocationName.Taopo_Swamp_Tear_Stone_Two: HasAll(ItemName.Whirlwind, ItemName.Scoop_Gem),
    LocationName.Taopo_Swamp_Vial: HasAll(
        ItemName.Whirlwind, ItemName.Growth, ItemName.Douse_Drop, ItemName.Frost_Jewel
    ),
    # Sea Of Time
    LocationName.Sea_of_Time_Poseidon: And(HasGroup(ItemType.Character.name, 3), Has(ItemName.Trident), has_djinn(24)),
    # Lemuria
    LocationName.Rime: HasAll(ItemName.Grindstone, ItemName.Cyclone_Chip, ItemName.Tremor_Bit),
    LocationName.Lemuria_Eclipse: And(
        # If "item shuffle: everything" is enabled, a lucky medal is guaranteed in the pool,
        # otherwise there are guaranteed lucky medals in Lemuria.
        # If hidden items are enabled make sure Reveal is in logic as the guarenteed medals are hidden,
        # one in the castle barrel, one dug up with scoop. We can assume for now just Reveal is enough
        Has(ItemName.Lucky_Medal, options=[OptionFilter(ItemShuffle, 3)], filtered_resolution=True),
        Has(
            ItemName.Reveal,
            options=[OptionFilter(ItemShuffle, 3, 'ne'), OptionFilter(RevealHiddenItem, 1)],
            filtered_resolution=True,
        ),
    ),
    # SW Atteka Islet
    LocationName.Luff: Has(ItemName.Lifting_Gem),
    # Hesperia Settlement
    LocationName.Hesperia_Settlement_166_coins: Has(ItemName.Growth),
    LocationName.Tinder: Has(ItemName.Growth),
    # Shaman Village Cave
    LocationName.Eddy: HasAll(ItemName.Whirlwind, ItemName.Lifting_Gem, ItemName.Frost_Jewel),
    # Shaman Village
    LocationName.Shaman_Village_Hover_Jade: Has(ItemName.Moapa_defeated),
    LocationName.Shaman_Village_Hard_Nut: HasAll(ItemName.Shamans_Rod, ItemName.Whirlwind),
    LocationName.Shaman_Village_Spirit_Gloves: Has(ItemName.Growth),
    LocationName.Aroma: HasAll(ItemName.Moapa_defeated, ItemName.Lash_Pebble),
    LocationName.Gasp: HasAll(
        ItemName.Shamans_Rod, ItemName.Whirlwind, ItemName.Hover_Jade, ItemName.Lifting_Gem, ItemName.Reveal
    ),
    LocationName.Shaman_Village_Elixir_Two: HasAll(
        ItemName.Shamans_Rod, ItemName.Hover_Jade, ItemName.Lifting_Gem, ItemName.Whirlwind, ItemName.Reveal
    ),
    LocationName.Shaman_Village_Moapa: And(
        HasGroup(ItemType.Character.name, 3), HasAll(ItemName.Shamans_Rod, ItemName.Whirlwind), has_djinn(28)
    ),
    # Atteka Inlet
    LocationName.Geode: HasAll(ItemName.Cyclone_Chip, ItemName.Lifting_Gem),
    # Contigo
    LocationName.Contigo_Dragon_Skin: Has(ItemName.Reveal),
    LocationName.Salt: Has(ItemName.Scoop_Gem),
    LocationName.Shine: Has(ItemName.Orb_of_Force),
    # Jupiter Lighthouse
    LocationName.Jupiter_Lighthouse_Mimic: HasAll(ItemName.Hover_Jade, ItemName.Red_Key),
    LocationName.Jupiter_Lighthouse_Erinyes_Tunic: Has(ItemName.Hover_Jade),
    LocationName.Jupiter_Lighthouse_Potion: HasAll(ItemName.Hover_Jade, ItemName.Reveal),
    LocationName.Jupiter_Lighthouse_Psy_Crystal: HasAll(ItemName.Hover_Jade, ItemName.Reveal),
    LocationName.Jupiter_Lighthouse_Meditation_Rod: HasAll(ItemName.Hover_Jade, ItemName.Reveal),
    LocationName.Jupiter_Lighthouse_Red_Key: HasAll(ItemName.Hover_Jade, ItemName.Reveal),
    LocationName.Jupiter_Lighthouse_Blue_Key: HasAll(ItemName.Hover_Jade, ItemName.Red_Key),
    LocationName.Jupiter_Lighthouse_Mist_Potion: HasAll(ItemName.Hover_Jade, ItemName.Red_Key),
    LocationName.Jupiter_Lighthouse_306_coins: HasAll(ItemName.Hover_Jade, ItemName.Red_Key),
    LocationName.Jupiter_Lighthouse_Water_of_Life: HasAll(
        ItemName.Hover_Jade, ItemName.Reveal, ItemName.Pound_Cube, ItemName.Blue_Key
    ),
    LocationName.Jupiter_Lighthouse_Phaetons_Blade: HasAll(
        ItemName.Hover_Jade, ItemName.Reveal, ItemName.Pound_Cube, ItemName.Blue_Key
    ),
    LocationName.Whorl: HasAll(ItemName.Hover_Jade, ItemName.Reveal, ItemName.Pound_Cube, ItemName.Blue_Key),
    LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst: HasAll(
        ItemName.Hover_Jade, ItemName.Reveal, ItemName.Pound_Cube, ItemName.Blue_Key, ItemName.Red_Key
    ),
    # Atteka Cavern
    LocationName.Atteka_Cavern_Coatlicue: Has(ItemName.Parch),
    # Gondowan Settlement
    LocationName.Gondowan_Settlement_Star_Dust: Has(ItemName.Cyclone_Chip),
    # Magma Rock
    LocationName.Magma_Rock_Oil_Drop: Has(ItemName.Burst_Brooch),
    LocationName.Magma_Rock_383_coins: HasAll(ItemName.Burst_Brooch, ItemName.Growth),
    LocationName.Magma_Rock_Salamander_Tail: HasAll(ItemName.Burst_Brooch, ItemName.Growth, ItemName.Lash_Pebble),
    # Magma Rock Interior
    LocationName.Magma_Rock_Magma_Ball: And(
        Has(ItemName.Blaze), Has(ItemName.Whirlwind, options=NO_MAGMA_SHORTCUT, filtered_resolution=True)
    ),
    LocationName.Magma_Rock_Golem_Core: And(
        Has(ItemName.Whirlwind), Has(ItemName.Burst_Brooch, options=MAGMA_SHORTCUT, filtered_resolution=True)
    ),
    LocationName.Magma_Rock_Lucky_Medal: Has(ItemName.Burst_Brooch, options=MAGMA_SHORTCUT, filtered_resolution=True),
    LocationName.Magma_Rock_Mist_Potion: Has(ItemName.Burst_Brooch, options=MAGMA_SHORTCUT, filtered_resolution=True),
    LocationName.Magma_Rock_Salamander_Tail_Two: Or(
        Has(ItemName.Burst_Brooch, options=MAGMA_SHORTCUT),
        Has(ItemName.Whirlwind, options=NO_MAGMA_SHORTCUT),
    ),
    LocationName.Magma_Rock_Blaze: Has(ItemName.Whirlwind, options=NO_MAGMA_SHORTCUT, filtered_resolution=True),
    # Loho
    LocationName.Loho_Ship_Cannon: Has(ItemName.Magma_Ball),
    LocationName.Loho_Golem_Core: HasAll(ItemName.Ship_Cannon, ItemName.Scoop_Gem),
    LocationName.Loho_Golem_Core_Two: HasAll(ItemName.Ship_Cannon, ItemName.Scoop_Gem, ItemName.Lifting_Gem),
    LocationName.Lull: Has(ItemName.Ship_Cannon),
    # Angara Cavern
    LocationName.Angara_Cavern_Haures: Has(ItemName.Carry_Stone),
    # Kalt Island
    LocationName.Gel: Has(ItemName.Lash_Pebble),
    # Prox
    LocationName.Prox_Dark_Matter: HasAll(ItemName.Scoop_Gem, ItemName.Lifting_Gem),
    LocationName.Mold: Has(ItemName.Scoop_Gem),  # TODO: Only one djinn in Prox?
    # Mars Lighthouse
    LocationName.Mars_Lighthouse_Mimic: Has(ItemName.Pound_Cube),
    LocationName.Mars_Lighthouse_Teleport_Lapis: And(
        Has(ItemName.Pound_Cube),
        Has(ItemName.Burst_Brooch),
        Has(ItemName.Grindstone),
        HasAny(ItemName.Blaze, ItemName.Teleport_Lapis),
    ),
    LocationName.Balm: And(
        Has(ItemName.Pound_Cube),
        Has(ItemName.Burst_Brooch),
        Has(ItemName.Grindstone),
        HasAny(ItemName.Blaze, ItemName.Teleport_Lapis),
    ),
    LocationName.Mars_Lighthouse_Mars_Star: Has(ItemName.Flame_Dragons_defeated),
    LocationName.Mars_Lighthouse_Heated: HasAll(ItemName.Flame_Dragons_defeated, ItemName.Mars_Star),
    LocationName.Mars_Lighthouse_Orihalcon: HasAll(
        ItemName.Pound_Cube, ItemName.Burst_Brooch, ItemName.Blaze, ItemName.Grindstone
    ),
    LocationName.Mars_Lighthouse_Valkyrie_Mail: HasAll(
        ItemName.Pound_Cube,
        ItemName.Burst_Brooch,
        ItemName.Blaze,
        ItemName.Reveal,
        ItemName.Teleport_Lapis,
        ItemName.Grindstone,
    ),
    LocationName.Mars_Lighthouse_Sol_Blade: HasAll(
        ItemName.Pound_Cube,
        ItemName.Burst_Brooch,
        ItemName.Blaze,
        ItemName.Reveal,
        ItemName.Teleport_Lapis,
        ItemName.Grindstone,
    ),
    LocationName.Mars_Lighthouse_Flame_Dragons: And(
        HasGroup(ItemType.Character.name, 3),
        Has(ItemName.Teleport_Lapis),
        Has(ItemName.Pound_Cube),
        Has(ItemName.Burst_Brooch),
        Has(ItemName.Grindstone),
        Has(ItemName.Blaze),
        Has(ItemName.Reveal),
        has_djinn(48),
    ),
    # Mars Lighthouse activated
    LocationName.Fugue: Has(
        ItemName.Mars_Lighthouse_Heated,
        options=[OptionFilter(ShortcutMarsLighthouse, 0)],
        filtered_resolution=True,
    ),
    LocationName.Mars_Lighthouse_Psy_Crystal: HasAll(ItemName.Cyclone_Chip, ItemName.Hover_Jade, ItemName.Reveal),
    LocationName.Mars_Lighthouse_Doom_Dragon: And(
        HasGroup(ItemType.Character.name, 3),
        Has(ItemName.Cyclone_Chip),
        Has(ItemName.Hover_Jade),
        Has(ItemName.Frost_Jewel),
        Has(ItemName.Burst_Brooch),
        Has(ItemName.Blaze),
        Has(ItemName.Carry_Stone),
        Has(ItemName.Sand),
        Has(ItemName.Reveal),
        Has(ItemName.Teleport_Lapis),
        has_djinn(56),
    ),
}


def set_access_rules(world: GSTLAWorld):  # noqa: PLR0912, PLR0915
    game_data = load_game_data()
    player = world.player

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
