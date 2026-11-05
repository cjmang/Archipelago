from __future__ import annotations

import os
from collections import defaultdict
from typing import TextIO

from jinja2 import Environment, PackageLoader, select_autoescape

from .game_data import GameData
from .gstla_types import ElementType

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))


def main():
    env = Environment(loader=PackageLoader('gen'), autoescape=select_autoescape())
    env.filters['bitwise_and'] = lambda x, y: x & y > 0
    data = GameData()
    generate_location_names(env, data)
    generate_location_data(env, data)


def generate_location_names(env: Environment, data: GameData):
    template = env.get_template('location_names.py.jinja')
    hidden_items = []
    key_items = []
    summon_tablets = []
    major_items = []
    remainder = []
    earth_djinn = []
    water_djinn = []
    fire_djinn = []
    air_djinn = []
    events = []
    name_list = []

    for djinn in data.raw_djinn_data:
        # d = {'key': djinn.name, 'value': djinn.name}
        if djinn.element == ElementType.Earth:
            earth_djinn.append(djinn)
        elif djinn.element == ElementType.Water:
            water_djinn.append(djinn)
        elif djinn.element == ElementType.Fire:
            fire_djinn.append(djinn)
        elif djinn.element == ElementType.Air:
            air_djinn.append(djinn)
        name_list.append({'name': djinn.name, 'id': djinn.ap_id})
    for event in data.events.values():
        events.append(data.location_names[event.event_id])
        name_list.append({'name': data.location_names[event.event_id].py_name, 'id': event.event_id})
    for loc_datum in data.raw_location_data:
        loc_name = data.location_names[loc_datum.id]
        name_list.append({'name': loc_name.py_name, 'id': loc_datum.addr[0]})
        if loc_datum.is_summon:
            summon_tablets.append(loc_name)
        elif loc_datum.is_key_item:
            key_items.append(loc_name)
        elif loc_datum.is_major_item:
            major_items.append(loc_name)
        elif loc_datum.is_hidden:
            hidden_items.append(loc_name)
        else:
            remainder.append(loc_name)

    with open(os.path.join(SCRIPT_DIR, 'gen', 'internal_location_names.py'), 'w') as outfile:
        write_warning(outfile)
        outfile.write(
            template.render(
                hiddenItems=hidden_items,
                keyItems=key_items,
                summonTablets=summon_tablets,
                majorItems=major_items,
                remainder=remainder,
                earthDjinn=earth_djinn,
                waterDjinn=water_djinn,
                fireDjinn=fire_djinn,
                airDjinn=air_djinn,
                events=events,
                name_list=name_list,
            )
        )


def generate_location_data(env: Environment, data: GameData):
    template = env.get_template('location_data.py.jinja')
    with open(os.path.join(SCRIPT_DIR, 'gen', 'internal_location_data.py'), 'w') as outfile:
        write_warning(outfile)
        loc_data = data.raw_location_data
        psy_ids = {psy.id for psy in data.raw_psy_data}
        djinn_locs = data.raw_djinn_data
        summons_loc = []
        psy_locs = []
        remainder = []
        for loc in loc_data:
            if loc.is_summon:
                summons_loc.append(loc)
            elif loc.vanilla_contents in psy_ids:
                psy_locs.append(loc)
            else:
                remainder.append(loc)
        loc_type_lookup: defaultdict[int, str] = defaultdict(
            lambda: 'Item',
            {
                2722: 'Trade',  # Pretty Stone
                2724: 'Trade',  # Red Cloth
                2723: 'Trade',  # Milk
                2721: 'Trade',  # Li'l Turtle
                3328: 'Character',  # Contigo Isaac
                3329: 'Character',  # Contigo Garet
                3330: 'Character',  # Contigo Ivan
                3331: 'Character',  # Contigo Mia
                3333: 'Character',  # Idejima Jenna
                3334: 'Character',  # Idejima Sheba
                3335: 'Character',  # Kibombo Piers
            },
        )
        for loc in remainder:
            if loc.is_hidden:
                loc_type_lookup[loc.id] = 'Hidden'
        outfile.write(
            template.render(
                summon_locations=summons_loc,
                psyenergy_locations=psy_locs,
                djinn_locations=djinn_locs,
                other_locations=remainder,
                events=data.events.values(),
                loc_type_lookup=loc_type_lookup,
            )
        )


def write_warning(fp: TextIO):
    fp.write(
        """# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
"""
    )


#

if __name__ == '__main__':
    main()
