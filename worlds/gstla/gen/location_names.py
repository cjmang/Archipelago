from worlds.gstla.names import LocationName
from .internal_location_names import ids_by_py_name

ids_by_loc_name: dict[str, int] = {getattr(LocationName, key): value for key, value in ids_by_py_name.items()}

loc_names_by_id: dict[int, str] = {value: key for key, value in ids_by_loc_name.items()}

option_name_to_goal_name = {
    'Chestbeaters': LocationName.Kandorean_Temple_Chestbeaters,
    'King Scorpion': LocationName.Yampi_Desert_King_Scorpion,
    'Briggs': LocationName.Alhafra_Briggs,
    'Aqua Hydra': LocationName.Lemurian_Ship_Aqua_Hydra,
    'Poseidon': LocationName.Sea_of_Time_Poseidon,
    'Serpent': LocationName.Gaia_Rock_Serpent,
    'Avimander': LocationName.Champa_Avimander,
    'Moapa': LocationName.Shaman_Village_Moapa,
    'Reunion': LocationName.Contigo_Reunion,
    'Flame Dragons': LocationName.Mars_Lighthouse_Flame_Dragons,
    'Doom Dragon': LocationName.Mars_Lighthouse_Doom_Dragon,
    'Star Magician': LocationName.Treasure_Isle_Star_Magician,
    'Sentinel': LocationName.Islet_Cave_Sentinel,
    'Valukar': LocationName.Yampi_Desert_Cave_Valukar,
    'Dullahan': LocationName.Anemos_Inner_Sanctum_Dullahan,
}
