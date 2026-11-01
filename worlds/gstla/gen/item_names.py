from worlds.gstla.names.item_name import ItemName
from .internal_item_names import item_id_by_py_name

item_id_by_name: dict[str, int] = {getattr(ItemName, key): value for key, value in item_id_by_py_name.items()}
# Special case for empty item
item_id_by_name['Empty'] = 0

name_by_item_id: dict[int, str] = {value: key for key, value in item_id_by_name.items()}
