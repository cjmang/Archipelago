from __future__ import annotations

import dataclasses
import math
from typing import TYPE_CHECKING, cast

from rule_builder.field_resolvers import FieldResolver
from rule_builder.rules import HasGroup, Rule
from worlds.gstla.gstla_types import ItemType

if TYPE_CHECKING:
    from worlds.gstla import GSTLAWorld


@dataclasses.dataclass(frozen=True)
class DjinnLogicCount(FieldResolver, game='Golden Sun The Lost Age'):
    count: int

    def resolve(self, world) -> int:
        world = cast('GSTLAWorld', world)
        return math.ceil(self.count * (world.options.djinn_logic.value / 100))


def has_djinn(count: int) -> Rule:
    return HasGroup(ItemType.Djinn.name, DjinnLogicCount(count))
