from typing import Callable, List, Dict, NamedTuple
from enum import Enum
from BaseClasses import Location, CollectionState
from .Names.LocationName import LocationName

class LocationType(str, Enum):
   Item = "Item"
   Event = "Event"
   Djinn = "Djinn"
   Psyenergy = "Psyenergy"


class LocationData(NamedTuple):
    id: int
    name: str
    addresses: List[int]
    event_type: int
    loc_type: LocationType = LocationType.Item

class GSTLALocation(Location):
    game: str = "Golden Sun The Lost Age"

hidden_items = [
    LocationData(1, LocationName.Daila_Herb, [991776,991796], 2),
    LocationData(2, LocationName.Daila_Smoke_Bomb, [991784,991804], 3),
    LocationData(3, LocationName.Daila_Psy_Crystal, [991812], 131),
    LocationData(4, LocationName.N_Osenia_Islet_Lucky_Medal, [991824], 3),
    LocationData(5, LocationName.Daila_Sleep_Bomb, [991832], 3),
    LocationData(6, LocationName.Daila_3_coins, [991840], 2),
    LocationData(7, LocationName.Daila_12_coins, [991848], 2),
    LocationData(8, LocationName.Madra_Antidote, [991948], 13),
    LocationData(9, LocationName.Madra_Cyclone_Chip, [16384166,991956], 128),
    LocationData(10, LocationName.Madra_Smoke_Bomb, [991968], 3),
    LocationData(11, LocationName.Madra_15_coins, [991976], 13),
    LocationData(12, LocationName.Madra_Sleep_Bomb, [991984], 2),
    LocationData(13, LocationName.Madra_Elixir, [991996], 2),
    LocationData(14, LocationName.Yampi_Desert_315_coins, [992128], 131),
    LocationData(15, LocationName.Alhafra_Sleep_Bomb, [992252], 2),
    LocationData(16, LocationName.Alhafra_Lucky_Medal, [992260], 2),
    LocationData(17, LocationName.Alhafra_32_coins, [992268], 13),
    LocationData(18, LocationName.Alhafra_Smoke_Bomb, [992280], 2),
    LocationData(19, LocationName.Alhafra_Elixir, [992304], 3),
    LocationData(20, LocationName.Alhafra_Apple, [992312], 2),
    LocationData(21, LocationName.Alhafran_Cave_Power_Bread, [992348], 2),
    LocationData(22, LocationName.Mikasalla_Nut, [992396], 13),
    LocationData(23, LocationName.Mikasalla_Elixir, [992404], 3),
    LocationData(24, LocationName.Mikasalla_Lucky_Pepper, [992416], 3),
    LocationData(25, LocationName.Mikasalla_Herb, [992424], 2),
    LocationData(26, LocationName.E_Tundaria_Islet_Lucky_Medal, [992432], 2),
    LocationData(27, LocationName.Garoh_Nut, [992456], 3),
    LocationData(28, LocationName.Garoh_Smoke_Bomb, [992464], 3),
    LocationData(29, LocationName.Garoh_Sleep_Bomb, [992476], 2),
    LocationData(30, LocationName.Garoh_Elixir, [992484], 2),
    LocationData(31, LocationName.Naribwe_Elixir, [992700], 2),
    LocationData(32, LocationName.Naribwe_18_coins, [992712], 2),
    LocationData(33, LocationName.Naribwe_Sleep_Bomb, [992720], 2),
    LocationData(34, LocationName.Kibombo_Mountains_Smoke_Bomb, [992764], 13),
    LocationData(35, LocationName.Kibombo_Lucky_Pepper, [992800,992812], 2),
    LocationData(36, LocationName.Kibombo_Lucky_Medal, [992824], 2),
    LocationData(37, LocationName.Kibombo_Nut, [992832], 3),
    LocationData(38, LocationName.Gabomba_Catacombs_Mint, [992876], 131),
    LocationData(39, LocationName.Lemurian_Ship_Elixir, [992908], 3),
    LocationData(40, LocationName.Lemurian_Ship_Antidote, [992916], 13),
    LocationData(41, LocationName.Lemurian_Ship_Oil_Drop, [992936,992944], 3),
    LocationData(42, LocationName.W_Indra_Islet_Lucky_Medal, [992992], 3),
    LocationData(43, LocationName.SE_Angara_Islet_Lucky_Medal, [993016], 13),
    LocationData(44, LocationName.Sea_of_Time_Islet_Lucky_Medal, [993028], 3),
    LocationData(45, LocationName.Yallam_Nut, [993040], 131),
    LocationData(46, LocationName.Yallam_16_coins, [993048], 2),
    LocationData(47, LocationName.Yallam_Antidote, [993056], 131),
    LocationData(48, LocationName.Yallam_Elixir, [993076], 13),
    LocationData(49, LocationName.Yallam_Oil_Drop, [993084], 3),
    LocationData(50, LocationName.Taopo_Swamp_Bramble_Seed, [993152], 131),
    LocationData(51, LocationName.Apojii_Islands_Mint, [993164], 131),
    LocationData(52, LocationName.Apojii_Islands_Herb, [993172], 131),
    LocationData(53, LocationName.Apojii_Islands_182_coins, [993180], 2),
    LocationData(54, LocationName.Apojii_Islands_32_coins, [993192], 3),
    LocationData(55, LocationName.Apojii_Islands_Bramble_Seed, [993204], 131),
    LocationData(56, LocationName.Izumo_Antidote, [993360], 131),
    LocationData(57, LocationName.Izumo_Antidote, [993368], 131),
    LocationData(58, LocationName.Izumo_Lucky_Medal, [993376], 131),
    LocationData(59, LocationName.Izumo_Elixir, [993384], 2),
    LocationData(60, LocationName.Izumo_Water_of_Life, [993392], 2),
    LocationData(61, LocationName.Izumo_Smoke_Bomb, [993404], 2),
    LocationData(62, LocationName.Champa_Smoke_Bomb, [993532], 13),
    LocationData(63, LocationName.Champa_12_coins, [993540], 13),
    LocationData(64, LocationName.Champa_Lucky_Medal, [993548], 2),
    LocationData(65, LocationName.Champa_Elixir, [993560], 13),
    LocationData(66, LocationName.Champa_Sleep_Bomb, [993572], 3),
    LocationData(67, LocationName.Tundaria_Tower_Center_Prong, [16384200,993776], 128),
    LocationData(68, LocationName.Lemuria_Lucky_Medal, [993864], 131),
    LocationData(69, LocationName.Lemuria_Hard_Nut, [993880], 131),
    LocationData(70, LocationName.Lemuria_Bone, [993888], 131),
    LocationData(71, LocationName.Lemuria_Lucky_Medal, [993924], 3),
    LocationData(72, LocationName.Gondowan_Settlement_Lucky_Medal, [993948], 8),
    LocationData(73, LocationName.Contigo_Power_Bread, [994016], 3),
    LocationData(74, LocationName.Contigo_Bramble_Seed, [994032], 131),
    LocationData(75, LocationName.Shaman_Village_Lucky_Medal, [994052], 2),
    LocationData(76, LocationName.Shaman_Village_Weasels_Claw, [994064], 3),
    LocationData(77, LocationName.Shaman_Village_Elixir, [994072], 2),
    LocationData(78, LocationName.Shaman_Village_Lucky_Pepper, [994084], 2),
    LocationData(79, LocationName.Jupiter_Lighthouse_Mint, [994312], 131),
    LocationData(80, LocationName.Loho_Crystal_Powder, [994572], 3),
    LocationData(81, LocationName.Prox_Cookie, [994592], 2),
    LocationData(82, LocationName.Prox_Potion, [994604], 2),
    LocationData(83, LocationName.Prox_Sacred_Feather, [994612], 13)
]
major_items = [
    LocationData(97, LocationName.Dehkan_Plateau_Full_Metal_Vest, [991884], 128),
    LocationData(98, LocationName.Dehkan_Plateau_Themis_Axe, [991916], 128),
    LocationData(99, LocationName.Madra_Nurses_Cap, [991940], 128),
    LocationData(100, LocationName.Osenia_Cliffs_Pirates_Sword, [992080], 128),
    LocationData(101, LocationName.Yampi_Desert_Guardian_Ring, [992092], 128),
    LocationData(102, LocationName.Yampi_Desert_Blow_Mace, [992180], 128),
    LocationData(103, LocationName.Yampi_Desert_Cave_Mythril_Silver, [992204], 131),
    LocationData(104, LocationName.Yampi_Desert_Cave_Dark_Matter, [992224], 128),
    LocationData(105, LocationName.Yampi_Desert_Cave_Orihalcon, [992232], 128),
    LocationData(106, LocationName.Alhafran_Cave_Ixion_Mail, [992332], 128),
    LocationData(107, LocationName.Garoh_Hypnos_Sword, [992444], 128),
    LocationData(108, LocationName.Airs_Rock_Storm_Brand, [992512], 128),
    LocationData(109, LocationName.Airs_Rock_Fujin_Shield, [992552], 128),
    LocationData(110, LocationName.Airs_Rock_Clarity_Circlet, [992584], 128),
    LocationData(111, LocationName.Naribwe_Thorn_Crown, [992684], 128),
    LocationData(112, LocationName.Naribwe_Unicorn_Ring, [992692], 128),
    LocationData(113, LocationName.Kibombo_Mountains_Tear_Stone, [992740], 128),
    LocationData(114, LocationName.Kibombo_Mountains_Disk_Axe, [992752], 128),
    LocationData(115, LocationName.Gabomba_Statue_Bone_Armlet, [992844], 128),
    LocationData(116, LocationName.Shrine_of_the_Sea_God_Rusty_Staff, [992968], 128),
    LocationData(117, LocationName.Yallam_Masamune, [993064], 128),
    LocationData(118, LocationName.Taopo_Swamp_Tear_Stone, [993108], 131),
    LocationData(119, LocationName.Taopo_Swamp_Tear_Stone, [993116], 131),
    LocationData(120, LocationName.Taopo_Swamp_Star_Dust, [993140], 131),
    LocationData(121, LocationName.Aqua_Rock_Mist_Sabre, [993236], 128),
    LocationData(122, LocationName.Aqua_Rock_Rusty_Sword, [993300], 128),
    LocationData(123, LocationName.Aqua_Rock_Tear_Stone, [993344], 128),
    LocationData(124, LocationName.Izumo_Festival_Coat, [993412], 13),
    LocationData(125, LocationName.Izumo_Phantasmal_Mail, [993432], 128),
    LocationData(126, LocationName.Gaia_Rock_Rusty_Mace, [993484], 128),
    LocationData(127, LocationName.Gaia_Rock_Cloud_Brand, [993492], 131),
    LocationData(128, LocationName.Islet_Cave_Turtle_Boots, [993504], 128),
    LocationData(129, LocationName.Islet_Cave_Rusty_Staff, [993512], 128),
    LocationData(130, LocationName.Champa_Viking_Helm, [993524], 128),
    LocationData(131, LocationName.Ankohl_Ruins_Thanatos_Mace, [993664], 128),
    LocationData(132, LocationName.Ankohl_Ruins_Muni_Robe, [993680], 128),
    LocationData(133, LocationName.Ankohl_Ruins_Sylph_Feather, [993700], 128),
    LocationData(134, LocationName.Tundaria_Tower_Sylph_Feather, [993744], 128),
    LocationData(135, LocationName.Tundaria_Tower_Lightning_Sword, [993768], 128),
    LocationData(136, LocationName.Lemuria_Rusty_Sword, [993872], 131),
    LocationData(137, LocationName.Lemuria_Star_Dust, [993896], 131),
    LocationData(138, LocationName.Gondowan_Settlement_Star_Dust, [993936], 128),
    LocationData(139, LocationName.SW_Atteka_Islet_Dragon_Skin, [993984], 128),
    LocationData(140, LocationName.Shaman_Village_Spirit_Gloves, [994044], 128),
    LocationData(141, LocationName.Treasure_Isle_Sylph_Feather, [994232], 128),
    LocationData(142, LocationName.Treasure_Isle_Rusty_Axe, [994240], 128),
    LocationData(143, LocationName.Treasure_Isle_Star_Dust, [994248], 128),
    LocationData(144, LocationName.Treasure_Isle_Jesters_Armlet, [994260], 128),
    LocationData(145, LocationName.Treasure_Isle_Fire_Brand, [994280], 128),
    LocationData(146, LocationName.Treasure_Isle_Iris_Robe, [994288], 128),
    LocationData(147, LocationName.Jupiter_Lighthouse_Erinyes_Tunic, [994336], 128),
    LocationData(148, LocationName.Jupiter_Lighthouse_Meditation_Rod, [994368], 128),
    LocationData(149, LocationName.Jupiter_Lighthouse_Phaetons_Blade, [994436], 128),
    LocationData(150, LocationName.Magma_Rock_Salamander_Tail, [994468], 128),
    LocationData(151, LocationName.Magma_Rock_Salamander_Tail, [994504], 128),
    LocationData(152, LocationName.Magma_Rock_Golem_Core, [994524], 128),
    LocationData(153, LocationName.Loho_Mythril_Silver, [994548], 131),
    LocationData(154, LocationName.Loho_Golem_Core, [994556], 131),
    LocationData(155, LocationName.Loho_Golem_Core, [994564], 131),
    LocationData(156, LocationName.Prox_Dark_Matter, [994584], 131),
    LocationData(157, LocationName.Mars_Lighthouse_Alastors_Hood, [994656], 128),
    LocationData(158, LocationName.Mars_Lighthouse_Orihalcon, [994668], 128),
    LocationData(159, LocationName.Mars_Lighthouse_Valkyrie_Mail, [994680], 128),
    LocationData(160, LocationName.Mars_Lighthouse_Sol_Blade, [994692], 128),
    LocationData(161, LocationName.Contigo_Dragon_Skin, [994716], 128),
    LocationData(162, LocationName.Anemos_Inner_Sanctum_Dark_Matter, [994728], 128),
    LocationData(163, LocationName.Anemos_Inner_Sanctum_Orihalcon, [994736], 128),
    LocationData(164, LocationName.Overworld_Rusty_Axe, [994928], 133),
    LocationData(165, LocationName.Overworld_Rusty_Mace, [994936], 133),
    LocationData(166, LocationName.Overworld_Rusty_Sword, [994944], 133),
    LocationData(167, LocationName.Overworld_Rusty_Staff, [994952], 133),
    LocationData(168, LocationName.Overworld_Rusty_Sword, [994960], 133)
]
key_items = [
    LocationData(169, LocationName.Kandorean_Temple_Mysterious_Card, [991860], 128),
    LocationData(170, LocationName.Madra_Cyclone_Chip, [16384166,991956], 128),
    LocationData(171, LocationName.Madra_Catacombs_Ruin_Key, [992036,992048], 128),
    LocationData(172, LocationName.Madra_Catacombs_Tremor_Bit, [992060], 128),
    LocationData(173, LocationName.Yampi_Desert_Trainers_Whip, [992148], 128),
    LocationData(174, LocationName.Gondowan_Cliffs_Healing_Fungus, [992656], 131),
    LocationData(175, LocationName.Gondowan_Cliffs_Laughing_Fungus, [992664], 131),
    LocationData(176, LocationName.Gabomba_Catacombs_Tomegathericon, [992888], 131),
    LocationData(177, LocationName.Shrine_of_the_Sea_God_Right_Prong, [992980], 131),
    LocationData(178, LocationName.Aqua_Rock_Aquarius_Stone, [993280], 128),
    LocationData(179, LocationName.Gaia_Rock_Dancing_Idol, [993456], 131),
    LocationData(180, LocationName.Ankohl_Ruins_Left_Prong, [993732], 131),
    LocationData(181, LocationName.Tundaria_Tower_Center_Prong, [16384200,993776], 128),
    LocationData(182, LocationName.Tundaria_Tower_Burst_Brooch, [993828], 131),
    LocationData(183, LocationName.Lemuria_Grindstone, [993916], 128),
    LocationData(184, LocationName.Jupiter_Lighthouse_Red_Key, [994376], 131),
    LocationData(185, LocationName.Jupiter_Lighthouse_Blue_Key, [994396], 131),
    LocationData(186, LocationName.Mars_Lighthouse_Teleport_Lapis, [994636], 128),
    LocationData(187, LocationName.Kandorean_Temple_Lash_Pebble, [16384160], 128),
    LocationData(188, LocationName.Dehkan_Plateau_Pound_Cube, [16384162], 128),
    LocationData(189, LocationName.Yampi_Desert_Scoop_Gem, [16384164], 128),
    LocationData(190, LocationName.Shaman_Village_Hover_Jade, [16384168], 128),
    LocationData(191, LocationName.Mars_Lighthouse_Mars_Star, [16384170], 128),
    LocationData(192, LocationName.Gabomba_Statue_Black_Crystal, [16384172], 128),
    LocationData(193, LocationName.Champa_Trident, [16384174], 128),
    LocationData(194, LocationName.E_Tundaria_Islet_Pretty_Stone, [16384176], 128),
    LocationData(195, LocationName.SE_Angara_Islet_Red_Cloth, [16384178], 128),
    LocationData(196, LocationName.N_Osenia_Islet_Milk, [16384180], 128),
    LocationData(197, LocationName.W_Indra_Islet_Lil_Turtle, [16384182], 128),
    LocationData(198, LocationName.Daila_Sea_Gods_Tear, [16384186], 128),
    LocationData(199, LocationName.Magma_Rock_Magma_Ball, [16384188], 128),
    LocationData(200, LocationName.Airs_Rock_Reveal, [16384190], 132),
    LocationData(201, LocationName.Aqua_Rock_Parch, [16384192], 132),
    LocationData(202, LocationName.Gaia_Rock_Sand, [16384194], 132),
    LocationData(203, LocationName.Magma_Rock_Blaze, [16384196], 132),
    LocationData(204, LocationName.Idejima_Shamans_Rod, [16384202], 128),
    LocationData(205, LocationName.Idejima_Mind_Read, [16384204], 132),
    LocationData(206, LocationName.Idejima_Whirlwind, [16384206], 132),
    LocationData(207, LocationName.Idejima_Growth, [16384208], 132),
    LocationData(208, LocationName.Contigo_Carry_Stone, [16384210], 128),
    LocationData(209, LocationName.Contigo_Lifting_Gem, [16384212], 128),
    LocationData(210, LocationName.Contigo_Orb_of_Force, [16384214], 128),
    LocationData(211, LocationName.Contigo_Catch_Beads, [16384216], 128),
    LocationData(212, LocationName.Kibombo_Douse_Drop, [16384218], 128),
    LocationData(213, LocationName.Kibombo_Frost_Jewel, [16384220], 128)
]
filler = [
    LocationData(214, LocationName.Kandorean_Temple_Mimic, [991872], 129),
    LocationData(215, LocationName.Dehkan_Plateau_Elixir, [991892], 128),
    LocationData(216, LocationName.Dehkan_Plateau_Mint, [991904], 128),
    LocationData(217, LocationName.Dehkan_Plateau_Nut, [991928], 128),
    LocationData(218, LocationName.Madra_Catacombs_Apple, [992008], 128),
    LocationData(219, LocationName.Madra_Catacombs_Mist_Potion, [992016], 128),
    LocationData(220, LocationName.Madra_Catacombs_Lucky_Medal, [992028], 128),
    LocationData(221, LocationName.Yampi_Desert_Antidote, [992104], 128),
    LocationData(222, LocationName.Yampi_Desert_Lucky_Medal, [992140], 128),
    LocationData(223, LocationName.Yampi_Desert_Hard_Nut, [992172], 128),
    LocationData(224, LocationName.Yampi_Desert_Cave_Water_of_Life, [992192], 128),
    LocationData(225, LocationName.Alhafra_Psy_Crystal, [992244], 128),
    LocationData(226, LocationName.Alhafran_Cave_123_coins, [992324], 128),
    LocationData(227, LocationName.Alhafran_Cave_Lucky_Medal, [992340], 128),
    LocationData(228, LocationName.Alhafran_Cave_777_coins, [992360], 128),
    LocationData(229, LocationName.Alhafran_Cave_Potion, [992368], 128),
    LocationData(230, LocationName.Alhafran_Cave_Psy_Crystal, [992376], 128),
    LocationData(231, LocationName.Mikasalla_82_coins, [992388], 128),
    LocationData(232, LocationName.Airs_Rock_Smoke_Bomb, [992496], 128),
    LocationData(233, LocationName.Airs_Rock_Cookie, [992504], 128),
    LocationData(234, LocationName.Airs_Rock_Mimic, [992520], 129),
    LocationData(235, LocationName.Airs_Rock_Vial, [992532], 128),
    LocationData(236, LocationName.Airs_Rock_Sleep_Bomb, [992540], 128),
    LocationData(237, LocationName.Airs_Rock_Vial, [992564], 128),
    LocationData(238, LocationName.Airs_Rock_Vial, [992596], 128),
    LocationData(239, LocationName.Airs_Rock_Elixir, [992608], 128),
    LocationData(240, LocationName.Airs_Rock_Psy_Crystal, [992620], 128),
    LocationData(241, LocationName.Airs_Rock_666_coins, [992644], 128),
    LocationData(242, LocationName.Gondowan_Cliffs_Sleep_Bomb, [992672], 128),
    LocationData(243, LocationName.Kibombo_Mountains_Power_Bread, [992732], 128),
    LocationData(244, LocationName.Gabomba_Statue_Mimic, [992852], 129),
    LocationData(245, LocationName.Gabomba_Statue_Elixir, [992864], 128),
    LocationData(246, LocationName.Lemurian_Ship_Potion, [992900], 128),
    LocationData(247, LocationName.Lemurian_Ship_Mist_Potion, [992928], 128),
    LocationData(248, LocationName.Taopo_Swamp_Cookie, [993096], 128),
    LocationData(249, LocationName.Taopo_Swamp_Vial, [993128], 128),
    LocationData(250, LocationName.Aqua_Rock_Nut, [993216], 128),
    LocationData(251, LocationName.Aqua_Rock_Elixir, [993224], 128),
    LocationData(252, LocationName.Aqua_Rock_Oil_Drop, [993244], 128),
    LocationData(253, LocationName.Aqua_Rock_Water_of_Life, [993256], 128),
    LocationData(254, LocationName.Aqua_Rock_Mimic, [993268], 129),
    LocationData(255, LocationName.Aqua_Rock_Lucky_Pepper, [993288], 128),
    LocationData(256, LocationName.Aqua_Rock_Crystal_Powder, [993312], 128),
    LocationData(257, LocationName.Aqua_Rock_Vial, [993332], 128),
    LocationData(258, LocationName.Gaia_Rock_Nut, [993444], 128),
    LocationData(259, LocationName.Gaia_Rock_Apple, [993464], 128),
    LocationData(260, LocationName.Gaia_Rock_Mimic, [993476], 129),
    #LocationData(261, LocationName.Ankohl_Ruins_???, [993584], 128),
    #LocationData(262, LocationName.Ankohl_Ruins_???, [993592], 128),
    #LocationData(263, LocationName.Ankohl_Ruins_???, [993600], 128),
    #LocationData(264, LocationName.Ankohl_Ruins_???, [993608], 128),
    #LocationData(265, LocationName.Ankohl_Ruins_???, [993616], 128),
    #LocationData(266, LocationName.Ankohl_Ruins_???, [993624], 128),
    LocationData(267, LocationName.Ankohl_Ruins_210_coins, [993632], 128),
    LocationData(268, LocationName.Ankohl_Ruins_Nut, [993640], 128),
    LocationData(269, LocationName.Ankohl_Ruins_Crystal_Powder, [993652], 128),
    LocationData(270, LocationName.Ankohl_Ruins_Power_Bread, [993672], 128),
    LocationData(271, LocationName.Ankohl_Ruins_365_coins, [993692], 128),
    LocationData(272, LocationName.Ankohl_Ruins_Vial, [993708], 128),
    LocationData(273, LocationName.Ankohl_Ruins_Potion, [993720], 128),
    LocationData(274, LocationName.Tundaria_Tower_Lucky_Medal, [993752], 128),
    LocationData(275, LocationName.Tundaria_Tower_Vial, [993760], 128),
    LocationData(276, LocationName.Tundaria_Tower_365_coins, [993788], 128),
    LocationData(277, LocationName.Tundaria_Tower_Mint, [993796], 128),
    LocationData(278, LocationName.Tundaria_Tower_Hard_Nut, [993808], 128),
    LocationData(279, LocationName.Tundaria_Tower_Crystal_Powder, [993816], 128),
    LocationData(280, LocationName.Hesperia_Settlement_166_coins, [993960], 128),
    LocationData(281, LocationName.Atteka_Inlet_Vial, [993996], 128),
    LocationData(282, LocationName.Contigo_Corn, [994024], 131),
    LocationData(283, LocationName.Shaman_Village_Hard_Nut, [994096], 128),
    LocationData(284, LocationName.Treasure_Isle_161_coins, [994108], 128),
    LocationData(285, LocationName.Treasure_Isle_Lucky_Medal, [994116], 128),
    #LocationData(286, LocationName.Treasure_Isle_???, [994124], 128),
    #LocationData(287, LocationName.Treasure_Isle_???, [994132], 128),
    #LocationData(288, LocationName.Treasure_Isle_???, [994140], 128),
    #LocationData(289, LocationName.Treasure_Isle_???, [994148], 128),
    #LocationData(290, LocationName.Treasure_Isle_???, [994160], 128),
    #LocationData(291, LocationName.Treasure_Isle_???, [994168], 128),
    #LocationData(292, LocationName.Treasure_Isle_???, [994176], 128),
    #LocationData(293, LocationName.Treasure_Isle_???, [994184], 128),
    #LocationData(294, LocationName.Treasure_Isle_???, [994192], 128),
    #LocationData(295, LocationName.Treasure_Isle_???, [994200], 128),
    LocationData(296, LocationName.Treasure_Isle_911_coins, [994208], 128),
    LocationData(297, LocationName.Treasure_Isle_Psy_Crystal, [994216], 128),
    LocationData(298, LocationName.Treasure_Isle_Cookie, [994224], 128),
    LocationData(299, LocationName.Treasure_Isle_Mimic, [994268], 129),
    LocationData(300, LocationName.Jupiter_Lighthouse_Potion, [994348], 128),
    LocationData(301, LocationName.Jupiter_Lighthouse_Psy_Crystal, [994356], 128),
    LocationData(302, LocationName.Jupiter_Lighthouse_Mimic, [994388], 129),
    LocationData(303, LocationName.Jupiter_Lighthouse_Mist_Potion, [994404], 128),
    LocationData(304, LocationName.Jupiter_Lighthouse_306_coins, [994412], 128),
    LocationData(305, LocationName.Jupiter_Lighthouse_Water_of_Life, [994424], 128),
    LocationData(306, LocationName.Magma_Rock_Oil_Drop, [994448], 128),
    LocationData(307, LocationName.Magma_Rock_383_coins, [994460], 128),
    LocationData(308, LocationName.Magma_Rock_Lucky_Medal, [994480], 128),
    LocationData(309, LocationName.Magma_Rock_Mist_Potion, [994492], 128),
    LocationData(310, LocationName.Magma_Rock_Mimic, [994536], 129),
    LocationData(311, LocationName.Mars_Lighthouse_Apple, [994624], 128),
    LocationData(312, LocationName.Mars_Lighthouse_Mimic, [994644], 129),
    LocationData(313, LocationName.Mars_Lighthouse_Psy_Crystal, [994704], 128),
    LocationData(314, LocationName.Shaman_Village_Elixir, [994832], 128),
    LocationData(None, LocationName.DoomDragonDefeated, [994832], 128, LocationType.Event),
    LocationData(None, LocationName.DefeatChestBeaters, [994832], 128, LocationType.Event)

]

base_djinn_index = 400

djinn_locations = [
    LocationData(base_djinn_index, LocationName.Flint, [16384000], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 1, LocationName.Granite, [16384002], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 2, LocationName.Quartz, [16384004], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 3, LocationName.Vine, [16384006], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 4, LocationName.Sap, [16384008], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 5, LocationName.Ground, [16384010], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 6, LocationName.Bane, [16384012], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 7, LocationName.Echo, [16384014], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 8, LocationName.Iron, [16384016], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 9, LocationName.Steel, [16384018], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 10, LocationName.Mud, [16384020], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 11, LocationName.Flower, [16384022], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 12, LocationName.Meld, [16384024], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 13, LocationName.Petra, [16384026], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 14, LocationName.Salt, [16384028], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 15, LocationName.Geode, [16384030], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 16, LocationName.Mold, [16384032], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 17, LocationName.Crystal, [16384034], 128, LocationType.Djinn),

    LocationData(base_djinn_index + 18, LocationName.Fizz, [16384036], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 19, LocationName.Sleet, [16384038], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 20, LocationName.Mist, [16384040], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 21, LocationName.Spritz, [16384042], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 22, LocationName.Hail, [16384044], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 23, LocationName.Tonic, [16384046], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 24, LocationName.Dew, [16384048], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 25, LocationName.Fog, [16384050], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 26, LocationName.Sour, [16384052], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 27, LocationName.Spring, [16384054], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 28, LocationName.Shade, [16384056], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 29, LocationName.Chill, [16384058], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 30, LocationName.Steam, [16384060], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 31, LocationName.Rime, [16384062,], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 32, LocationName.Gel, [16384064], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 33, LocationName.Eddy, [16384066], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 34, LocationName.Balm, [16384068], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 35, LocationName.Serac, [16384070], 128, LocationType.Djinn),

    LocationData(base_djinn_index + 36, LocationName.Forge, [16384072], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 37, LocationName.Fever, [16384074], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 38, LocationName.Corona, [16384076], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 39, LocationName.Scorch, [16384078], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 40, LocationName.Ember, [16384080], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 41, LocationName.Flash, [16384082], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 42, LocationName.Torch, [16384084], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 43, LocationName.Cannon, [16384086], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 44, LocationName.Spark, [16384088], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 45, LocationName.Kindle, [16384090], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 46, LocationName.Char, [16384092], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 47, LocationName.Coal, [16384094], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 48, LocationName.Reflux, [16384096], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 49, LocationName.Core, [16384098], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 50, LocationName.Tinder, [16384100], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 51, LocationName.Shine, [16384102], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 52, LocationName.Fury, [16384104], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 53, LocationName.Fugue, [16384106], 128, LocationType.Djinn),

    LocationData(base_djinn_index + 54, LocationName.Gust, [16384108], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 55, LocationName.Breeze, [16384110], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 56, LocationName.Zephyr, [16384112], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 57, LocationName.Smog, [16384114], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 58, LocationName.Kite, [16384116], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 59, LocationName.Squall, [16384118], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 60, LocationName.Luff, [16384120], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 61, LocationName.Breath, [16384122], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 62, LocationName.Blitz, [16384124], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 63, LocationName.Ether, [16384126], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 64, LocationName.Waft, [16384128], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 65, LocationName.Haze, [16384130], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 66, LocationName.Wheeze, [16384132], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 67, LocationName.Aroma, [16384134], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 68, LocationName.Whorl, [16384136], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 69, LocationName.Gasp, [16384138], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 70, LocationName.Lull, [16384140], 128, LocationType.Djinn),
    LocationData(base_djinn_index + 71, LocationName.Gale, [16384142], 128, LocationType.Djinn)
]

summon_index = 500

summon_tablets = [
    LocationData(summon_index + 1, LocationName.Madra_Catacombs_Moloch, [992068], 132),
    LocationData(summon_index + 2, LocationName.Yampi_Desert_Cave_Daedalus, [992212], 132),
    LocationData(summon_index + 3, LocationName.Airs_Rock_Flora, [992632], 132),
    LocationData(summon_index + 4, LocationName.Izumo_Ulysses, [993424], 132),
    LocationData(summon_index + 5, LocationName.Treasure_Isle_Azul, [994300], 132),
    LocationData(summon_index + 6, LocationName.Indra_Cavern_Zagan, [994844], 132),
    LocationData(summon_index + 7, LocationName.Osenia_Cavern_Megaera, [994856], 132),
    LocationData(summon_index + 8, LocationName.Angara_Cavern_Haures, [994868], 132),
    LocationData(summon_index + 9, LocationName.Atteka_Cavern_Coatlicue, [994880], 132),
    LocationData(summon_index + 10, LocationName.Islet_Cave_Catastrophe, [994892], 132),
    LocationData(summon_index + 11, LocationName.Anemos_Inner_Sanctum_Charon, [994904], 132),
    LocationData(summon_index + 12, LocationName.Anemos_Inner_Sanctum_Iris, [994916], 132),
    LocationData(summon_index + 13, LocationName.Lemuria_Eclipse, [16384198], 132)
]

psyenergy_index = 300

psyenergy_locations = [
    LocationData(psyenergy_index + 1, LocationName.Madra_Cyclone_Chip, [16384166, 991956], 128),
    LocationData(psyenergy_index + 2, LocationName.Madra_Catacombs_Tremor_Bit, [992060], 128),
    LocationData(psyenergy_index + 3, LocationName.Tundaria_Tower_Burst_Brooch, [993828], 131),
    LocationData(psyenergy_index + 4, LocationName.Lemuria_Grindstone, [993916], 128),
    LocationData(psyenergy_index + 5, LocationName.Mars_Lighthouse_Teleport_Lapis, [994636], 128),
    LocationData(psyenergy_index + 6, LocationName.Kandorean_Temple_Lash_Pebble, [16384160], 128),
    LocationData(psyenergy_index + 7, LocationName.Dehkan_Plateau_Pound_Cube, [16384162], 128),
    LocationData(psyenergy_index + 8, LocationName.Yampi_Desert_Scoop_Gem, [16384164], 128),
    LocationData(psyenergy_index + 9, LocationName.Shaman_Village_Hover_Jade, [16384168], 128),
    LocationData(psyenergy_index + 10, LocationName.Airs_Rock_Reveal, [16384190], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 11, LocationName.Aqua_Rock_Parch, [16384192], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 12, LocationName.Gaia_Rock_Sand, [16384194], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 13, LocationName.Magma_Rock_Blaze, [16384196], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 14, LocationName.Idejima_Mind_Read, [16384204], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 15, LocationName.Idejima_Whirlwind, [16384206], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 16, LocationName.Idejima_Growth, [16384208], 132, LocationType.Psyenergy),
    LocationData(psyenergy_index + 17, LocationName.Contigo_Carry_Stone, [16384210], 128),
    LocationData(psyenergy_index + 18, LocationName.Contigo_Lifting_Gem, [16384212], 128),
    LocationData(psyenergy_index + 19, LocationName.Contigo_Orb_of_Force, [16384214], 128),
    LocationData(psyenergy_index + 20, LocationName.Contigo_Catch_Beads, [16384216], 128),
    LocationData(psyenergy_index + 21, LocationName.Kibombo_Douse_Drop, [16384218], 128),
    LocationData(psyenergy_index + 22, LocationName.Kibombo_Frost_Jewel, [16384220], 128)
]

test_locations = [
    LocationData(1, LocationName.Daila_Herb, [991776, 991796], 2),
    LocationData(2, LocationName.Daila_Smoke_Bomb, [991784, 991804], 3),
    LocationData(3, LocationName.Daila_Psy_Crystal, [991812], 131),
    LocationData(5, LocationName.Daila_Sleep_Bomb, [991832], 3),
    LocationData(6, LocationName.Daila_3_coins, [991840], 2),
    LocationData(7, LocationName.Daila_12_coins, [991848], 2),
    LocationData(198, LocationName.Daila_Sea_Gods_Tear, [16384186], 128),

    LocationData(96, LocationName.Dehkan_Plateau_Elixir, [991892], 128),
    LocationData(97, LocationName.Dehkan_Plateau_Full_Metal_Vest, [991884], 128),
    LocationData(98, LocationName.Dehkan_Plateau_Themis_Axe, [991916], 128),
    LocationData(216, LocationName.Dehkan_Plateau_Mint, [991904], 128),
    LocationData(217, LocationName.Dehkan_Plateau_Nut, [991928], 128),

    LocationData(8, LocationName.Madra_Antidote, [991948], 13),
    LocationData(10, LocationName.Madra_Smoke_Bomb, [991968], 3),
    LocationData(11, LocationName.Madra_15_coins, [991976], 13),
    LocationData(12, LocationName.Madra_Sleep_Bomb, [991984], 2),
    LocationData(13, LocationName.Madra_Elixir, [991996], 2),
    LocationData(99, LocationName.Madra_Nurses_Cap, [991940], 128),

    LocationData(84, LocationName.Madra_Catacombs_Moloch, [992068], 132),
    LocationData(218, LocationName.Madra_Catacombs_Apple, [992008], 128),
    LocationData(219, LocationName.Madra_Catacombs_Mist_Potion, [992016], 128),
    LocationData(220, LocationName.Madra_Catacombs_Lucky_Medal, [992028], 128),
    LocationData(171, LocationName.Madra_Catacombs_Ruin_Key, [992036, 992048], 128),
]

def create_loctype_to_datamapping():
    types: Dict[str, List[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types


all_locations: List[LocationData] = test_locations + djinn_locations + psyenergy_locations + summon_tablets
location_name_to_id: Dict[str, LocationData] =  {location.name: location for location in all_locations if location.loc_type != LocationType.Event}
location_type_to_data: Dict[str, List[LocationData]] = create_loctype_to_datamapping()