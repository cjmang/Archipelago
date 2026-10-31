from abc import ABC, abstractmethod
from typing import Any, ClassVar, Self

from BaseClasses import ItemClassification
from worlds.gstla.gstla_types import ItemCategory, ItemData, ItemType


class BaseItem(ABC):
    # TODO: classvars here should probably be validated, gotta use __init_subclass__ or something iirc
    ITEM_TYPE: ClassVar[ItemType]
    CLASSIFICATION: ClassVar[ItemClassification]
    CATEGORY: ClassVar[ItemCategory]

    ap_id: int
    name: str

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
