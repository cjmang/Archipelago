from typing import List, Dict, Optional, TYPE_CHECKING
from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, EntranceRandomizationError, \
    ERPlacementState, EntranceLookup, bake_target_group_lookup
from .Names.EntranceName import EntranceName
from .GstlaTypes import ERTestGroups
from .Connections import vanilla_connections
import logging

if TYPE_CHECKING:
    from . import GSTLAWorld

strict_direction_group_lookup = {
    ERTestGroups.NORTH: [ ERTestGroups.SOUTH],
    ERTestGroups.SOUTH: [ ERTestGroups.NORTH],
    ERTestGroups.WEST: [ ERTestGroups.EAST],
    ERTestGroups.EAST: [ ERTestGroups.WEST],
    ERTestGroups.UP: [ ERTestGroups.DOWN],
    ERTestGroups.DOWN: [ ERTestGroups.UP]  
}

direction_group_lookup = {
    0: [ERTestGroups.NORTH, ERTestGroups.SOUTH, ERTestGroups.WEST, ERTestGroups.EAST, ERTestGroups.UP, ERTestGroups.DOWN],
    ERTestGroups.NORTH: [ERTestGroups.NORTH, ERTestGroups.SOUTH, ERTestGroups.WEST, ERTestGroups.EAST, ERTestGroups.UP, ERTestGroups.DOWN],
    ERTestGroups.SOUTH: [ERTestGroups.SOUTH, ERTestGroups.NORTH, ERTestGroups.WEST, ERTestGroups.EAST, ERTestGroups.UP, ERTestGroups.DOWN],
    ERTestGroups.WEST: [ERTestGroups.WEST, ERTestGroups.EAST, ERTestGroups.NORTH, ERTestGroups.SOUTH, ERTestGroups.UP, ERTestGroups.DOWN],
    ERTestGroups.EAST: [ERTestGroups.EAST, ERTestGroups.WEST, ERTestGroups.NORTH, ERTestGroups.SOUTH, ERTestGroups.UP, ERTestGroups.DOWN],
    ERTestGroups.UP: [ERTestGroups.UP, ERTestGroups.DOWN, ERTestGroups.SOUTH, ERTestGroups.NORTH, ERTestGroups.WEST, ERTestGroups.EAST],
    ERTestGroups.DOWN: [ERTestGroups.DOWN, ERTestGroups.UP, ERTestGroups.NORTH, ERTestGroups.SOUTH, ERTestGroups.WEST, ERTestGroups.EAST]
}

transition_group_lookup = {
    ERTestGroups.OW_WALK: [ERTestGroups.SCREEN_EDGE_WALK],
    ERTestGroups.OW_SHIP: [ERTestGroups.SCREEN_EDGE_SHIP],
    ERTestGroups.SCREEN_EDGE_SHIP: [ERTestGroups.OW_SHIP, ERTestGroups.SCREEN_EDGE_SHIP],
    ERTestGroups.SCREEN_EDGE_WALK: [ERTestGroups.OW_WALK, ERTestGroups.SCREEN_EDGE_WALK],
    ERTestGroups.FALL: [ERTestGroups.FALL],
    ERTestGroups.LADDER: [ERTestGroups.LADDER],
    ERTestGroups.TELEPORT: [ERTestGroups.TELEPORT],
    ERTestGroups.CYCLONE: [ERTestGroups.CYCLONE],
    ERTestGroups.GEYSER: [ ERTestGroups.GEYSER]
}

def get_target_groups(group: int) -> List[int]:
    direction = group & ERTestGroups.DIRECTION_MASK
    transition = group & ERTestGroups.TRANSITION_MASK

    target_groups: List[int] = []
    logging.error('group -- ' + str(group) + ' -- ' + str(direction) + ' -- ' + str(transition) )

    transtion_groups = transition_group_lookup[transition]
    direction_groups = strict_direction_group_lookup[direction]
    for transition_group in transtion_groups:
        for direction_group in direction_groups:
            target_groups.append(transition_group | direction_group)

    for tg in target_groups:
        logging.error(str(tg) + ' -- ' + str(tg & ERTestGroups.DIRECTION_MASK) + ' -- ' + str(tg & ERTestGroups.TRANSITION_MASK) )
    logging.error('end of group --' + str(group))

    return target_groups

entrances_to_disconnect: List[str] = [
    EntranceName.Overworld_To_Daila_NorthSide,
    EntranceName.Daila_North_To_Overworld,
    EntranceName.Daila_South_To_Overworld,
    EntranceName.Overworld_To_Daila_SouthSide,
    EntranceName.Overworld_To_KandoreanTemple,
    EntranceName.KandoreanTemple_To_Overworld,
    EntranceName.KandoreanTemple_Outside_SideCave,
    EntranceName.KandoreanTemple_WellPath_To_CaveExit,
    EntranceName.KandoreanTemple_WellPath_To_WellRope,
    EntranceName.KandoreanTemple_TempleGrounds_WellRope,
    EntranceName.KandoreanTemple_TempleGrounds_NorthDoor,
    EntranceName.KandoreanTemple_Lobby_To_SouthDoor,
    EntranceName.KandoreanTemple_Lobby_To_NorthDoor,
    EntranceName.KandoreanTemple_DropDownLedge_Door,
    EntranceName.KandoreanTemple_LashLedge_Door,
    EntranceName.KandoreanTemple_EntryRoom_SouthDoor,
    EntranceName.KandoreanTemple_EntryRoom_BackStaircase,
    EntranceName.KandoreanTemple_JumpColumns_CentralStaircase,
    EntranceName.KandoreanTemple_JumpColumns_ZigZagsDoor,
    EntranceName.KandoreanTemple_CliffsEdge_SouthDoor,
    EntranceName.KandoreanTemple_CliffsEdge_Staircase,
    EntranceName.KandoreanTemple_WaterStream_WestsideStaircase,
    EntranceName.KandoreanTemple_WaterStream_EastsideDoorway,
    EntranceName.KandoreanTemple_GeyserPuzzles_SouthDoor,
    EntranceName.KandoreanTemple_GeyserPuzzles_WestGeyser,
    EntranceName.KandoreanTemple_GeyserPuzzles_EastGeyser,
    EntranceName.KandoreanTemple_TightRopeArea_EastGeyserPlatform,
    EntranceName.KandoreanTemple_TightRopeArea_WestGeyserPlatform,
    EntranceName.KandoreanTemple_TightRopeArea_RopeGeyser,
    EntranceName.KandoreanTemple_TightRopeArea_StairsNearRopes,
    EntranceName.KandoreanTemple_TightRopeArea_SouthEastDoor,
    EntranceName.KandoreanTemple_GeyzerPuzzleLedge_Staircase,
    EntranceName.KandoreanTemple_DjinnRoom_DoorNearLashRope,
    EntranceName.KandoreanTemple_DjinnRoom_SouthStairs,
    EntranceName.KandoreanTemple_StairWell_WestStairs,
    EntranceName.KandoreanTemple_StairWell_EastStairs,
    EntranceName.KandoreanTemple_PotRoom_SouthStairs,
    EntranceName.KandoreanTemple_PotRoom_NorthLadder,
    EntranceName.KandoreanTemple_PurpleHallway_NorthLadder,
    EntranceName.KandoreanTemple_PurpleHallway_SouthDoor,
    EntranceName.KandoreanTemple_MastersRoom_NorthWestDoor,
    EntranceName.KandoreanTemple_MastersRoom_SouthWestDoor,
    EntranceName.KandoreanTemple_MastersRoom_SouthEastDoor,
    EntranceName.Overworld_To_ShrineOfTheSeaGod,
    EntranceName.ShrineOfTheSeaGod_To_Overworld,
    EntranceName.ShrineOfTheSeaGod_EntryLow_EastDoor,
    EntranceName.ShrineOfTheSeaGod_EntryHigh_WestDoor,
    EntranceName.ShrineOfTheSeaGod_TorchedDeadEnd_WestDoor,
    EntranceName.ShrineOfTheSeaGod_QuadBridgesUpper_EasternDoor,
    EntranceName.ShrineOfTheSeaGod_QuadBridgesUpper_Stairs,
    EntranceName.ShrineOfTheSeaGod_SkippingStonesDeadEnd_Staircase,
    EntranceName.ShrineOfTheSeaGod_QuadBridgesDroppedArea_SouthStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFootstepsArea_NorthernStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFootstepsArea_WesternStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFootstepsArea_EasternStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFootstepsArea_SouthernStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFleeingBridge_WesternStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnFleeingBridge_EasternStairs,
    EntranceName.ShrineOfTheSeaGod_DjinnTorchCorner_SouthernStairs,
    EntranceName.ShrineOfTheSeaGod_FrostLedge_NorthernDoor,
    EntranceName.ShrineOfTheSeaGod_OceansView_SouthernDoor,
    EntranceName.ShrineOfTheSeaGod_OceansView_NorthEasternStairs,
    EntranceName.ShrineOfTheSeaGod_RushingWaterBridges_WesternStairs,
    EntranceName.ShrineOfTheSeaGod_RushingWaterBridgesLash_EasternStairs,
    EntranceName.ShrineOfTheSeaGod_QuadBridgesWest_WesternStairs,
    EntranceName.ShrineOfTheSeaGod_QuadBridgesWest_EasternStairs,
    EntranceName.ShrineOfTheSeaGod_WateryShrineInWater_SouthWestStairs,
    EntranceName.ShrineOfTheSeaGod_WateryShrineInWater_ElevateShrine,
    EntranceName.ShrineOfTheSeaGod_ElevatedShrine_LoweringShrine,
    EntranceName.ShrineOfTheSeaGod_ElevatedShrine_NorthWestLadder,
    EntranceName.ShrineOfTheSeaGod_UpperTowerArea_WestLadder,
    EntranceName.ShrineOfTheSeaGod_UpperTowerArea_EastLadder,
    EntranceName.ShrineOfTheSeaGod_TopOfTheShrine_EastLadder,
    EntranceName.DehkanPlateau_West_To_Overworld,
    EntranceName.DehkanPlateau_East_To_Overworld,
    EntranceName.Overworld_To_DehkanPlateau_NorthWestSide,
    EntranceName.Overworld_To_DehkanPlateau_SouthEastSide,
    EntranceName.DehkanPlateau_TripleStairsCrackedFloor,
    EntranceName.DehkanPlateau_TripleStairsUpperLedgeEasternExit,
    EntranceName.DehkanPlateau_TripleStairsUpperLedgeDoorway,
    EntranceName.DehkanPlateau_IsolatedNearTripleStairs_Doorway,
    EntranceName.DehkanPlateau_HorizontalOvalShapedCave_NorthDoorway,
    EntranceName.DehkanPlateau_HorizontalOvalShapedCave_SouthDoorway,
    EntranceName.DehkanPlateau_TripleStonePillars_WesternExit,
    EntranceName.DehkanPlateau_TripleStonePillars_NorthernExit,
    EntranceName.DehkanPlateau_TripleStonePillars_CrackedFloor,
    EntranceName.DehkanPlateau_TeasingCavernSouthernExit,
    EntranceName.DehkanPlateau_UShapedCavern_WestDoorway,
    EntranceName.DehkanPlateau_UShapedCavern_EastDoorway,
    EntranceName.DehkanPlateau_StonePillarsLogLedge_Doorway,
    EntranceName.DehkanPlateau_StonePillarMaze_SouthernExit,
    EntranceName.DehkanPlateau_StonePillarMaze_EasternExit,
    EntranceName.DehkanPlateau_CrackedFloorsRockSlide_WesternExit,
    EntranceName.DehkanPlateau_CrackedFloorsRockSlide_CrackedFloor,
    EntranceName.DehkanPlateau_BalloonCavern_SouthernExit,
    EntranceName.DehkanPlateau_MirrorJCavern_WesternExit,
    EntranceName.DehkanPlateau_MirrorJCavern_EasternExit,
    EntranceName.DehkanPlateau_IsolatedCrakcedFloorsArea_Doorway,
    EntranceName.DehkanPlateau_IsolatedCrakcedFloorsArea_CrackedFloor,
    EntranceName.DehkanPlateau_SideEyeCavern_Doorway,
    EntranceName.DehkanPlateau_RockSlideArea_Doorway,
    EntranceName.DehkanPlateau_RockSlideArea_EasternExit,
    EntranceName.DehkanPlateau_RopeBridge_WesternExit,
    EntranceName.DehkanPlateau_RopeBridge_Doorway,
    EntranceName.DehkanPlateau_RopeBridge_CrackedFloor,
    EntranceName.DehkanPlateau_BottleCavern_Doorway,
    EntranceName.DehkanPlateau_BelowRopeBridge_EasternExit,
    EntranceName.DehkanPlateau_CrampedWesternLedge_WesternExit,
    EntranceName.DehkanPlateau_MiddleLedgeBetweenPillars_Doorway,
    EntranceName.DehkanPlateau_ThreeAngledCavern_NorthernDoorway,
    EntranceName.DehkanPlateau_ThreeAngledCavern_EasternDoorway,
    EntranceName.DehkanPlateau_CrackedFloorCaveLowerHalf_EasternDoorway,
    EntranceName.DehkanPlateau_CrackedFloorCaveLowerHalf_SouthernDoorway,
    EntranceName.DehkanPlateau_CrackedFloorCaveLowerHalf_WesternDoorway,
    EntranceName.DehkanPlateau_CrackedFloorCave_CrackedFloor,
    EntranceName.DehkanPlateau_CrackedFloorCaveUpperHalf_NorthenDoorway,
    EntranceName.DehkanPlateau_DeepCavenDropDownArea_Doorway,
    EntranceName.DehkanPlateau_PoundPillarCavernUpperHalf_WesternDoorway,
    EntranceName.DehkanPlateau_PoundPillarCavernUpperHalf_EasternDoorway,
    EntranceName.DehkanPlateau_PoundPillarCavernLowerHalf_WesternDoorway,
    EntranceName.DehkanPlateau_PoundPillarCavernLowerHalf_EasternDoorway,
    EntranceName.DehkanPlateau_CrackedFloorsNorthOfPillar_Doorway,
    EntranceName.DehkanPlateau_CrackedFloorsNorthOfPillar_CrackedFloor,
    EntranceName.DehkanPlateau_DeepCavernUpperLedge_NorthernDoorway,
    EntranceName.DehkanPlateau_DeepCavernUpperLedge_SouthernDoorway,
    EntranceName.DehkanPlateau_DjinnCombatCavernRoom_NorthernDoorway,
    EntranceName.DehkanPlateau_DjinnCombatCavernRoom_SouthernDoorway,
    EntranceName.DehkanPlateau_FlatHallwayDeepCavern_WesternDoorway,
    EntranceName.DehkanPlateau_FlatHallwayDeepCavern_EasternDoorway,
    EntranceName.DehkanPlateau_QuadStairs_EasternDoorway,
    EntranceName.Overworld_To_IndraCavern,
    EntranceName.IndraCavern_To_Overworld,
    EntranceName.Overworld_To_Madra,
    EntranceName.Madra_To_Overworld,
    EntranceName.MadraToMadraCatacombsEast,
    EntranceName.MadraToMadraCatacombsWest,
    EntranceName.MadraCatacombsEastToMadra,
    EntranceName.MadraCatacombsWestToMadra,
    EntranceName.MadraCatacombsLadderRoomEast_SouthernDoorway,
    EntranceName.MadraCatacombsLadderRoomWest_SouthernDoorway,
    EntranceName.MadraCatacombsEastConnectorRoom_NorthEasternDoorway,
    EntranceName.MadraCatacombsEastConnectorRoom_NorthWesternDoorway,
    EntranceName.MadraCatacombsEastConnectorRoom_SouthWesternDoorway,
    EntranceName.MadraCatacombsRockBlockedRoom_SouthernDoorway,
    EntranceName.MadraCatacombsRockLedgeEastRidge_Doorway,
    EntranceName.MadraCatacombsRockLedgeWestRidge_NorthernDoorway,
    EntranceName.MadraCatacombsRockLedgeWestRidge_WesternDoorway,
    EntranceName.MadraCatacombsRuinsEntry_EasternDoorway,
    EntranceName.MadraCatacombsMainRuinsArea_MainRuinEntry,
    EntranceName.MadraCatacombsBackRuins_EasternRuinEntry,
    EntranceName.MadraCatacombsUpperRuinsArea_RuinsUpperDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EasternHallway_EasternLedge_SouthExit,
    EntranceName.MadraCatacombsRuinedBuilding_EasternHallway_EasternLedge_Stairway,
    EntranceName.MadraCatacombsRuinedBuilding_TightRidge_Stairway,
    EntranceName.MadraCatacombsRuinedBuilding_TightRidge_Doorway,
    EntranceName.MadraCatacombsRuinedBuilding_TremorRoom_SouthDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EntryHall_SouthernDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EntryHall_WesternDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EntryHall_NorthernDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EntryHall_EastStairs,
    EntranceName.MadraCatacombsRuinedBuilding_EntryHall_EasternDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_CollapsedHall_SouthDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_CentralRoom_SouthDoor,
    EntranceName.MadraCatacombsRuinedBuilding_MainUpstairsEastArea_EastStairs,
    EntranceName.MadraCatacombsRuinedBuilding_MainUpstairsEastArea_EastDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_EastBedroom_Doorway,
    EntranceName.MadraCatacombsRuinedBuilding_EasternHallway_WesternLedge_SouthDoor,
    EntranceName.MadraCatacombsRuinedBuilding_EasternHallway_WesternLedge_DownStairway,
    EntranceName.MadraCatacombsRuinedBuilding_EasternHallway_WesternLedge_UpStairway,
    EntranceName.MadraCatacombsRuinedBuilding_LockedRoom_Stairway,
    EntranceName.MadraCatacombsRuinedBuilding_LongHallway_EastDownStairway,
    EntranceName.MadraCatacombsRuinedBuilding_LongHallway_WestDownStairway,
    EntranceName.MadraCatacombsRuinedBuilding_CollapsedHall_NorthSide_Stairway,
    EntranceName.MadraCatacombsRuinedBuilding_MainUpstairsWestArea_SouthDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_MainUpstairsWestArea_NorthDoorway,
    EntranceName.MadraCatacombsRuinedBuilding_WestBedroom_Doorway,
    EntranceName.Overworld_To_MadraDrawbridge_SouthSide,
    EntranceName.Overworld_To_MadraDrawbridge_NorthSide,
    EntranceName.MadraDrawbridge_South_To_Overworld,
    EntranceName.MadraDrawbridge_North_To_Overworld,
    EntranceName.Overworld_To_OseniaCliffs_WestSide,
    EntranceName.Overworld_To_OseniaCliffs_EastSide,
    EntranceName.OseniaCliffs_West_To_Overworld,
    EntranceName.OseniaCliffs_East_To_Overworld,
    EntranceName.Overworld_To_Mikasalla,
    EntranceName.Mikasalla_To_Overworld,
    EntranceName.Overworld_To_OseniaCavern,
    EntranceName.OseniaCavern_To_Overworld,
    EntranceName.Overworld_To_Garoh,
    EntranceName.Garoh_To_Overworld,
    EntranceName.Overworld_To_AirsRock,
    EntranceName.AirsRock_To_Overworld,
    EntranceName.Overworld_To_Alhafra,
    EntranceName.Alhafra_To_Overworld
]

def perform_entrance_rando(world: 'GSTLAWorld'):
    disconnect_entrances(world)
    target_group_lookup = bake_target_group_lookup(world, get_target_groups)
    return randomize_entrances(world, True, target_group_lookup, True)

def disconnect_entrances(world: 'GSTLAWorld'):
    for ent in entrances_to_disconnect:
        entrance = world.get_entrance(ent)
        connection_data = vanilla_connections[entrance.name]

        if entrance.randomization_group & ERTestGroups.DIRECTION_MASK == ERTestGroups.NORTH:
            logging.error('North: ' + entrance.name)

        
        if entrance.randomization_group & ERTestGroups.DIRECTION_MASK == ERTestGroups.EAST:
            logging.error('East: ' + entrance.name)

        if entrance.randomization_type == EntranceType.ONE_WAY:
            disconnect_entrance_for_randomization(entrance, target_group=connection_data.target_rando_group ,one_way_target_name=connection_data.target_name)
        else:
            disconnect_entrance_for_randomization(entrance)