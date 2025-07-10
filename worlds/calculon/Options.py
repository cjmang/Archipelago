from dataclasses import dataclass

from schema import Schema, Optional

from Options import PerGameCommonOptions, OptionSet, Range, OptionDict


class Games(OptionSet):
    """Which games to do simulations on.  If empty, will run simulations for all games in the multiworld."""
    default = {}

class Skip(OptionSet):
    """Which games to skip doing simulations on."""
    default = {"Clique", "APBingo", "Slotlock"}

class NumberOfSims(Range):
    default = 10
    range_start = 10
    range_end = 10000

class ItemGroups(OptionDict):
    """Which items for games should be treated as the same.  Sometimes games have unique items but the
    effect on logic is identical.  This dilutes what Calculon will compute, so adding them in a bunch
    will help get a proper analysis of the items.

    There are two ways to do this:

        "Game Name":
            item_groups:
             - "item group name 1"
             - "item group name 2"

    Or alternatively:
        "Game Name":
            "custom group name 1":
                - "item name 1"
                - "item name 2"
            "custom group name 2:
                - "item name 1"
                - "item name 2"

    Note in either case that the items cannot be in multiple groups at the same time.  This will cause the analysis
    to fail.
    """
    default = {
        "Golden Sun The Lost Age": {
            "item_groups": [ "Character" ],
        },
        "Hollow Knight": {
            "item_groups": ["Dive", "Fireball", "Charms", "Dreamers", "Scream"],
        }
    }
    schema = Schema({
        str: {
            Optional("item_groups", default=[]): [str],
            Optional(str): {
                str: [str]
            }
        }
    })

@dataclass
class CalculonOptions(PerGameCommonOptions):
    games: Games
    skip_games: Skip
    num_sims: NumberOfSims
    item_groups: ItemGroups