# TODO: rename to loader.py/game_loader.py/game_data.py/data_loader.py/main.py/index.py?

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

import orjson

from .characters import Character
from .coins import Coins
from .djinns import Djinn
from .equipment import EquipmentItem
from .events import Event
from .items import VanillaItem
from .mimics import Mimic
from .psynergy import LearnedPsynergy, PsynergyItem
from .summons import Summon

if TYPE_CHECKING:
    from collections.abc import Mapping

    from worlds.gstla.gstla_types import ItemData
    from .base import BaseItem


@dataclass(frozen=True, slots=True, kw_only=True)
class GameData:
    characters: Mapping[int, Character]
    coins: Mapping[int, Coins]
    djinn: Mapping[int, Djinn]
    equipment: Mapping[int, EquipmentItem]
    events: Mapping[int, Event]
    items: Mapping[int, VanillaItem]
    mimics: Mapping[int, Mimic]
    psynergy: Mapping[int, LearnedPsynergy]
    psynergy_items: Mapping[int, PsynergyItem]
    summons: Mapping[int, Summon]

    # item_by_id and item_by_name are the things actually read by AP
    item_by_id: Mapping[int, ItemData]
    item_by_name: Mapping[str, ItemData]

    def dump_by_id(self):
        # TODO: classification flag into str?
        data = orjson.dumps(
            self.item_by_id, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS | orjson.OPT_NON_STR_KEYS
        )
        # print(data.decode())
        return data.decode()

    def dump_by_name(self):
        data = orjson.dumps(
            self.item_by_name, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS | orjson.OPT_NON_STR_KEYS
        )
        # print(data.decode())
        return data.decode()


def _get_items_by_ap_id(rows: tuple[BaseItem, ...]) -> dict[int, BaseItem]:
    table = {row.ap_id: row for row in rows}
    if len(table) != len(rows):
        raise ValueError(f'Duplicate AP ids in {type(rows[0]).__name__}')
    return table


@cache
def load_game_data() -> GameData:
    tables = {
        'characters': _get_items_by_ap_id(Character.load()),
        'coins': _get_items_by_ap_id(Coins.load()),
        'djinn': _get_items_by_ap_id(Djinn.load()),
        'equipment': _get_items_by_ap_id(EquipmentItem.load()),
        'events': _get_items_by_ap_id(Event.load()),
        'items': _get_items_by_ap_id(VanillaItem.load()),
        'mimics': _get_items_by_ap_id(Mimic.load()),
        'psynergy': _get_items_by_ap_id(LearnedPsynergy.load()),
        'psynergy_items': _get_items_by_ap_id(PsynergyItem.load()),
        'summons': _get_items_by_ap_id(Summon.load()),
    }

    item_by_id: dict[int, ItemData] = {}
    item_by_name: dict[str, ItemData] = {}
    for table in tables.values():
        for row in table.values():
            item = row.as_item()
            if item.id in item_by_id:
                raise ValueError(f'Duplicate ID {item.id=}: {item.name} vs {item_by_id[item.id].name}')
            if item.name in item_by_name:
                raise ValueError(f'Duplicate item name {item.name}: {item.id} vs {item_by_name[item.name].id}')
            item_by_id[item.id] = item
            item_by_name[item.name] = item

    return GameData(
        **tables,
        item_by_id=item_by_id,
        item_by_name=item_by_name,
    )
