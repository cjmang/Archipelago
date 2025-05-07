from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SpireWorld


def create_regions(world: 'SpireWorld', player: int):
    from . import create_region

    multiworld = world.multiworld

    multiworld.regions.append(create_region(multiworld, player, 'Menu', None, ['Neow\'s Room']))

    multiworld.regions.append(create_region(multiworld, player, "Neow's Room", None, ["Early Act 1"]))
    # link up our region with the entrance we just made
    # multiworld.get_entrance("Neow's Room", player).connect(multiworld.get_region('Early Act 1', player))

    multiworld.regions.append(create_region(multiworld, player, 'Early Act 1',
                                   [
                                       "Card Draw 1",
                                       "Card Draw 2",
                                       "Card Draw 3",
                                   ],
                                        ["Mid Act 1"]))

    multiworld.regions.append(create_region(multiworld, player, 'Mid Act 1',
                                   [
                                       'Card Draw 4',
                                       'Card Draw 5',
                                       'Relic 1',
                                       'Relic 2',
                                   ],["Late Act 1"]))

    multiworld.regions.append(create_region(multiworld, player, 'Late Act 1',
                                   [
                                       'Relic 3',
                                       'Act 1 Boss',
                                       'Rare Card Draw 1',
                                       'Boss Relic 1'
                                   ], ["Early Act 2"]))

    multiworld.regions.append(create_region(multiworld, player, 'Early Act 2',
                                   [
                                       "Card Draw 6",
                                       "Card Draw 7",
                                   ], ["Mid Act 2"]))

    multiworld.regions.append(create_region(multiworld, player, 'Mid Act 2',
                                   [
                                        'Card Draw 8',
                                       'Relic 4',
                                       'Relic 5'
                                   ], ["Late Act 2"]))

    multiworld.regions.append(create_region(multiworld, player, 'Late Act 2',
                                   [
                                       'Card Draw 9',
                                       'Card Draw 10',
                                       'Relic 6',
                                       'Act 2 Boss',
                                       'Rare Card Draw 2',
                                       'Boss Relic 2',
                                   ], ["Early Act 3"]))

    multiworld.regions.append(create_region(multiworld, player, 'Early Act 3',
                                   [
                                       "Card Draw 11",
                                       "Card Draw 12",
                                   ], ["Mid Act 3"]))

    multiworld.regions.append(create_region(multiworld, player, 'Mid Act 3',
                                   [
                                       "Card Draw 13",
                                       "Relic 7",
                                       "Relic 8",
                                   ], ["Late Act 3"]))

    multiworld.regions.append(create_region(multiworld, player, 'Late Act 3',
                                   [
                                        "Card Draw 14",
                                       "Card Draw 15",
                                       "Relic 9",
                                       "Relic 10",
                                       "Act 3 Boss"
                                   ], ["Act 4"]))

    multiworld.regions.append(create_region(multiworld, player, 'Act 4',
                                   [
                                        "Heart Room"
                                   ]))

    for region in multiworld.get_regions(player):
        if region.name == 'Menu':
            continue
        entrance = world.get_entrance(region.name)
        entrance.connect(region)
