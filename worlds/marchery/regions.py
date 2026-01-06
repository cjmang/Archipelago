from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import MagicArcheryWorld



def create_and_connect_regions(world: MagicArcheryWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: MagicArcheryWorld) -> None:
    forest = Region("Forest", world.player, world.multiworld)
    regions = [forest]
    world.multiworld.regions += regions


def connect_regions(world: MagicArcheryWorld) -> None:
    pass
