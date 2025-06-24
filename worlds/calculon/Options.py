from dataclasses import dataclass

from Options import PerGameCommonOptions, OptionSet


class Games(OptionSet):
    """Which game to do simulations on.  Use "all" to do simulations on every game"""
    default = {"all"}

@dataclass
class CalculonOptions(PerGameCommonOptions):
    games: Games