import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Self

import orjson

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemData, ItemType


class BaseItem(ABC):
    """
    Base class for all AP items.
    All subclasses should use @dataclass(frozen=True, slots=True, kw_only=True)
    This is the poor mans Pydantic model so that we can guarantee that the model is really what it looks like.
    Also: a slotted dataclass should reduce memory usage quite a bit. If we have hundreds to thousands of instances,
    this is probably pretty good. Only drawback: Can't use super() calls in those subclasses.
    But the tradeoff's worth it, I think.
    """

    # TODO: classvars here should probably be validated, gotta use __init_subclass__ or something iirc
    ITEM_TYPE: ClassVar[ItemType]
    CLASSIFICATION: ClassVar[ItemClassification]
    CATEGORY: ClassVar[ItemCategory]

    ap_id: int
    name: str

    @property
    def in_pool(self) -> bool:
        # only use this if you want to filter some items,
        # like a "cloak" psynergy or some summons
        return True

    def as_item(self) -> ItemData:
        return ItemData(
            id=self.ap_id,
            name=self.name,
            type=self.ITEM_TYPE,
            classification=self.CLASSIFICATION,
            category=self.CATEGORY,
        )

    @classmethod
    @abstractmethod
    def load(cls, *args: Any, **kwargs: Any) -> tuple[Self, ...]:
        """Every subclass should be able to decide itself where it comes from. Most get filled by data/*.json files."""

    @staticmethod
    def read_json(path: str | Path) -> dict:
        return orjson.loads(pkgutil.get_data('worlds.gstla', str(path)))
