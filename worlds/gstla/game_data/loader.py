# TODO: rename to loader.py/game_loader.py/game_data.py/data_loader.py/main.py/index.py?

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING, TypeVar

import orjson

from .characters import Character
from .coins import Coins
from .djinns import Djinn, DjinnLocation
from .equipment import EquipmentItem
from .events import Event, EventLocation
from .items import VanillaItem
from .locations import ChestLocation
from .mimics import Mimic
from .psynergy import LearnedPsynergy, PsynergyItem
from .summons import Summon

if TYPE_CHECKING:
    from collections.abc import Mapping

    from worlds.gstla.gstla_types import ItemCategory, ItemData, LocationData, LocationType
    from .base import BaseItem, BaseLocation

RowT = TypeVar('RowT', bound='BaseItem | BaseLocation')


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

    # item_by_id and item_by_name are the things actually read by AP (probably want to rename to items_*)
    item_by_id: Mapping[int, ItemData]
    item_by_name: Mapping[str, ItemData]

    items_by_category: Mapping[ItemCategory, tuple[ItemData, ...]]

    chest_locations: Mapping[int, ChestLocation]
    djinn_locations: Mapping[int, DjinnLocation]
    event_locations: Mapping[int, EventLocation]

    # location_by_id/name exclude events so use event_by_name for those instead
    location_by_id: Mapping[int, LocationData]
    location_by_name: Mapping[str, LocationData]
    event_by_name: Mapping[str, LocationData]
    locations_by_type: Mapping[LocationType, tuple[LocationData, ...]]

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


def _get_rows_by_ap_id(rows: tuple[RowT, ...]) -> dict[int, RowT]:
    table = {row.ap_id: row for row in rows}
    if len(table) != len(rows):
        raise ValueError(f'Duplicate AP ids in {type(rows[0]).__name__}')
    return table


@cache
def load_game_data() -> GameData:
    tables = {
        'characters': _get_rows_by_ap_id(Character.load()),
        'coins': _get_rows_by_ap_id(Coins.load()),
        'djinn': _get_rows_by_ap_id(Djinn.load()),
        'equipment': _get_rows_by_ap_id(EquipmentItem.load()),
        'events': _get_rows_by_ap_id(Event.load()),
        'items': _get_rows_by_ap_id(VanillaItem.load()),
        'mimics': _get_rows_by_ap_id(Mimic.load()),
        'psynergy': _get_rows_by_ap_id(LearnedPsynergy.load()),
        'psynergy_items': _get_rows_by_ap_id(PsynergyItem.load()),
        'summons': _get_rows_by_ap_id(Summon.load()),
    }

    # Items
    item_by_id: dict[int, ItemData] = {}
    item_by_name: dict[str, ItemData] = {}
    items_by_category: defaultdict[ItemCategory, list[ItemData]] = defaultdict(list)
    for table in tables.values():
        for row in table.values():
            item = row.as_item()
            if item.id in item_by_id:
                raise ValueError(f'Duplicate ID {item.id=}: {item.name} vs {item_by_id[item.id].name}')
            if item.name in item_by_name:
                raise ValueError(f'Duplicate item name {item.name}: {item.id} vs {item_by_name[item.name].id}')
            item_by_id[item.id] = item
            item_by_name[item.name] = item
            items_by_category[item.category].append(item)

    # Locations
    chest_locations = _get_rows_by_ap_id(ChestLocation.load())
    djinn_locations = _get_rows_by_ap_id(DjinnLocation.load())
    event_locations = _get_rows_by_ap_id(EventLocation.load())

    location_by_id: dict[int, LocationData] = {}
    location_by_name: dict[str, LocationData] = {}
    event_by_name: dict[str, LocationData] = {}
    locations_by_type: defaultdict[LocationType, list[LocationData]] = defaultdict(list)
    for row in (*chest_locations.values(), *djinn_locations.values(), *event_locations.values()):
        location = row.as_location()
        if location.id in location_by_id:
            raise ValueError(f'Duplicate location ID {location.id=}: {location.name}')
        if location.name in location_by_name or location.name in event_by_name:
            raise ValueError(f'Duplicate location name {location.name}: {location.id}')
        if isinstance(row, EventLocation):
            event_by_name[location.name] = location
        else:
            location_by_id[location.id] = location
            location_by_name[location.name] = location
        locations_by_type[location.type].append(location)

    return GameData(
        # TODO: actually use the now registered locations
        **tables,
        item_by_id=item_by_id,
        item_by_name=item_by_name,
        items_by_category={category: tuple(items) for category, items in items_by_category.items()},
        location_by_id=location_by_id,
        location_by_name=location_by_name,
        event_by_name=event_by_name,
        chest_locations=chest_locations,
        djinn_locations=djinn_locations,
        event_locations=event_locations,
        locations_by_type={loc_type: tuple(locs) for loc_type, locs in locations_by_type.items()},
    )
