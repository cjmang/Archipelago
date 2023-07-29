from worlds.AutoWorld import WebWorld, World
import os

from typing import List

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType
from .Locations import GSTLALocation, all_locations, location_name_to_id, LocationType
from .Rules import set_access_rules, set_item_rules
from .Regions import create_regions
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName
from .Rom import get_base_rom_path, get_base_rom_bytes, LocalRom, GSTLADeltaPatch


class GSTLAWeb(WebWorld):
    theme = "jungle"


class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    option_definitions = GSTLAOptions
    data_version = 1
    djinnlist = []

    item_name_to_id = {item.itemName: item.ap_id for item in all_items}
    location_name_to_id = {location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn: { "Echo", "Fog", "Breath", "Iron", "Cannon" },
        "venus_djinn": {},
        "mercury_djinn": {},
        "mars_djinn": {},
        "jupiter_djinn": {}
    }

    cyclonechip = []


    def generate_early(self) -> None:
        pass


    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)


    def create_items(self) -> None:
        for item in all_items:
            for _ in range(item.quantity):
                ap_item = self.create_item(item.itemName)
                if item.type == ItemType.Djinn:
                    self.djinnlist.append(ap_item)
                elif item.itemName == ItemName.Cyclone_Chip:
                    self.cyclonechip.append(ap_item)
                else:
                    self.multiworld.itempool.append(self.create_item(item.itemName))


    def set_rules(self) -> None:
        set_item_rules(self.multiworld, self.player)
        set_access_rules(self.multiworld, self.player)

        self.multiworld.get_location(LocationName.DoomDragonDefeated, self.player) \
            .place_locked_item(self.create_event(ItemName.Victory))

        self.multiworld.get_location(LocationName.DefeatChestBeaters, self.player) \
            .place_locked_item(self.create_event("DefeatChestbeaters"))

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_basic(self):
        pass

    def get_pre_fill_items(self) -> List["Item"]:
        return self.djinnlist

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError
        all_state = self.multiworld.get_all_state(use_cache=False)
        locs = []
        #Todo: replace this with a list of djinn locations and fill them up with djinn items
        locs.append( self.multiworld.get_location("Echo", self.player))
        locs.append( self.multiworld.get_location("Fog", self.player))
        locs.append( self.multiworld.get_location("Breath", self.player))
        locs.append( self.multiworld.get_location("Iron", self.player))
        locs.append( self.multiworld.get_location("Cannon", self.player))

        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(self.djinnlist)

        for ap_item in self.djinnlist:
            all_state.remove(ap_item)

        all_state.remove(self.cyclonechip[0])

        fill_restrictive(self.multiworld, all_state, locs, self.djinnlist, True, True)

        fill_restrictive(self.multiworld, all_state, [self.multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, self.player)], self.cyclonechip, True, True)

    def generate_output(self, output_directory: str):
        rom = LocalRom(get_base_rom_path())
        world = self.multiworld
        player = self.player

        locations = location_name_to_id
        for location in locations:
            ap_location = world.get_location(location, player)
            location_data = location_name_to_id[location]
            ap_item = ap_location.item

            item_data = item_table[ap_item.name]
            if item_data.type == ItemType.Djinn:
                rom.write_djinn(location_data, item_data)
            else:
                rom.write_item(location_data, item_data)

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gba")

        try:

            patch = GSTLADeltaPatch(os.path.splitext(rompath)[0]+GSTLADeltaPatch.patch_file_ending, player=player,
                                    player_name=world.player_name[player], patched_path=rompath)
            rom.write_to_file(rompath)
            patch.write()
        except:
            raise()
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

        #for testing in case delta patch fails
        rom.write_to_file('C:/Users/Gebruiker/Desktop/GameDev/GsTlaAp/GsArchipelago/output/gstla_patched.gba')


    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        return GSTLAItem(item.itemName, item.progression, item.ap_id, self.player)


    def create_event(self, event: str):
        return GSTLAItem(event, ItemClassification.progression, None, self.player)