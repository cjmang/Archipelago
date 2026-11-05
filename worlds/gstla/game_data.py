import json
import os
from collections import defaultdict
from typing import Any, NamedTuple

from .gstla_types import ElementType, ItemType

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

num_words = {
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five',
    6: 'Six',
    7: 'Seven',
    8: 'Eight',
    9: 'Nine',
    10: 'Ten',
}


class LocationDatum(NamedTuple):
    rando_flag: int
    flag: int
    map_id: int
    locked: bool
    is_summon: bool
    is_key_item: bool
    is_major_item: bool
    is_hidden: bool
    addr: list[int]
    event_type: int
    location_id: int
    id: int
    vanilla_contents: int
    vanilla_name: str
    map_name: str
    restrictions: int


class EnemyDatum(NamedTuple):
    name: str
    id: int
    ap_id: int
    flag: int


class EventDatum(NamedTuple):
    event_id: int
    flag: int
    location_name: str
    item_name: str


class DjinnDatum(NamedTuple):
    ap_id: int
    id: int
    element: ElementType
    name: str
    addr: int
    stats_addr: int
    stats: list[int]
    vanilla_flag: int
    item_type: ItemType = ItemType.Djinn


class PsyDatum(NamedTuple):
    id: int
    name: str
    addr: int
    item_type: ItemType = ItemType.Psynergy


class LocationName(NamedTuple):
    id: int
    flag: int
    py_name: str
    str_name: str

    @classmethod
    def from_loc_data(cls, loc: LocationDatum, value: str = None, suffix: str = ''):
        key = loc.map_name
        val = loc.vanilla_name + suffix
        py_name = key.replace(' ', '_').replace("'", '')
        str_name = val.replace(' ', '_').replace("'", '').replace('???', 'Empty')
        if value is None:
            return LocationName(loc.id, loc.flag, py_name + '_' + str_name, py_name + ' - ' + str_name)
        return LocationName(loc.id, loc.flag, py_name + '_' + str_name, value)


class GameData:
    def __init__(self):
        self.raw_location_data: list[LocationDatum] = []
        self.raw_djinn_data: list[DjinnDatum] = []
        self.raw_psy_data: list[PsyDatum] = []
        # self.raw_enemy_data: list[EnemyDatum] = []
        self.location_names: dict[int, LocationName] = {}
        self.events: dict[int, EventDatum] = {}
        self._load_locations()
        self._load_djinn()
        self._setup_events()
        self._setup_location_names()
        self._setup_psy_energies()

    def _load_locations(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'item_locations.json'), 'r') as loc_file:
            location_data = json.load(loc_file)
        # A few locations use different flags than stated in the item_locations.json file
        # E.g. character starting inventories
        flag_overwrites = {
            16384202: 0x4,  # Shaman's Rod -> Felix
            16384204: 0x6,  # Mind Read -> Sheba
            16384206: 0x6,  # Whirlwind -> Sheba
            16384208: 0x4,  # Growth -> Felix
            16384210: 0x3,  # Carry Stone -> Mia
            16384212: 0x2,  # Lifting Gem -> Ivan
            16384214: 0x1,  # Orb of Force -> Garet
            16384216: 0x0,  # Catch Beads -> Isaac
            16384218: 0x7,  # Douse Drop -> Piers
            16384220: 0x7,  # Frost Jewel -> Piers
        }
        restriction_map = {'no-empty': 1, 'no-mimic': 2, 'no-summon': 4, 'no-money': 8}
        restriction_dict: defaultdict[int, int] = defaultdict(lambda: 0)
        for loc_logic_file in os.listdir(os.path.join(SCRIPT_DIR, 'data', 'location_logic')):
            assert loc_logic_file.endswith('.json')
            with open(os.path.join(SCRIPT_DIR, 'data', 'location_logic', loc_logic_file), 'r') as data_file:
                data = json.load(data_file)

            treasure_data = data['Treasure']
            for datum in treasure_data:
                if 'Restriction' not in datum:
                    continue
                restrictions = datum['Restriction']
                addr = int(datum['Addr'], 16)
                assert addr not in restriction_dict
                for restriction in restrictions:
                    restriction_dict[addr] += restriction_map[restriction]

        for flag, locs in location_data.items():
            # The extra locations are variations on the same map.  We mostly don't care for the client,
            # but the rom generator currently does care, since it will need to place the same item on all
            # variations of the map
            loc = locs[0]
            addr = [x['addr'] for x in locs]
            rando_flag = int(flag, 16)
            mapped_flag = flag_overwrites.get(addr[0], rando_flag)
            restriction_data = restriction_dict[loc['id']]
            if loc['eventType'] != 0x80 and loc['eventType'] != 0x84:
                restriction_data |= restriction_map['no-empty'] + restriction_map['no-mimic']
            if addr[0] > 0xFA0000:
                restriction_data |= restriction_map['no-money']
            if loc['id'] < 0x10 or (loc['id'] | 0xF00) == 0x100:
                restriction_data |= (
                    restriction_map['no-empty'] + restriction_map['no-mimic'] + restriction_map['no-money']
                )
            datum = LocationDatum(
                rando_flag,
                mapped_flag,
                loc['mapId'],
                loc['locked'],
                loc['isSummon'],
                loc['isKeyItem'],
                loc['isMajorItem'],
                loc['isHidden'],
                addr,
                loc['eventType'],
                loc['locationId'],
                loc['id'],
                loc['vanillaContents'],
                loc['vanillaName'],
                loc['mapName'],
                restriction_data,
            )
            self.raw_location_data.append(datum)

    def _load_djinn(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'djinn.json'), 'r') as djinn_file:
            djinn_data = json.load(djinn_file)
        for djinn in djinn_data:
            # Largest vanilla item id is 460
            self.raw_djinn_data.append(
                DjinnDatum(
                    ap_id=djinn['addr'],
                    id=djinn['vanillaId'],
                    element=ElementType(djinn['vanillaElement']),
                    name=djinn['vanillaName'],
                    addr=djinn['addr'],
                    # From emo tracker pack
                    stats_addr=djinn['statAddr'],
                    stats=djinn['stats'],
                    # 0x30 is the start of the djinn flags; the game has flag slots for 20 djinn
                    # per element, even though there's only 18 per element, so some flags are just unused
                    vanilla_flag=0x30 + (djinn['vanillaElement'] * 20) + djinn['vanillaId'],
                )
            )

    def _load_enemies(self):
        """
        # TODO: Migrate to a dataclass in (new_)game_data/enemies.py
        # Function is unused, but leaving here in case we actually want to use it for some reason
        enemy_offset = 6000
        with open(os.path.join(SCRIPT_DIR, 'data', 'enemies.json'), 'r') as enemy_file:
            enemy_data = json.load(enemy_file)
            for name, list in enemy_data.items():
                if name == '???':
                    continue
                for enemy in list:
                    self.raw_enemy_data.append(
                        # Enemy kill flags start at 0x600; the flag is off by 7 sorta; -1 for the json
                        # starting at 1 instead of 0, and + 8 for player characters
                        EnemyDatum(
                            enemy['name'], enemy['id'] - 1, enemy['id'] + enemy_offset, enemy['id'] - 1 + 8 + 0x600
                        )
                    )

        for enemy in self.raw_enemy_data:
            name = ItemName.from_enemy_data(enemy)
            self.item_names[enemy.ap_id] = name
            self.location_names[enemy.ap_id] = LocationName(enemy.ap_id, enemy.flag, name.py_name, name.str_name)
        """

    def _recurse_tracker_data(
        self, tracker_name_data: dict[int, str], tracker_names: dict[str, int], node: dict[str, Any]
    ) -> None:
        if 'sections' not in node:
            if 'children' in node:
                for child in node['children']:
                    self._recurse_tracker_data(tracker_name_data, tracker_names, child)
            return
        sections = node['sections']
        area_name = node['name']
        for i in range(len(sections)):
            section = sections[i]
            flags = node['children'][i]['name']
            for flag_str in flags.split(','):
                flag = int(flag_str, 16)
                if flag in tracker_name_data:
                    continue
                tracker_name = f'{area_name} - {section["name"]}'
                # count = names[tracker_name] + 1
                tracker_names[tracker_name] += 1
                count = tracker_names[tracker_name]
                suffix = ''
                if count > 1:
                    suffix = ' ' + num_words[count]
                tracker_name_data[flag] = tracker_name + suffix

    def _setup_location_names(self):
        names: defaultdict[str, int] = defaultdict(lambda: 0)
        tracker_name_data: dict[int, str] = {}
        tracker_names: defaultdict[str, int] = defaultdict(lambda: 0)
        with open(os.path.join(SCRIPT_DIR, 'data', 'locations.json')) as infile:
            tracker_data = json.load(infile)[0]
        self._recurse_tracker_data(tracker_name_data, tracker_names, tracker_data)
        for loc in self.raw_location_data:
            tracker_name = tracker_name_data.get(loc.rando_flag)
            # tracker_name = None
            if tracker_name is not None:
                loc_name = LocationName.from_loc_data(loc, tracker_name)
            else:
                loc_name = LocationName.from_loc_data(loc)
            count = names[loc_name.py_name] + 1
            names[loc_name.py_name] = count
            if count > 1:
                if tracker_name is not None:
                    loc_name = LocationName.from_loc_data(loc, tracker_name, ' ' + num_words[count])
                else:
                    loc_name = LocationName.from_loc_data(loc, None, ' ' + num_words[count])
                # loc_name = LocationName.from_loc_data(loc, None, ' ' + num_words[count])
            assert loc_name.id not in self.location_names, f'{hex(loc_name.id)=}, {loc_name.str_name=}'
            self.location_names[loc_name.id] = loc_name

    def _setup_psy_energies(self):
        self.raw_psy_data += [
            PsyDatum(3596, 'Growth', 3596),
            PsyDatum(3662, 'Whirlwind', 3662),
            PsyDatum(3722, 'Parch', 3722),
            PsyDatum(3723, 'Sand', 3723),
            PsyDatum(3725, 'Mind Read', 3725),
            PsyDatum(3728, 'Reveal', 3728),
            PsyDatum(3738, 'Blaze', 3738),
        ]

    def _setup_events(self):
        # Just some offset to avoid colliding with anything else; needs to avoid any location or item ids in AP
        event_offset = 5000
        events = [  # TODO: move to game_data/events.py, dedup
            EventDatum(event_offset + 1, 0x778, 'Mars Lighthouse - Doom Dragon', 'Doom Dragon Defeated'),
            EventDatum(event_offset + 2, 0x8AB, 'Alhafra Briggs', 'Briggs defeated'),
            EventDatum(event_offset + 3, 0x97F, 'Alhafra Prison Briggs', 'Briggs escaped'),
            EventDatum(event_offset + 4, 0x8FF, 'Gabomba Statue Ritual', 'Gabomba Statue Completed'),
            EventDatum(event_offset + 5, 0x9EE, 'Gaia Rock - Serpent', 'Serpent defeated'),
            EventDatum(event_offset + 6, 0x665, 'Sea of Time - Poseidon', 'Poseidon defeated'),
            EventDatum(event_offset + 7, 0x93F, 'Lemurian Ship - Aqua Hydra', 'Aqua Hydra defeated'),
            EventDatum(event_offset + 8, 0x94D, 'Shaman Village - Moapa', 'Moapa defeated'),
            EventDatum(event_offset + 9, 0xA21, 'Jupiter_Lighthouse Aeri - Agatio and Karst', 'Jupiter Beacon Lit'),
            EventDatum(event_offset + 10, 0xA4B, 'Mars Lighthouse - Flame Dragons', 'Flame Dragons - defeated'),
            EventDatum(event_offset + 11, 0x8DE, 'Lemurian Ship - Engine Room', 'Ship'),
            EventDatum(event_offset + 12, 0x8DF, 'Contigo - Wings of Anemos', 'Wings of Anemos'),
            EventDatum(event_offset + 13, 0x64A, 'Kandorean Temple - Chestbeaters', 'Chestbeaters defeated'),
            EventDatum(event_offset + 14, 0x64D, 'Yampi Desert - King Scorpion', 'King Scorpion defeated'),
            EventDatum(event_offset + 15, 0x662, 'Champa - Avimander', 'Avimander defeated'),
            EventDatum(event_offset + 16, 0x6A4, 'Treasure Isle - Star Magician', 'Star Magician defeated'),
            EventDatum(event_offset + 17, 0x6DD, 'Islet Cave - Sentinel', 'Sentinel defeated'),
            EventDatum(event_offset + 18, 0x6D1, 'Yampi Desert Cave - Valukar', 'Valukar defeated'),
            EventDatum(event_offset + 19, 0x6DA, 'Anemos Inner Sanctum - Dullahan', 'Dullahan defeated'),
            # Flag here is really the Jupiter Lighthouse flag.  Base rando with PC shuffle seems to do something weird
            # with the reunion flag
            EventDatum(event_offset + 20, 0xA21, 'Contigo - Reunion', 'Reunion'),
            EventDatum(event_offset + 21, 0x1, 'Victory Event', 'Victory'),
            EventDatum(event_offset + 22, 0xA5F, 'Loho - Ship Cannon', 'Ship Cannon'),
            EventDatum(event_offset + 23, 0xA30, 'Mars Lighthouse - Heated', 'Mars Lighthouse Heated'),
            # EventDatum(event_offset + 15,, "Jupiter Lighthouse - Karst", "Karst defeated"),
            # EventDatum(event_offset + 15,, "Jupiter Lighthouse - Agatio", "Agatio defeated"),
        ]
        self.events = {e.event_id: e for e in events}
        for event in self.events.values():
            self.location_names[event.event_id] = LocationName(
                event.event_id,
                event.flag,
                event.location_name.replace(' ', '_').replace('-', '').replace('__', '_'),
                event.location_name,
            )
