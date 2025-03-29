from typing import List
from BaseClasses import MultiWorld, EntranceType
from .Names.RegionName import RegionName
from .Names.EntranceName import EntranceName
from .GstlaTypes import EntranceData, ERTestGroups

vanilla_connections: List[EntranceData] = \
[
    EntranceData(EntranceName.Menu_StartGame, RegionName.Indra_Idejima),
    EntranceData(EntranceName.AnywhereToJoinedPartyMembers, RegionName.PartyMembers),

    #Overworld
    EntranceData(EntranceName.Overworld_To_Daila_NorthSide, RegionName.Indra_Daila, '2:3', ERTestGroups.SOUTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Daila_SouthSide, RegionName.Indra_Daila, '2:2', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_KandoreanTemple, RegionName.Indra_KandoreanTemple, '2:4', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_ShrineOfTheSeaGod, RegionName.Indra_ShrineOfTheSeaGod, '2:5', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_DehkanPlateau_NorthWestSide, RegionName.Indra_DehkanPlateau, '2:6',  ERTestGroups.EAST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_DehkanPlateau_SouthEastSide, RegionName.Indra_DehkanPlateau, '2:7',  ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_IndraCavern, RegionName.IndraCavern, '2:83', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Madra, RegionName.Madra, '2:9', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_GondowanCliffs_EastSide, RegionName.GondowanCliffs, '2:22', ERTestGroups.WEST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_MadraDrawbridge_SouthSide, RegionName.MadraDrawBridge, '2:10', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_MadraDrawbridge_NorthSide, RegionName.MadraDrawBridge, '2:11', ERTestGroups.SOUTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_OseniaCliffs_WestSide, RegionName.OseniaCliffs, '2:12', ERTestGroups.EAST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_OseniaCliffs_EastSide, RegionName.OseniaCliffs, '2:13', ERTestGroups.WEST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Mikasalla, RegionName.Mikasalla, '2:14', ERTestGroups.WEST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_OseniaCavern, RegionName.OseniaCavern, '2:82', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Garoh, RegionName.Garoh, '2:15', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_AirsRock, RegionName.AirsRock, '2:16', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_YampiDesertFront, RegionName.YampiDesertFront, '2:17', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_Garoh_To_YampiDesertBack, RegionName.YampiDesertBack, '2:19', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_Alhafra_To_YampiDesertBack, RegionName.YampiDesertBack, '2:18', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Alhafra, RegionName.Alhafra, '2:20', ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_GondowanCliffs_WestSide, RegionName.GondowanCliffs, '2:21', ERTestGroups.EAST | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Naribwe_SouthSide, RegionName.Naribwe, '2:23', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Naribwe_NorthSide, RegionName.Naribwe, '2:24', ERTestGroups.SOUTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_KibomboMountains_SouthSide, RegionName.KibomboMountains, '2:25', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_KibomboMountains_NorthSide, RegionName.KibomboMountains, '2:26', ERTestGroups.SOUTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_To_Kibombo, RegionName.Kibombo, '2:27', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_WestIndraIslet_To_WestIndraIslet, RegionName.WestIndraIslet, '2:28', ERTestGroups.NORTH | ERTestGroups.OW_WALK),
    EntranceData(EntranceName.Overworld_EastTundariaIslet_To_EastTundariaIslet, RegionName.EastTundariaIslet, '2:29', ERTestGroups.NORTH | ERTestGroups.OW_WALK),

    #Indra
    EntranceData(EntranceName.Idejima_To_Overworld, RegionName.Indra_IdejimaArea, '9:4', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK, EntranceType.ONE_WAY),
    EntranceData(EntranceName.Daila_North_To_Overworld, RegionName.Indra_IdejimaArea, '13:9', ERTestGroups.NORTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Daila_South_To_Overworld, RegionName.Indra_NorthernIndra, '13:8', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.KandoreanTemple_To_Overworld, RegionName.Indra_NorthernIndra, '21:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.ShrineOfTheSeaGod_To_Overworld, RegionName.Indra_NorthernIndra, '23:3', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.DehkanPlateau_West_To_Overworld, RegionName.Indra_NorthernIndra, '34:1', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.DehkanPlateau_East_To_Overworld, RegionName.Indra_SouthernIndra, '36:6', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.IndraCavern_To_Overworld, RegionName.Indra_SouthernIndra, '275:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Madra_To_Overworld, RegionName.Indra_SouthernIndra, '44:11', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.GondowanCliffs_East_To_Overworld, RegionName.Indra_SouthernIndra, '102:2', ERTestGroups.EAST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.MadraDrawbridge_South_To_Overworld, RegionName.Indra_SouthernIndra, '53:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.MadraDrawbridge_North_To_Overworld, RegionName.Indra_MadraDrawBridgeArea, '53:2', ERTestGroups.NORTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.OseniaCliffs_West_To_Overworld, RegionName.Indra_MadraDrawBridgeArea, '54:1', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.OseniaCliffs_East_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '54:2', ERTestGroups.EAST | ERTestGroups.SCREEN_EDGE_WALK),

    #Osenia
    EntranceData(EntranceName.Mikasalla_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '55:6', ERTestGroups.EAST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.OseniaCavern_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '276:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Garoh_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '61:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.AirsRock_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '82:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.YampiDesertBack_To_Overworld_Garoh, RegionName.Oseania_SouthWesternOsenia, '75:2', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.YampDesertFront_To_Overworld, RegionName.Oseania_SouthWesternOsenia, '67:1', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.YampiDesertBack_To_Overworld_Alhafra, RegionName.Oseania_AlhafraArea, '74:2', ERTestGroups.NORTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Alhafra_To_Overworld, RegionName.Oseania_AlhafraArea, '95:9', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
 
    #Gondowan
    EntranceData(EntranceName.GondowanCliffs_West_To_Overworld, RegionName.Gondowan_SouthernGondowan, '102:1', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Naribwe_South_To_Overworld, RegionName.Gondowan_SouthernGondowan, '105:6', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Naribwe_North_To_Overworld, RegionName.Gondowan_SouthernGondowan, '105:7', ERTestGroups.NORTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.KibomboMountains_South_To_Overworld, RegionName.Gondowan_SouthernGondowan, '108:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.KibomboMountains_NorthWest_To_Overworld, RegionName.Gondowan_CentralGondowan, '107:1', ERTestGroups.WEST | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.Kibombo_To_Overworld, RegionName.Gondowan_CentralGondowan, '113:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),


    #Eastern Sea
    EntranceData(EntranceName.Overworld_Indra_North_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_Indra_South_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_Oseania_AlhafraArea_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_Gondowan_Central_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_Gondowan_South_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_WestIndraIslet_To_EasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.Overworld_EastTundariaIslet_To_EasternSea, RegionName.EasternSea),

    EntranceData(EntranceName.Overworld_EasternSea_To_Indra_North, RegionName.Indra_NorthernIndra),
    EntranceData(EntranceName.Overworld_EasternSea_To_Indra_South, RegionName.Indra_SouthernIndra),
    EntranceData(EntranceName.Overworld_EasternSea_To_Osenia_AlhafraArea, RegionName.Oseania_AlhafraArea),
    EntranceData(EntranceName.Overworld_EasternSea_To_Gondowan_Central, RegionName.Gondowan_CentralGondowan),
    EntranceData(EntranceName.Overworld_EasternSea_To_Gondowan_South, RegionName.Gondowan_SouthernGondowan),
    EntranceData(EntranceName.Overworld_EasternSea_To_WestIndraIslet, RegionName.Overworld_WestIndraIslet),
    EntranceData(EntranceName.Overworld_EasternSea_To_EastTundariaIslet, RegionName.Overworld_EastTundariaIslet),


    EntranceData(EntranceName.WestIndraIslet_To_Overworld, RegionName.Overworld_WestIndraIslet, '131:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),
    EntranceData(EntranceName.EastTundariaIslet_To_Overworld, RegionName.Overworld_EastTundariaIslet, '132:1', ERTestGroups.SOUTH | ERTestGroups.SCREEN_EDGE_WALK),



    EntranceData(EntranceName.MadraToMadraCatacombs, RegionName.MadraCatacombs),
    EntranceData(EntranceName.MadraToLemurianShip, RegionName.Lemurian_Ship),
    EntranceData(EntranceName.YampiDesertFrontToYampiDesertBack, RegionName.YampiDesertBack),
    EntranceData(EntranceName.YampiDesertBackToYampiDesertCave, RegionName.YampiDesertCave),
    EntranceData(EntranceName.AlhafraToAlhafraCave, RegionName.AlhafraCave),
    EntranceData(EntranceName.KibomboToGabombaStatue, RegionName.GabombaStatue),
    EntranceData(EntranceName.GabombaStatueToGabombaCatacombs, RegionName.GabombaCatacombs),
    EntranceData(EntranceName.EasternSeaToNorthOseniaIslet, RegionName.NorthOseniaIslet),
    EntranceData(EntranceName.EasternSeaToSouthEastAngaraIslet, RegionName.SouthEastAngaraIslet),
    EntranceData(EntranceName.EasternSeaToSeaOfTimeIslet, RegionName.SeaOfTimeIslet),
    EntranceData(EntranceName.EasternSeaToSeaOfTime, RegionName.SeaOfTime),
    EntranceData(EntranceName.EasternSeaToTreasureIsland, RegionName.TreasureIsland),
    EntranceData(EntranceName.EasternSeaToChampa, RegionName.Champa),
    EntranceData(EntranceName.EasternSeaToAnkohlRuins, RegionName.AnkohlRuins),
    EntranceData(EntranceName.EasternSeaToIzumo, RegionName.Izumo),
    EntranceData(EntranceName.EasternSeaToGaiaRock, RegionName.GaiaRock),
    EntranceData(EntranceName.EasternSeaToYallam, RegionName.Yallam),
    EntranceData(EntranceName.EasternSeaToTundariaTower, RegionName.TundariaTower),
    EntranceData(EntranceName.EasternSeaToApojiiIslands, RegionName.ApojiiIslands),
    EntranceData(EntranceName.EasternSeaToAquaRock, RegionName.AquaRock),
    EntranceData(EntranceName.EasternSeaToWesternSea, RegionName.WesternSea),
    EntranceData(EntranceName.SeaOfTimeIsletToIsletCave, RegionName.IsletCave),
    EntranceData(EntranceName.TreasureIslandToTreasureIsland_Grindstone, RegionName.TreasureIsland_Grindstone),
    EntranceData(EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion, RegionName.TreasureIsland_PostReunion),
    EntranceData(EntranceName.TundariaTowerToTundariaTower_Parched, RegionName.TundariaTower_Parched),
    EntranceData(EntranceName.AnkohlRuinsToAnkohlRuins_Sand, RegionName.AnkohlRuins_Sand),
    EntranceData(EntranceName.YallamToTaopoSwamp, RegionName.TaopoSwamp),
    EntranceData(EntranceName.SeaOfTimeToLemuria, RegionName.Lemuria),
    EntranceData(EntranceName.LemuriaToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    EntranceData(EntranceName.WesternSeaToSouthWestAttekaIslet, RegionName.SouthWestAttekaIslet),
    EntranceData(EntranceName.WesternSeaToHesperiaSettlement, RegionName.HesperiaSettlement),
    EntranceData(EntranceName.WesternSeaToShamanVillageCave, RegionName.ShamanVillageCave),
    EntranceData(EntranceName.WesternSeaToAttekaInlet, RegionName.AttekaInlet),
    EntranceData(EntranceName.WesternSeaToAttekaCavern, RegionName.AttekaCavern),
    EntranceData(EntranceName.WesternSeaToGondowanSettlement, RegionName.GondowanSettlement),
    EntranceData(EntranceName.WesternSeaToMagmaRock, RegionName.MagmaRock),
    EntranceData(EntranceName.WesternSeaToLoho, RegionName.Loho),
    EntranceData(EntranceName.WesternSeaToAngaraCavern, RegionName.AngaraCavern),
    EntranceData(EntranceName.WesternSeaToKaltIsland, RegionName.KaltIsland),
    EntranceData(EntranceName.WesternSeaToProx, RegionName.Prox),
    EntranceData(EntranceName.ShamanVillageCaveToShamanVillage, RegionName.ShamanVillage),
    EntranceData(EntranceName.AttekaInletToContigo, RegionName.Contigo),
    EntranceData(EntranceName.AttekaInletToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    EntranceData(EntranceName.ContigoToJupiterLighthouse, RegionName.JupiterLighthouse),
    EntranceData(EntranceName.ContigoToAnemosInnerSanctum, RegionName.AnemosSanctum),
    EntranceData(EntranceName.ContigoToReunion, RegionName.Reunion),
    EntranceData(EntranceName.MagmaRockToMagmaRockInterior, RegionName.MagmaRockInterior),
    EntranceData(EntranceName.ProxToMarsLighthouse, RegionName.MarsLighthouse),
    EntranceData(EntranceName.MarsLighthouseToMarsLighthouse_Activated, RegionName.MarsLighthouse_Activated)
]


def create_vanilla_connections(multiworld: MultiWorld, player: int):
    for connection in vanilla_connections:
        entrance = multiworld.get_entrance(connection.source_entrance, player)
        target = multiworld.get_region(connection.target, player)

        entrance.connect(target)