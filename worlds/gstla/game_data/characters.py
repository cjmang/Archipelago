from abc import abstractmethod
from typing import Any, Self

from worlds.gstla.gstla_types import ItemData
from .base import BaseItem


class Character(BaseItem):
    # ITEM_TYPE =

    index: int  # replace with the CharacterIndex enum after deathlink merge
    name: str
    flag: int
    addr: int

    @property
    def ap_id(self) -> int:  # 0xD00 + index
        pass

    def as_item(self) -> ItemData:
        pass

    # @classmethod
    # def load(cls, ...):