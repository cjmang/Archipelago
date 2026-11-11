from abc import ABC, abstractmethod
from importlib.resources import files
from inspect import get_annotations
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import orjson

from worlds.gstla.gstla_types import ItemCategory, ItemData, ItemType, LocationData, LocationRestriction, LocationType

if TYPE_CHECKING:
    from BaseClasses import ItemClassification


PKG_ROOT = files('worlds.gstla')


def read_json(path: str | Path) -> Any:
    return orjson.loads((PKG_ROOT / str(path)).read_bytes())


def read_json_dir(path: str | Path) -> dict[str, Any]:
    directory = PKG_ROOT / str(path)
    return {file.name: orjson.loads(file.read_bytes()) for file in directory.iterdir() if file.name.endswith('.json')}


def _check_required_fields(cls: 'type[BaseItem | BaseLocation]') -> None:
    for attr in getattr(cls, '_required_fields', []):
        if not hasattr(cls, attr) and not any(attr in get_annotations(base) for base in cls.__mro__):
            raise TypeError(f'{cls.__name__} must set {attr} as a field or as a property')


class BaseItem(ABC):
    """
    Base class for all AP items.
    All subclasses should use @dataclass(frozen=True, slots=True, kw_only=True)
    This is the poor mans Pydantic model so that we can guarantee that the model is really what it looks like.
    Also: a slotted dataclass should reduce memory usage quite a bit. If we have hundreds to thousands of instances,
    this is probably pretty good. Only drawback: Can't use super() calls in those subclasses.
    But the tradeoff's worth it, I think.
    """

    _required_fields = ['ap_id', 'name', 'item_type', 'classification', 'category']

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
        _check_required_fields(cls)

    @property
    def shuffled(self) -> bool:
        """Decides if this item should go into the item pool as a regular shuffled entry.

        Should be set to False for something like:
         - Items that we never want to have in the first place, like "Cloak Ball" or "Halt Gem"
         - Anything that gets a location via any other way, like Fillers, Traps or Djinns (for now)
        """
        return True

    def as_item(self) -> ItemData:
        return ItemData(
            id=self.ap_id,
            name=self.name,
            category=self.category,
            classification=self.classification,
            shuffled=self.shuffled,
            type=self.item_type,
        )

    @classmethod
    @abstractmethod
    def load(cls, *args: Any, **kwargs: Any) -> tuple[Self, ...]:
        """Every subclass should be able to decide itself where it comes from. Most get filled by data/*.json files."""


class BaseLocation(ABC):
    """
    Base class for all AP locations.

    See `BaseItem` docstring for more details on how these work.
    """

    _required_fields = ['ap_id', 'name', 'location_type', 'flag', 'rando_flag', 'restrictions']

    if TYPE_CHECKING:

        @property
        def ap_id(self) -> int: ...

        @property
        def name(self) -> str: ...

        @property
        def location_type(self) -> LocationType: ...

        @property
        def flag(self) -> int: ...

        @property
        def rando_flag(self) -> int: ...

        @property
        def restrictions(self) -> LocationRestriction: ...

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        _check_required_fields(cls)

    def as_location(self) -> LocationData:
        return LocationData(
            id=self.ap_id,
            name=self.name,
            type=self.location_type,
            flag=self.flag,
            rando_flag=self.rando_flag,
            restrictions=self.restrictions,
        )

    @classmethod
    @abstractmethod
    def load(cls, *args: Any, **kwargs: Any) -> tuple[Self, ...]:
        """Every subclass should be able to decide itself where it comes from. Most get filled by data/*.json files."""
