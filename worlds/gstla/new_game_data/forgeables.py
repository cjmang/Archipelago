from .base import read_json


def load_forge_mapping() -> dict[int, tuple[int, ...]]:
    """
    This just maps a forge material to the possible forgeable items:
        422 (Rusty Axe) -> (299 (Viking Axe),),
        437 (Orihalcon) -> (276 (Excalibur), 297 (Stellar Axe), ...),
    """
    raw_forge_map = read_json('data/forgeables.json')
    forge_mapping: dict[int, tuple[int, ...]] = {}

    for material_id, forge in raw_forge_map.items():
        for result_id in forge['results']:
            if result_id != 0:
                forge_mapping[int(material_id)] = tuple(result_id for result_id in forge['results'] if result_id != 0)

    return forge_mapping
