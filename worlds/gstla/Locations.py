from typing import Callable, List, Dict, NamedTuple, Optional
from enum import Enum
from BaseClasses import Location, MultiWorld
from .Names.LocationName import LocationName
from .Names.ItemName import ItemName

class LocationType(str, Enum):
   Item = "Item"
   Event = "Event"
   Djinn = "Djinn"
   Psyenergy = "Psyenergy"
   Hidden = "Hidden"
   Trade = "Trade"


def always_on(multiworld, player):
    return True

class LocationData(NamedTuple):
    id: Optional[int]
    name: str
    addresses: List[int]
    event_type: int
    vanilla_item: str
    loc_type: LocationType = LocationType.Item
    event: bool = False
    included: Callable[[MultiWorld, int], bool] = always_on


class GSTLALocation(Location):
    game: str = "Golden Sun The Lost Age"

base_djinn_index = 400

djinn_locations = [
    LocationData(base_djinn_index, LocationName.Flint, [16384000], 128, ItemName.Flint, LocationType.Djinn),
    LocationData(base_djinn_index + 1, LocationName.Granite, [16384002], 128, ItemName.Granite, LocationType.Djinn),
    LocationData(base_djinn_index + 2, LocationName.Quartz, [16384004], 128, ItemName.Quartz, LocationType.Djinn),
    LocationData(base_djinn_index + 3, LocationName.Vine, [16384006], 128, ItemName.Vine, LocationType.Djinn),
    LocationData(base_djinn_index + 4, LocationName.Sap, [16384008], 128, ItemName.Sap, LocationType.Djinn),
    LocationData(base_djinn_index + 5, LocationName.Ground, [16384010], 128, ItemName.Ground, LocationType.Djinn),
    LocationData(base_djinn_index + 6, LocationName.Bane, [16384012], 128, ItemName.Bane, LocationType.Djinn),
    LocationData(base_djinn_index + 7, LocationName.Echo, [16384014], 128, ItemName.Echo, LocationType.Djinn),
    LocationData(base_djinn_index + 8, LocationName.Iron, [16384016], 128, ItemName.Iron, LocationType.Djinn),
    LocationData(base_djinn_index + 9, LocationName.Steel, [16384018], 128, ItemName.Steel, LocationType.Djinn),
    LocationData(base_djinn_index + 10, LocationName.Mud, [16384020], 128, ItemName.Mud, LocationType.Djinn),
    LocationData(base_djinn_index + 11, LocationName.Flower, [16384022], 128, ItemName.Flower, LocationType.Djinn),
    LocationData(base_djinn_index + 12, LocationName.Meld, [16384024], 128, ItemName.Meld, LocationType.Djinn),
    LocationData(base_djinn_index + 13, LocationName.Petra, [16384026], 128, ItemName.Petra, LocationType.Djinn),
    LocationData(base_djinn_index + 14, LocationName.Salt, [16384028], 128,  ItemName.Salt, LocationType.Djinn),
    LocationData(base_djinn_index + 15, LocationName.Geode, [16384030], 128, ItemName.Geode, LocationType.Djinn),
    LocationData(base_djinn_index + 16, LocationName.Mold, [16384032], 128, ItemName.Mold, LocationType.Djinn),
    LocationData(base_djinn_index + 17, LocationName.Crystal, [16384034], 128, ItemName.Crystal, LocationType.Djinn),

    LocationData(base_djinn_index + 18, LocationName.Fizz, [16384036], 128, ItemName.Fizz, LocationType.Djinn),
    LocationData(base_djinn_index + 19, LocationName.Sleet, [16384038], 128, ItemName.Sleet, LocationType.Djinn),
    LocationData(base_djinn_index + 20, LocationName.Mist, [16384040], 128, ItemName.Mist, LocationType.Djinn),
    LocationData(base_djinn_index + 21, LocationName.Spritz, [16384042], 128, ItemName.Spritz, LocationType.Djinn),
    LocationData(base_djinn_index + 22, LocationName.Hail, [16384044], 128, ItemName.Hail, LocationType.Djinn),
    LocationData(base_djinn_index + 23, LocationName.Tonic, [16384046], 128, ItemName.Tonic, LocationType.Djinn),
    LocationData(base_djinn_index + 24, LocationName.Dew, [16384048], 128, ItemName.Dew, LocationType.Djinn),
    LocationData(base_djinn_index + 25, LocationName.Fog, [16384050], 128, ItemName.Fog, LocationType.Djinn),
    LocationData(base_djinn_index + 26, LocationName.Sour, [16384052], 128, ItemName.Sour, LocationType.Djinn),
    LocationData(base_djinn_index + 27, LocationName.Spring, [16384054], 128, ItemName.Spring, LocationType.Djinn),
    LocationData(base_djinn_index + 28, LocationName.Shade, [16384056], 128, ItemName.Shade, LocationType.Djinn),
    LocationData(base_djinn_index + 29, LocationName.Chill, [16384058], 128, ItemName.Chill, LocationType.Djinn),
    LocationData(base_djinn_index + 30, LocationName.Steam, [16384060], 128, ItemName.Steam, LocationType.Djinn),
    LocationData(base_djinn_index + 31, LocationName.Rime, [16384062,], 128, ItemName.Rime, LocationType.Djinn),
    LocationData(base_djinn_index + 32, LocationName.Gel, [16384064], 128, ItemName.Gel, LocationType.Djinn),
    LocationData(base_djinn_index + 33, LocationName.Eddy, [16384066], 128, ItemName.Eddy, LocationType.Djinn),
    LocationData(base_djinn_index + 34, LocationName.Balm, [16384068], 128, ItemName.Balm, LocationType.Djinn),
    LocationData(base_djinn_index + 35, LocationName.Serac, [16384070], 128, ItemName.Serac, LocationType.Djinn),

    LocationData(base_djinn_index + 36, LocationName.Forge, [16384072], 128, ItemName.Forge, LocationType.Djinn),
    LocationData(base_djinn_index + 37, LocationName.Fever, [16384074], 128, ItemName.Fever, LocationType.Djinn),
    LocationData(base_djinn_index + 38, LocationName.Corona, [16384076], 128, ItemName.Corona, LocationType.Djinn),
    LocationData(base_djinn_index + 39, LocationName.Scorch, [16384078], 128, ItemName.Scorch, LocationType.Djinn),
    LocationData(base_djinn_index + 40, LocationName.Ember, [16384080], 128, ItemName.Ember, LocationType.Djinn),
    LocationData(base_djinn_index + 41, LocationName.Flash, [16384082], 128, ItemName.Flash, LocationType.Djinn),
    LocationData(base_djinn_index + 42, LocationName.Torch, [16384084], 128, ItemName.Torch, LocationType.Djinn),
    LocationData(base_djinn_index + 43, LocationName.Cannon, [16384086], 128, ItemName.Cannon, LocationType.Djinn),
    LocationData(base_djinn_index + 44, LocationName.Spark, [16384088], 128, ItemName.Spark, LocationType.Djinn),
    LocationData(base_djinn_index + 45, LocationName.Kindle, [16384090], 128, ItemName.Kindle, LocationType.Djinn),
    LocationData(base_djinn_index + 46, LocationName.Char, [16384092], 128, ItemName.Char, LocationType.Djinn),
    LocationData(base_djinn_index + 47, LocationName.Coal, [16384094], 128, ItemName.Coal, LocationType.Djinn),
    LocationData(base_djinn_index + 48, LocationName.Reflux, [16384096], 128, ItemName.Reflux, LocationType.Djinn),
    LocationData(base_djinn_index + 49, LocationName.Core, [16384098], 128, ItemName.Core, LocationType.Djinn),
    LocationData(base_djinn_index + 50, LocationName.Tinder, [16384100], 128, ItemName.Tinder, LocationType.Djinn),
    LocationData(base_djinn_index + 51, LocationName.Shine, [16384102], 128, ItemName.Shine, LocationType.Djinn),
    LocationData(base_djinn_index + 52, LocationName.Fury, [16384104], 128, ItemName.Fury, LocationType.Djinn),
    LocationData(base_djinn_index + 53, LocationName.Fugue, [16384106], 128, ItemName.Fugue, LocationType.Djinn),

    LocationData(base_djinn_index + 54, LocationName.Gust, [16384108], 128, ItemName.Gust, LocationType.Djinn),
    LocationData(base_djinn_index + 55, LocationName.Breeze, [16384110], 128, ItemName.Breeze, LocationType.Djinn),
    LocationData(base_djinn_index + 56, LocationName.Zephyr, [16384112], 128, ItemName.Zephyr, LocationType.Djinn),
    LocationData(base_djinn_index + 57, LocationName.Smog, [16384114], 128, ItemName.Smog, LocationType.Djinn),
    LocationData(base_djinn_index + 58, LocationName.Kite, [16384116], 128, ItemName.Kite, LocationType.Djinn),
    LocationData(base_djinn_index + 59, LocationName.Squall, [16384118], 128, ItemName.Squall, LocationType.Djinn),
    LocationData(base_djinn_index + 60, LocationName.Luff, [16384120], 128, ItemName.Luff, LocationType.Djinn),
    LocationData(base_djinn_index + 61, LocationName.Breath, [16384122], 128, ItemName.Breath, LocationType.Djinn),
    LocationData(base_djinn_index + 62, LocationName.Blitz, [16384124], 128, ItemName.Blitz, LocationType.Djinn),
    LocationData(base_djinn_index + 63, LocationName.Ether, [16384126], 128, ItemName.Ether, LocationType.Djinn),
    LocationData(base_djinn_index + 64, LocationName.Waft, [16384128], 128, ItemName.Waft, LocationType.Djinn),
    LocationData(base_djinn_index + 65, LocationName.Haze, [16384130], 128, ItemName.Haze, LocationType.Djinn),
    LocationData(base_djinn_index + 66, LocationName.Wheeze, [16384132], 128, ItemName.Wheeze, LocationType.Djinn),
    LocationData(base_djinn_index + 67, LocationName.Aroma, [16384134], 128, ItemName.Aroma, LocationType.Djinn),
    LocationData(base_djinn_index + 68, LocationName.Whorl, [16384136], 128, ItemName.Whorl, LocationType.Djinn),
    LocationData(base_djinn_index + 69, LocationName.Gasp, [16384138], 128, ItemName.Gasp, LocationType.Djinn),
    LocationData(base_djinn_index + 70, LocationName.Lull, [16384140], 128, ItemName.Lull, LocationType.Djinn),
    LocationData(base_djinn_index + 71, LocationName.Gale, [16384142], 128, ItemName.Gale, LocationType.Djinn)
]

summon_index = 500

summon_tablets = [
    LocationData(summon_index + 1, LocationName.Madra_Catacombs_Moloch, [992068], 132, ItemName.Moloch),
    LocationData(summon_index + 2, LocationName.Yampi_Desert_Cave_Daedalus, [992212], 132, ItemName.Daedalus),
    LocationData(summon_index + 3, LocationName.Airs_Rock_Flora, [992632], 132, ItemName.Flora),
    LocationData(summon_index + 4, LocationName.Izumo_Ulysses, [993424], 132, ItemName.Ulysses),
    LocationData(summon_index + 5, LocationName.Treasure_Isle_Azul, [994300], 132, ItemName.Azul),
    LocationData(summon_index + 6, LocationName.Indra_Cavern_Zagan, [994844], 132, ItemName.Zagan),
    LocationData(summon_index + 7, LocationName.Osenia_Cavern_Megaera, [994856], 132, ItemName.Megaera),
    LocationData(summon_index + 8, LocationName.Angara_Cavern_Haures, [994868], 132, ItemName.Haures),
    LocationData(summon_index + 9, LocationName.Atteka_Cavern_Coatlicue, [994880], 132, ItemName.Coatlicue),
    LocationData(summon_index + 10, LocationName.Islet_Cave_Catastrophe, [994892], 132, ItemName.Catastrophe),
    LocationData(summon_index + 11, LocationName.Anemos_Inner_Sanctum_Charon, [994904], 132, ItemName.Charon),
    LocationData(summon_index + 12, LocationName.Anemos_Inner_Sanctum_Iris, [994916], 132, ItemName.Iris),
    LocationData(summon_index + 13, LocationName.Lemuria_Eclipse, [16384198], 132, ItemName.Eclipse)
]

psyenergy_index = 300

psyenergy_locations = [
    LocationData(psyenergy_index + 1, LocationName.Madra_Cyclone_Chip, [16384166, 991956], 128, ItemName.Cyclone_Chip),
    LocationData(psyenergy_index + 2, LocationName.Madra_Catacombs_Tremor_Bit, [992060], 128, ItemName.Tremor_Bit),
    LocationData(psyenergy_index + 3, LocationName.Tundaria_Tower_Burst_Brooch, [993828], 131, ItemName.Burst_Brooch),
    LocationData(psyenergy_index + 4, LocationName.Lemuria_Grindstone, [993916], 128, ItemName.Grindstone),
    LocationData(psyenergy_index + 5, LocationName.Mars_Lighthouse_Teleport_Lapis, [994636], 128, ItemName.Teleport_Lapis),
    LocationData(psyenergy_index + 6, LocationName.Kandorean_Temple_Lash_Pebble, [16384160], 128, ItemName.Lash_Pebble),
    LocationData(psyenergy_index + 7, LocationName.Dehkan_Plateau_Pound_Cube, [16384162], 128, ItemName.Pound_Cube),
    LocationData(psyenergy_index + 8, LocationName.Yampi_Desert_Scoop_Gem, [16384164], 128, ItemName.Scoop_Gem),
    LocationData(psyenergy_index + 9, LocationName.Shaman_Village_Hover_Jade, [16384168], 128, ItemName.Hover_Jade),
    LocationData(psyenergy_index + 10, LocationName.Airs_Rock_Reveal, [16384190], 132, ItemName.Reveal, LocationType.Psyenergy),
    LocationData(psyenergy_index + 11, LocationName.Aqua_Rock_Parch, [16384192], 132, ItemName.Parch, LocationType.Psyenergy),
    LocationData(psyenergy_index + 12, LocationName.Gaia_Rock_Sand, [16384194], 132, ItemName.Sand, LocationType.Psyenergy),
    LocationData(psyenergy_index + 13, LocationName.Magma_Rock_Blaze, [16384196], 132, ItemName.Blaze, LocationType.Psyenergy),
    LocationData(psyenergy_index + 14, LocationName.Idejima_Mind_Read, [16384204], 132, ItemName.Mind_Read, LocationType.Psyenergy),
    LocationData(psyenergy_index + 15, LocationName.Idejima_Whirlwind, [16384206], 132, ItemName.Whirlwind, LocationType.Psyenergy),
    LocationData(psyenergy_index + 16, LocationName.Idejima_Growth, [16384208], 132, ItemName.Growth, LocationType.Psyenergy),
    LocationData(psyenergy_index + 17, LocationName.Contigo_Carry_Stone, [16384210], 128, ItemName.Carry_Stone),
    LocationData(psyenergy_index + 18, LocationName.Contigo_Lifting_Gem, [16384212], 128, ItemName.Lifting_Gem),
    LocationData(psyenergy_index + 19, LocationName.Contigo_Orb_of_Force, [16384214], 128, ItemName.Orb_of_Force),
    LocationData(psyenergy_index + 20, LocationName.Contigo_Catch_Beads, [16384216], 128, ItemName.Catch_Beads),
    LocationData(psyenergy_index + 21, LocationName.Kibombo_Douse_Drop, [16384218], 128, ItemName.Douse_Drop),
    LocationData(psyenergy_index + 22, LocationName.Kibombo_Frost_Jewel, [16384220], 128, ItemName.Frost_Jewel)
]

test_locations = [
    LocationData(1, LocationName.Idejima_Shamans_Rod, [16384202], 128, ItemName.Shamans_Rod),

    LocationData(1, LocationName.Daila_Herb, [991776, 991796], 2, ItemName.Herb, LocationType.Hidden),
    LocationData(2, LocationName.Daila_Smoke_Bomb, [991784, 991804], 3, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(3, LocationName.Daila_Psy_Crystal, [991812], 131, ItemName.Psy_Crystal),
    LocationData(5, LocationName.Daila_Sleep_Bomb, [991832], 3, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(6, LocationName.Daila_3_coins, [991840], 2, ItemName.Herb, LocationType.Hidden),
    LocationData(7, LocationName.Daila_12_coins, [991848], 2, ItemName.Herb, LocationType.Hidden),
    LocationData(198, LocationName.Daila_Sea_Gods_Tear, [16384186], 128, ItemName.Sea_Gods_Tear),

    LocationData(169, LocationName.Kandorean_Temple_Mysterious_Card, [991860], 128, ItemName.Mysterious_Card),
    LocationData(214, LocationName.Kandorean_Temple_Mimic, [991872], 129, ItemName.Herb),

    LocationData(10, LocationName.Shrine_of_the_Sea_God_Rusty_Staff, [992968], 128, ItemName.Rusty_Staff_GlowerStaff),
    LocationData(11, LocationName.Shrine_of_the_Sea_God_Right_Prong, [992980], 131, ItemName.Right_Prong),

    LocationData(96, LocationName.Dehkan_Plateau_Elixir, [991892], 128, ItemName.Elixir),
    LocationData(97, LocationName.Dehkan_Plateau_Full_Metal_Vest, [991884], 128, ItemName.Full_Metal_Vest),
    LocationData(98, LocationName.Dehkan_Plateau_Themis_Axe, [991916], 128, ItemName.Themis_Axe),
    LocationData(216, LocationName.Dehkan_Plateau_Mint, [991904], 128, ItemName.Mint),
    LocationData(217, LocationName.Dehkan_Plateau_Nut, [991928], 128, ItemName.Nut),

    LocationData(8, LocationName.Madra_Antidote, [991948], 13, ItemName.Antidote, LocationType.Hidden),
    LocationData(10, LocationName.Madra_Smoke_Bomb, [991968], 3, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(11, LocationName.Madra_15_coins, [991976], 13, ItemName.Herb, LocationType.Hidden),
    LocationData(12, LocationName.Madra_Sleep_Bomb, [991984], 2, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(13, LocationName.Madra_Elixir, [991996], 2, ItemName.Elixir, LocationType.Hidden),
    LocationData(99, LocationName.Madra_Nurses_Cap, [991940], 128, ItemName.Nurses_Cap),

    LocationData(218, LocationName.Madra_Catacombs_Apple, [992008], 128, ItemName.Apple),
    LocationData(219, LocationName.Madra_Catacombs_Mist_Potion, [992016], 128, ItemName.Mist_Potion),
    LocationData(220, LocationName.Madra_Catacombs_Lucky_Medal, [992028], 128, ItemName.Lucky_Medal),
    LocationData(171, LocationName.Madra_Catacombs_Ruin_Key, [992036, 992048], 128, ItemName.Ruin_Key),

    LocationData(171, LocationName.Osenia_Cliffs_Pirates_Sword, [992080], 128, ItemName.Pirates_Sword),

    LocationData(100, LocationName.Yampi_Desert_Antidote, [992104], 128, ItemName.Antidote),
    LocationData(101, LocationName.Yampi_Desert_Guardian_Ring, [992092], 128, ItemName.Guardian_Ring),
    LocationData(102, LocationName.Yampi_Desert_Trainers_Whip, [992148], 128, ItemName.Trainers_Whip),
    LocationData(103, LocationName.Yampi_Desert_Lucky_Medal, [992140], 128, ItemName.Lucky_Medal),
    LocationData(104, LocationName.Yampi_Desert_315_coins, [992128], 131, ItemName.Herb),
    LocationData(105, LocationName.Yampi_Desert_Blow_Mace, [992180], 128, ItemName.Blow_Mace),
    LocationData(106, LocationName.Yampi_Desert_Hard_Nut, [992172], 128, ItemName.Hard_Nut),

    LocationData(106, LocationName.Yampi_Desert_Cave_Water_of_Life, [992192], 128, ItemName.Water_of_Life),
    LocationData(106, LocationName.Yampi_Desert_Cave_Orihalcon, [992232], 128, ItemName.Orihalcon),
    LocationData(106, LocationName.Yampi_Desert_Cave_Mythril_Silver, [992204], 131, ItemName.Mythril_Silver),
    LocationData(106, LocationName.Yampi_Desert_Cave_Dark_Matter, [992224], 128, ItemName.Dark_Matter),


    LocationData(106, LocationName.Alhafra_Psy_Crystal, [992244], 128, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Alhafra_Sleep_Bomb, [992252], 2, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Alhafra_Lucky_Medal, [992260], 2, ItemName.Lucky_Medal, LocationType.Hidden),
    LocationData(106, LocationName.Alhafra_32_coins, [992268], 13, ItemName.Herb, LocationType.Hidden),
    LocationData(106, LocationName.Alhafra_Smoke_Bomb, [992280], 2, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Alhafra_Elixir, [992304], 3, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Alhafra_Apple, [992312], 2, ItemName.Apple, LocationType.Hidden),

    LocationData(106, LocationName.Alhafran_Cave_123_coins, [992324], 128, ItemName.Herb),
    LocationData(106, LocationName.Alhafran_Cave_Ixion_Mail, [992332], 128, ItemName.Ixion_Mail),
    LocationData(106, LocationName.Alhafran_Cave_Lucky_Medal, [992340], 128, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Alhafran_Cave_Power_Bread, [992348], 2, ItemName.Power_Bread, LocationType.Hidden),
    LocationData(106, LocationName.Alhafran_Cave_777_coins, [992360], 128, ItemName.Herb),
    LocationData(106, LocationName.Alhafran_Cave_Potion, [992368], 128, ItemName.Potion),
    LocationData(106, LocationName.Alhafran_Cave_Psy_Crystal, [992376], 128, ItemName.Psy_Crystal),

    LocationData(106, LocationName.Mikasalla_Nut, [992396], 13, ItemName.Nut, LocationType.Hidden),
    LocationData(106, LocationName.Mikasalla_Herb, [992424], 2, ItemName.Herb, LocationType.Hidden),
    LocationData(106, LocationName.Mikasalla_Elixir, [992404], 3, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Mikasalla_82_coins, [992388], 128, ItemName.Herb),
    LocationData(106, LocationName.Mikasalla_Lucky_Pepper, [992416], 3, ItemName.Lucky_Pepper, LocationType.Hidden),

    LocationData(106, LocationName.Garoh_Nut, [992456], 3, ItemName.Nut, LocationType.Hidden),
    LocationData(106, LocationName.Garoh_Elixir, [992484], 2, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Garoh_Sleep_Bomb, [992476], 3, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Garoh_Smoke_Bomb, [992464], 3, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Garoh_Hypnos_Sword, [992444], 128, ItemName.Hypnos_Sword),

    LocationData(106, LocationName.Airs_Rock_Mimic, [992520], 129, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Airs_Rock_Cookie, [992504], 128, ItemName.Cookie),
    LocationData(106, LocationName.Airs_Rock_Elixir, [992608], 128, ItemName.Elixir),
    LocationData(106, LocationName.Airs_Rock_666_coins, [992644], 128, ItemName.Herb),
    LocationData(106, LocationName.Airs_Rock_Clarity_Circlet, [992584], 128, ItemName.Clarity_Circlet),
    LocationData(106, LocationName.Airs_Rock_Fujin_Shield, [992552], 128, ItemName.Fujin_Shield),
    LocationData(106, LocationName.Airs_Rock_Psy_Crystal, [992620], 128, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Airs_Rock_Sleep_Bomb, [992540], 128, ItemName.Sleep_Bomb),
    LocationData(106, LocationName.Airs_Rock_Smoke_Bomb, [992496], 128, ItemName.Smoke_Bomb),
    LocationData(106, LocationName.Airs_Rock_Storm_Brand, [992512], 128, ItemName.Storm_Brand),
    LocationData(106, LocationName.Airs_Rock_Vial, [992532], 128, ItemName.Vial), #Frost locked
    LocationData(106, LocationName.Airs_Rock_VialTwo, [992564], 128, ItemName.Vial),
    LocationData(106, LocationName.Airs_Rock_VialThree, [992596], 128, ItemName.Vial),


    LocationData(106, LocationName.Gondowan_Cliffs_Healing_Fungus, [992656], 131, ItemName.Healing_Fungus),
    LocationData(106, LocationName.Gondowan_Cliffs_Laughing_Fungus, [992664], 131, ItemName.Laughing_Fungus),
    LocationData(106, LocationName.Gondowan_Cliffs_Sleep_Bomb, [992672], 128, ItemName.Sleep_Bomb),

    LocationData(106, LocationName.Naribwe_Unicorn_Ring, [992692], 128, ItemName.Unicorn_Ring),
    LocationData(106, LocationName.Naribwe_Thorn_Crown, [992684], 128, ItemName.Thorn_Crown),
    LocationData(106, LocationName.Naribwe_Elixir, [992700], 2, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Naribwe_Sleep_Bomb, [992720], 2, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Naribwe_18_coins, [992712], 2, ItemName.Herb, LocationType.Hidden),

    LocationData(106, LocationName.Kibombo_Mountains_Tear_Stone, [992740], 128, ItemName.Tear_Stone),
    LocationData(106, LocationName.Kibombo_Mountains_Smoke_Bomb, [992764], 13, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Kibombo_Mountains_Power_Bread, [992732], 128, ItemName.Power_Bread),
    LocationData(106, LocationName.Kibombo_Mountains_Disk_Axe, [992752], 128, ItemName.Disk_Axe),

    LocationData(106, LocationName.Kibombo_Nut, [992832], 3, ItemName.Nut, LocationType.Hidden),
    LocationData(106, LocationName.Kibombo_Lucky_Pepper, [992800, 992812], 2, ItemName.Lucky_Pepper, LocationType.Hidden),
    LocationData(106, LocationName.Kibombo_Lucky_Medal, [992824], 2, ItemName.Lucky_Medal, LocationType.Hidden),


    LocationData(106, LocationName.Gabomba_Statue_Black_Crystal, [16384172], 128, ItemName.Black_Crystal),
    LocationData(106, LocationName.Gabomba_Statue_Mimic, [992852], 129, ItemName.Hard_Nut),
    LocationData(106, LocationName.Gabomba_Statue_Elixir, [992864], 128, ItemName.Elixir),
    LocationData(106, LocationName.Gabomba_Statue_Bone_Armlet, [992844], 128, ItemName.Bone_Armlet),

    LocationData(106, LocationName.Gabomba_Catacombs_Tomegathericon, [992888], 131, ItemName.Tomegathericon),
    LocationData(106, LocationName.Gabomba_Catacombs_Mint, [992876], 131, ItemName.Mint),

    LocationData(106, LocationName.Lemurian_Ship_Elixir, [992908], 3, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Lemurian_Ship_Potion, [992900], 128, ItemName.Potion),
    LocationData(106, LocationName.Lemurian_Ship_Oil_Drop, [992936], 3, ItemName.Oil_Drop, LocationType.Hidden),
    LocationData(106, LocationName.Lemurian_Ship_Antidote, [992916], 13, ItemName.Antidote, LocationType.Hidden),
    LocationData(106, LocationName.Lemurian_Ship_Mist_Potion, [992928], 128, ItemName.Mist_Potion),

    LocationData(106, LocationName.E_Tundaria_Islet_Pretty_Stone, [16384176], 128, ItemName.Pretty_Stone, LocationType.Trade),
    LocationData(106, LocationName.E_Tundaria_Islet_Lucky_Medal, [992432], 2, ItemName.Lucky_Medal, LocationType.Hidden),

    LocationData(106, LocationName.SE_Angara_Islet_Red_Cloth, [16384178], 128, ItemName.Red_Cloth, LocationType.Trade),
    LocationData(106, LocationName.SE_Angara_Islet_Lucky_Medal, [993016], 13, ItemName.Lucky_Medal, LocationType.Hidden),

    LocationData(106, LocationName.N_Osenia_Islet_Milk, [16384180], 128, ItemName.Milk, LocationType.Trade),
    LocationData(106, LocationName.N_Osenia_Islet_Lucky_Medal, [991824], 3, ItemName.Lucky_Medal, LocationType.Hidden),

    LocationData(106, LocationName.W_Indra_Islet_Lil_Turtle, [16384182], 128, ItemName.Lil_Turtle, LocationType.Trade),
    LocationData(106, LocationName.W_Indra_Islet_Lucky_Medal, [992992], 3, ItemName.Lucky_Medal, LocationType.Hidden),

    LocationData(106, LocationName.Sea_of_Time_Islet_Lucky_Medal, [993028], 3, ItemName.Lucky_Medal, LocationType.Hidden),


    LocationData(106, LocationName.Islet_Cave_Turtle_Boots, [993504], 128, ItemName.Turtle_Boots),
    LocationData(106, LocationName.Islet_Cave_Rusty_Staff, [993512], 128, ItemName.Rusty_Staff_Dracomace),


    LocationData(106, LocationName.Apojii_Islands_Herb, [993172], 131, ItemName.Herb),
    LocationData(106, LocationName.Apojii_Islands_Mint, [993164], 131, ItemName.Mint),
    LocationData(106, LocationName.Apojii_Islands_32_coins, [993192], 3, ItemName.Herb, LocationType.Hidden),
    LocationData(106, LocationName.Apojii_Islands_182_coins, [993180], 2, ItemName.Herb, LocationType.Hidden),
    LocationData(106, LocationName.Apojii_Islands_Bramble_Seed, [993204], 131, ItemName.Bramble_Seed),

    LocationData(106, LocationName.Aqua_Rock_Nut, [993216], 128, ItemName.Nut),
    LocationData(106, LocationName.Aqua_Rock_Vial, [993332], 128, ItemName.Vial),
    LocationData(106, LocationName.Aqua_Rock_Mimic, [993268], 129, ItemName.Potion),
    LocationData(106, LocationName.Aqua_Rock_Elixir, [993224], 128, ItemName.Elixir),
    LocationData(106, LocationName.Aqua_Rock_Aquarius_Stone, [993280], 128, ItemName.Aquarius_Stone),
    LocationData(106, LocationName.Aqua_Rock_Crystal_Powder, [993312], 128, ItemName.Crystal_Powder),
    LocationData(106, LocationName.Aqua_Rock_Lucky_Pepper, [993288], 128, ItemName.Lucky_Pepper),
    LocationData(106, LocationName.Aqua_Rock_Mist_Sabre, [993236], 128, ItemName.Mist_Sabre),
    LocationData(106, LocationName.Aqua_Rock_Oil_Drop, [993244], 128, ItemName.Oil_Drop),
    LocationData(106, LocationName.Aqua_Rock_Rusty_Sword, [993300], 128, ItemName.Rusty_Sword_RobbersBlade),
    LocationData(106, LocationName.Aqua_Rock_Tear_Stone, [993344], 128, ItemName.Tear_Stone),
    LocationData(106, LocationName.Aqua_Rock_Water_of_Life, [993256], 128, ItemName.Water_of_Life),

    LocationData(106, LocationName.Izumo_Elixir, [993384], 2, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Izumo_Antidote, [993360], 131, ItemName.Antidote),
    LocationData(106, LocationName.Izumo_Antidote_Two, [993368], 131, ItemName.Antidote),
    LocationData(106, LocationName.Izumo_Lucky_Medal, [993376], 131, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Izumo_Smoke_Bomb, [993404], 2, ItemName.Smoke_Bomb),
    LocationData(106, LocationName.Izumo_Festival_Coat, [993412], 13, ItemName.Festival_Coat, LocationType.Hidden),
    LocationData(106, LocationName.Izumo_Phantasmal_Mail, [993432], 128, ItemName.Phantasmal_Mail),
    LocationData(106, LocationName.Izumo_Water_of_Life, [993392], 2, ItemName.Water_of_Life, LocationType.Hidden),

    LocationData(106, LocationName.Gaia_Rock_Nut, [993444], 128, ItemName.Nut),
    LocationData(106, LocationName.Gaia_Rock_Apple, [993464], 128, ItemName.Apple),
    LocationData(106, LocationName.Gaia_Rock_Mimic, [993476], 129, ItemName.Potion),
    LocationData(106, LocationName.Gaia_Rock_Rusty_Mace, [993484], 128, ItemName.Rusty_Mace_DemonMace),
    LocationData(106, LocationName.Gaia_Rock_Cloud_Brand, [993492], 131, ItemName.Cloud_Brand),
    LocationData(106, LocationName.Gaia_Rock_Dancing_Idol, [993456], 131, ItemName.Dancing_Idol),

    LocationData(106, LocationName.Treasure_Isle_161_coins, [994108], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Iris_Robe, [994288], 128, ItemName.Iris_Robe),
    LocationData(106, LocationName.Treasure_Isle_911_coins, [994208], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Cookie, [994224], 128, ItemName.Cookie),
    LocationData(106, LocationName.Treasure_Isle_Fire_Brand, [994280], 128, ItemName.Fire_Brand),
    LocationData(106, LocationName.Treasure_Isle_Jesters_Armlet, [994260], 128, ItemName.Jesters_Armlet),
    LocationData(106, LocationName.Treasure_Isle_Lucky_Medal, [994116], 128, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Treasure_Isle_Mimic, [994268], 129, ItemName.Power_Bread),
    LocationData(106, LocationName.Treasure_Isle_Psy_Crystal, [994216], 128, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Treasure_Isle_Rusty_Axe, [994240], 128, ItemName.Rusty_Axe_VikingAxe),
    LocationData(106, LocationName.Treasure_Isle_Star_Dust, [994248], 128, ItemName.Star_Dust),
    LocationData(106, LocationName.Treasure_Isle_Sylph_Feather, [994232], 128, ItemName.Sylph_Feather),
    LocationData(106, LocationName.Treasure_Isle_Empty, [994124], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Two, [994132], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Three, [994140], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Four, [994148], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Five, [994160], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Six, [994168], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Seven, [994176], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Eight, [994184], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Nine, [994192], 128, ItemName.Herb),
    LocationData(106, LocationName.Treasure_Isle_Empty_Ten, [994200], 128, ItemName.Herb),

    LocationData(106, LocationName.Tundaria_Tower_Center_Prong, [16384200], 128, ItemName.Center_Prong),
    LocationData(106, LocationName.Tundaria_Tower_Mint, [993796], 128, ItemName.Mint),
    LocationData(106, LocationName.Tundaria_Tower_Vial, [993760], 128, ItemName.Vial),
    LocationData(106, LocationName.Tundaria_Tower_365_coins, [993788], 128, ItemName.Herb),
    LocationData(106, LocationName.Tundaria_Tower_Hard_Nut, [993808], 128, ItemName.Hard_Nut),
    LocationData(106, LocationName.Tundaria_Tower_Crystal_Powder, [993816], 128, ItemName.Crystal_Powder),
    LocationData(106, LocationName.Tundaria_Tower_Lightning_Sword, [993768], 128, ItemName.Lightning_Sword),
    LocationData(106, LocationName.Tundaria_Tower_Lucky_Medal, [993752], 128, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Tundaria_Tower_Sylph_Feather, [993744], 128, ItemName.Sylph_Feather),

    LocationData(106, LocationName.Ankohl_Ruins_Nut, [993640], 128, ItemName.Nut),
    LocationData(106, LocationName.Ankohl_Ruins_Vial, [993708], 128, ItemName.Vial),
    LocationData(106, LocationName.Ankohl_Ruins_Potion, [993720], 128, ItemName.Potion),
    LocationData(106, LocationName.Ankohl_Ruins_210_coins, [993632], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_365_coins, [993692], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Crystal_Powder, [993652], 128, ItemName.Crystal_Powder),
    LocationData(106, LocationName.Ankohl_Ruins_Left_Prong, [993732], 131, ItemName.Left_Prong),
    LocationData(106, LocationName.Ankohl_Ruins_Muni_Robe, [993680], 128, ItemName.Muni_Robe),
    LocationData(106, LocationName.Ankohl_Ruins_Power_Bread, [993672], 128, ItemName.Power_Bread),
    LocationData(106, LocationName.Ankohl_Ruins_Sylph_Feather, [993700], 128, ItemName.Sylph_Feather),
    LocationData(106, LocationName.Ankohl_Ruins_Thanatos_Mace, [993664], 128, ItemName.Thanatos_Mace),
    LocationData(106, LocationName.Ankohl_Ruins_Empty, [993584], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Empty_Two, [993592], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Empty_Three, [993600], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Empty_Four, [993608], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Empty_Five, [993616], 128, ItemName.Herb),
    LocationData(106, LocationName.Ankohl_Ruins_Empty_Six, [993624], 128, ItemName.Herb),

    LocationData(106, LocationName.Champa_Elixir, [993560], 13, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Champa_Trident, [16384174], 128, ItemName.Trident),
    LocationData(106, LocationName.Champa_12_coins, [993540], 13, ItemName.Herb, LocationType.Hidden),
    LocationData(106, LocationName.Champa_Sleep_Bomb, [993572], 3, ItemName.Sleep_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Champa_Smoke_Bomb, [993532], 13, ItemName.Smoke_Bomb, LocationType.Hidden),
    LocationData(106, LocationName.Champa_Lucky_Medal, [993548], 2, ItemName.Lucky_Medal, LocationType.Hidden),
    LocationData(106, LocationName.Champa_Viking_Helm, [993524], 128, ItemName.Viking_Helm),

    LocationData(106, LocationName.Yallam_Nut, [993040], 131, ItemName.Nut),
    LocationData(106, LocationName.Yallam_Elixir, [993076], 13, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Yallam_Antidote, [993056], 131, ItemName.Antidote),
    LocationData(106, LocationName.Yallam_Masamune, [993064], 128, ItemName.Masamune),
    LocationData(106, LocationName.Yallam_Oil_Drop, [993084], 3, ItemName.Oil_Drop, LocationType.Hidden),
    LocationData(106, LocationName.Yallam_16_coins, [993048], 2, ItemName.Herb, LocationType.Hidden),

    LocationData(106, LocationName.Taopo_Swamp_Vial, [993128], 128, ItemName.Vial),
    LocationData(106, LocationName.Taopo_Swamp_Cookie, [993096], 128, ItemName.Cookie),
    LocationData(106, LocationName.Taopo_Swamp_Star_Dust, [993140], 131, ItemName.Star_Dust),
    LocationData(106, LocationName.Taopo_Swamp_Bramble_Seed, [993152], 131, ItemName.Bramble_Seed),
    LocationData(106, LocationName.Taopo_Swamp_Tear_Stone, [993108], 131, ItemName.Tear_Stone),
    LocationData(106, LocationName.Taopo_Swamp_Tear_Stone_Two, [993116], 131, ItemName.Tear_Stone),


    LocationData(106, LocationName.Lemuria_Bone, [993888], 131, ItemName.Bone),
    LocationData(106, LocationName.Lemuria_Hard_Nut, [993880], 131, ItemName.Hard_Nut),
    LocationData(106, LocationName.Lemuria_Star_Dust, [993896], 131, ItemName.Star_Dust),
    LocationData(106, LocationName.Lemuria_Lucky_Medal, [993864], 131, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Lemuria_Lucky_Medal_Two, [993924], 3, ItemName.Lucky_Medal, LocationType.Hidden),
    LocationData(106, LocationName.Lemuria_Rusty_Sword, [993872], 131, ItemName.Rusty_Sword_CorsairsEdge),

    LocationData(106, LocationName.SW_Atteka_Islet_Dragon_Skin, [993984], 128, ItemName.Dragon_Skin),

    LocationData(106, LocationName.Hesperia_Settlement_166_coins, [993960], 128, ItemName.Herb),

    LocationData(106, LocationName.Shaman_Village_Elixir, [994072], 2, ItemName.Elixir, LocationType.Hidden),
    LocationData(106, LocationName.Shaman_Village_Spirit_Gloves, [994044], 128, ItemName.Spirit_Gloves),
    LocationData(106, LocationName.Shaman_Village_Hard_Nut, [994096], 128, ItemName.Hard_Nut),
    LocationData(106, LocationName.Shaman_Village_Lucky_Medal, [994052], 2, ItemName.Lucky_Medal, LocationType.Hidden),
    LocationData(106, LocationName.Shaman_Village_Lucky_Pepper, [994084], 128, ItemName.Lucky_Pepper, LocationType.Hidden),
    LocationData(106, LocationName.Shaman_Village_Weasels_Claw, [994064], 3, ItemName.Weasels_Claw),

    LocationData(106, LocationName.Atteka_Inlet_Vial, [993996], 128, ItemName.Vial),

    LocationData(106, LocationName.Contigo_Corn, [994024], 131, ItemName.Corn),
    LocationData(106, LocationName.Contigo_Bramble_Seed, [994032], 131, ItemName.Bramble_Seed),
    LocationData(106, LocationName.Contigo_Dragon_Skin, [994716], 128, ItemName.Dragon_Skin),
    LocationData(106, LocationName.Contigo_Power_Bread, [994016], 3, ItemName.Power_Bread, LocationType.Hidden),

    LocationData(106, LocationName.Jupiter_Lighthouse_Mint, [994312], 131, ItemName.Mint),
    LocationData(106, LocationName.Jupiter_Lighthouse_Blue_Key, [994396], 131, ItemName.Blue_Key),
    LocationData(106, LocationName.Jupiter_Lighthouse_Erinyes_Tunic, [994336], 128, ItemName.Erinyes_Tunic),
    LocationData(106, LocationName.Jupiter_Lighthouse_Meditation_Rod, [994368], 128, ItemName.Meditation_Rod),
    LocationData(106, LocationName.Jupiter_Lighthouse_Phaetons_Blade, [994436], 128, ItemName.Phaetons_Blade),
    LocationData(106, LocationName.Jupiter_Lighthouse_306_coins, [994412], 128, ItemName.Herb),
    LocationData(106, LocationName.Jupiter_Lighthouse_Mimic, [994388], 129, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Jupiter_Lighthouse_Mist_Potion, [994404], 128, ItemName.Mist_Potion),
    LocationData(106, LocationName.Jupiter_Lighthouse_Potion, [994348], 128, ItemName.Potion),
    LocationData(106, LocationName.Jupiter_Lighthouse_Psy_Crystal, [994356], 128, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Jupiter_Lighthouse_Red_Key, [994376], 131, ItemName.Red_Key),
    LocationData(106, LocationName.Jupiter_Lighthouse_Water_of_Life, [994424], 128, ItemName.Water_of_Life),

    LocationData(106, LocationName.Anemos_Inner_Sanctum_Orihalcon, [994736], 128, ItemName.Orihalcon),
    LocationData(106, LocationName.Anemos_Inner_Sanctum_Dark_Matter, [994728], 128, ItemName.Dark_Matter),

    LocationData(106, LocationName.Gondowan_Settlement_Lucky_Medal, [993948], 8, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Gondowan_Settlement_Star_Dust, [993936], 128, ItemName.Star_Dust),

    LocationData(106, LocationName.Magma_Rock_Golem_Core, [994524], 128, ItemName.Golem_Core),
    LocationData(106, LocationName.Magma_Rock_Magma_Ball, [16384188], 128, ItemName.Magma_Ball),
    LocationData(106, LocationName.Magma_Rock_Mimic, [994536], 129, ItemName.Apple),
    LocationData(106, LocationName.Magma_Rock_Salamander_Tail, [994468], 128, ItemName.Salamander_Tail),
    LocationData(106, LocationName.Magma_Rock_Salamander_Tail_Two, [994504], 128, ItemName.Salamander_Tail),
    LocationData(106, LocationName.Magma_Rock_383_coins, [994460], 128, ItemName.Herb),
    LocationData(106, LocationName.Magma_Rock_Lucky_Medal, [994480], 128, ItemName.Lucky_Medal),
    LocationData(106, LocationName.Magma_Rock_Mist_Potion, [994492], 128, ItemName.Mist_Potion),
    LocationData(106, LocationName.Magma_Rock_Oil_Drop, [994448], 128, ItemName.Oil_Drop),

    LocationData(106, LocationName.Loho_Crystal_Powder, [994572], 3, ItemName.Crystal_Powder, LocationType.Hidden),
    LocationData(106, LocationName.Loho_Mythril_Silver, [994548], 131, ItemName.Mythril_Silver),
    LocationData(106, LocationName.Loho_Golem_Core, [994556], 131, ItemName.Golem_Core),
    LocationData(106, LocationName.Loho_Golem_Core_Two, [994564], 131, ItemName.Golem_Core),


    LocationData(106, LocationName.Prox_Cookie, [994592], 2, ItemName.Cookie, LocationType.Hidden),
    LocationData(106, LocationName.Prox_Potion, [994604], 2, ItemName.Potion, LocationType.Hidden),
    LocationData(106, LocationName.Prox_Dark_Matter, [994584], 131, ItemName.Dark_Matter),
    LocationData(106, LocationName.Prox_Sacred_Feather, [994612], 13, ItemName.Sacred_Feather, LocationType.Hidden),

    LocationData(106, LocationName.Mars_Lighthouse_Alastors_Hood, [994656], 128, ItemName.Alastors_Hood),
    LocationData(106, LocationName.Mars_Lighthouse_Mars_Star, [16384170], 128, ItemName.Mars_Star),
    LocationData(106, LocationName.Mars_Lighthouse_Sol_Blade, [994692], 128, ItemName.Sol_Blade),
    LocationData(106, LocationName.Mars_Lighthouse_Apple, [994624], 128, ItemName.Apple),
    LocationData(106, LocationName.Mars_Lighthouse_Mimic, [994644], 129, ItemName.Cookie),
    LocationData(106, LocationName.Mars_Lighthouse_Orihalcon, [994668], 128, ItemName.Orihalcon),
    LocationData(106, LocationName.Mars_Lighthouse_Psy_Crystal, [994704], 128, ItemName.Psy_Crystal),
    LocationData(106, LocationName.Mars_Lighthouse_Valkyrie_Mail, [994680], 128, ItemName.Valkyrie_Mail),

    LocationData(106, LocationName.WesternSea_RustySword, [994944], 133, ItemName.Rusty_Sword_PiratesSabre),
    LocationData(106, LocationName.WesternSea_RustySword_Two, [994960], 133, ItemName.Rusty_Sword_SoulBrand),
    LocationData(106, LocationName.EasternSea_RustyAxe, [994928], 133, ItemName.Rusty_Axe_CaptainsAxe),
    LocationData(106, LocationName.EasternSea_RustyMace, [994936], 133, ItemName.Rusty_Mace_HagboneMace),
    LocationData(106, LocationName.WesternSea_RustyStaff, [994952], 133, ItemName.Rusty_Staff_GoblinsRod)

]

events = [
    LocationData(None, LocationName.Mars_Lighthouse_Doom_Dragon, [0], 0, ItemName.Victory, LocationType.Event, True),
    LocationData(None, LocationName.Alhafra_Briggs, [0], 0, ItemName.Briggs_defeated, LocationType.Event, True),
    LocationData(None, LocationName.Alhafra_Prison_Briggs, [0], 0, ItemName.Briggs_escaped, LocationType.Event, True),
    LocationData(None, LocationName.Gabombo_Statue, [0], 0, ItemName.Gabombo_Statue_Completed, LocationType.Event, True),
    LocationData(None, LocationName.Gaia_Rock_Serpent, [0], 0, ItemName.Serpent_defeated, LocationType.Event, True),
    LocationData(None, LocationName.SeaOfTime_Poseidon, [0], 0, ItemName.Poseidon_defeated, LocationType.Event,True),
    LocationData(None, LocationName.Lemurian_Ship_Aqua_Hydra, [0], 0, ItemName.Aqua_Hydra_defeated, LocationType.Event, True),
    LocationData(None, LocationName.Shaman_Village_Moapa, [0], 0, ItemName.Moapa_defeated, LocationType.Event, True),
    LocationData(None, LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst, [0], 0, ItemName.Jupiter_Beacon_Lit, LocationType.Event, True),
    LocationData(None, LocationName.Mars_Lighthouse_Flame_Dragons, [0], 0, ItemName.Flamedragons_defeated, LocationType.Event, True),
    LocationData(None, LocationName.Lemurian_Ship_Engine, [0], 0, ItemName.Ship, LocationType.Event, True)
]

def create_loctype_to_datamapping():
    types: Dict[str, List[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types


all_locations: List[LocationData] = test_locations + djinn_locations + psyenergy_locations + summon_tablets + events
location_name_to_id: Dict[str, LocationData] = {location.name: location for location in all_locations if location.loc_type != LocationType.Event}
location_type_to_data: Dict[str, List[LocationData]] = create_loctype_to_datamapping()