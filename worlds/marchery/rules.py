from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .world import MagicArcheryWorld


def set_all_rules(world: MagicArcheryWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: MagicArcheryWorld) -> None:
    pass


def set_all_location_rules(world: MagicArcheryWorld) -> None:
    pass


def set_completion_condition(world: MagicArcheryWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: True
