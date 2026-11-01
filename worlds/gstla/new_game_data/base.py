import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import orjson

from worlds.gstla.gstla_types import ItemCategory, ItemData, ItemType

if TYPE_CHECKING:
    from BaseClasses import ItemClassification


class BaseItem(ABC):
    """
    Base class for all AP items.
    All subclasses should use @dataclass(frozen=True, slots=True, kw_only=True)
    This is the poor mans Pydantic model so that we can guarantee that the model is really what it looks like.
    Also: a slotted dataclass should reduce memory usage quite a bit. If we have hundreds to thousands of instances,
    this is probably pretty good. Only drawback: Can't use super() calls in those subclasses.
    But the tradeoff's worth it, I think.
    """
    if TYPE_CHECKING:

        @property
        def ap_id(self) -> int: ...

        @property
        def name(self) -> str: ...

        @property
        def item_type(self) -> ItemType: ...

        @property
        def classification(self) -> ItemClassification: ...

        @property
        def category(self) -> ItemCategory: ...

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        for attr in ['item_type', 'classification', 'category']:
            if not hasattr(cls, attr):
                raise TypeError(f'{cls.__name__} must set {attr} as a field or as a property')

    @property
    def in_pool(self) -> bool:
        # only use this if you want to filter some items,
        # like a "cloak" psynergy or some summons
        return True

    def as_item(self) -> ItemData:
        return ItemData(
            id=self.ap_id,
            name=self.name,
            type=self.item_type,
            classification=self.classification,
            category=self.category,
        )

    @classmethod
    @abstractmethod
    def load(cls, *args: Any, **kwargs: Any) -> tuple[Self, ...]:
        """Every subclass should be able to decide itself where it comes from. Most get filled by data/*.json files."""

    @staticmethod
    def read_json(path: str | Path) -> dict:
        data_path = pkgutil.get_data('worlds.gstla', str(path))
        if data_path is None:
            raise ValueError(f'Could not find json file {path=}')
        return orjson.loads(data_path)
