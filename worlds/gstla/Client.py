# import asyncio
# import hashlib
# import json
# import os
# import multiprocessing
# import subprocess
# import zipfile
#
# from asyncio import StreamReader, StreamWriter
#
# import bsdiff4
#
# from CommonClient import CommonContext, server_loop, gui_enabled, \
#     ClientCommandProcessor, logger, get_base_parser
# import Utils
# from NetUtils import ClientStatus
# from worlds.gstla.Items import items_by_id
# from worlds.gstla.Rom import get_base_rom_path
# from worlds.gstla.Locations import all_locations
#
# SYSTEM_MESSAGE_ID = 0
#
# CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_GS23.lua"
# CONNECTION_REFUSED_STATUS = \
#     "Connection refused. Please start your emulator and make sure connector_GS23.lua is running"
# CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_GS23.lua"
# CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
# CONNECTION_CONNECTED_STATUS = "Connected"
# CONNECTION_INITIAL_STATUS = "Connection has not been initiated"
# CONNECTION_INCORRECT_ROM = "Supplied Base Rom does not match US GBA Blue Version. Please provide the correct ROM version"
#
# script_version: int = 2
#
# debugEnabled = False
# locations_checked = []
# items_sent = []
# itemIndex = 1
#
# CHECKSUM_BLUE = "8efe8b2aaed97149e897570cd123ff6e"
#
#
# class GS2CommandProcessor(ClientCommandProcessor):
#     def __init__(self, ctx):
#         super().__init__(ctx)
#
#     def _cmd_gba(self):
#         """Check GBA Connection State"""
#         if isinstance(self.ctx, GS2Context):
#             logger.info(f"GBA Status: {self.ctx.gba_status}")
#
#     def _cmd_debug(self):
#         """Toggle the Debug Text overlay in ROM"""
#         global debugEnabled
#         debugEnabled = not debugEnabled
#         logger.info("Debug Overlay Enabled" if debugEnabled else "Debug Overlay Disabled")
#
#
# class GS2Context(CommonContext):
#     command_processor = GS2CommandProcessor
#     game = "Golden Sun: The Lost Age"
#     items_handling = 0b001  # full local
#
#     def __init__(self, server_address, password):
#         super().__init__(server_address, password)
#         self.gba_streams: (StreamReader, StreamWriter) = None
#         self.gba_sync_task = None
#         self.gba_status = CONNECTION_INITIAL_STATUS
#         self.awaiting_rom = False
#         self.location_table = {}
#         self.version_warning = False
#         self.auth_name = None
#         self.slot_data = dict()
#         self.patching_error = False
#
#     async def server_auth(self, password_requested: bool = False):
#         if password_requested and not self.password:
#             await super(GS2Context, self).server_auth(password_requested)
#
#         if self.auth_name is None:
#             self.awaiting_rom = True
#             logger.info("No ROM detected, awaiting conection to Bizhawk to authenticate to the multiworld server")
#             return
#
#         logger.info("Attempting to decode from ROM... ")
#         self.awaiting_rom = False
#         self.auth = self.auth_name.decode("utf8").replace('\x00', '')
#         logger.info("Connecting as "+self.auth)
#         await self.send_connect(name=self.auth)
#
#     def run_gui(self):
#         from kvui import GameManager
#
#         class GS2Manager(GameManager):
#             logging_pairs = [
#                 ("Client", "Archipelago")
#             ]
#             base_title = "Archipelago Golden Sun: The Lost Age Client"
#
#         self.ui = GS2Manager(self)
#         self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
#
#     def on_package(self, cmd: str, args: dict):
#         if cmd == 'Connected':
#             self.slot_data = args.get("slot_data", {})
#             print(self.slot_data)
#
# class ItemInfo:
#     id = 0x00
#     sender = ""
#     type = ""
#     count = 1
#     itemName = "Unknown"
#     itemID = 0x00  # Item ID, Chip ID, etc.
#     subItemID = 0x00  # Code for chips, color for programs
#     itemIndex = 1
#
#     def __init__(self, id, sender, type):
#         self.id = id
#         self.sender = sender
#         self.type = type
#
#     def get_json(self):
#         json_data = {
#             "id": self.id,
#             "sender": self.sender,
#             "type": self.type,
#             "itemName": self.itemName,
#             "itemID": self.itemID,
#             "subItemID": self.subItemID,
#             "count": self.count,
#             "itemIndex": self.itemIndex
#         }
#         return json_data
#
#
# def get_payload(ctx: GS2Context):
#     global debugEnabled
#
#     items_sent = []
#     for i, item in enumerate(ctx.items_received):
#         item_data = items_by_id[item.item]
#         new_item = ItemInfo(i, ctx.player_names[item.player], item_data.type)
#         new_item.itemIndex = i+1
#         new_item.itemName = item_data.itemName
#         new_item.type = item_data.type
#         new_item.itemID = item_data.itemID
#         new_item.subItemID = item_data.subItemID
#         new_item.count = item_data.count
#         items_sent.append(new_item)
#
#     return json.dumps({
#         "items": [item.get_json() for item in items_sent],
#         "debug": debugEnabled
#         })
#
#
# async def parse_payload(payload: dict, ctx: GS2Context, force: bool):
#     # Game completion handling
#     if payload["gameComplete"] and not ctx.finished_game:
#         await ctx.send_msgs([{
#             "cmd": "StatusUpdate",
#             "status": ClientStatus.CLIENT_GOAL
#         }])
#         ctx.finished_game = True
#
#     # Locations handling
#     if ctx.location_table != payload["locations"]:
#         ctx.location_table = payload["locations"]
#         locs = [loc.id for loc in all_locations
#                 if check_location_packet(loc, ctx.location_table)]
#         await ctx.send_msgs([{
#             "cmd": "LocationChecks",
#             "locations": locs
#         }])
#
#
# def check_location_packet(location, memory):
#     if len(memory) == 0:
#         return False
#     # Our keys have to be strings to come through the JSON lua plugin so we have to turn our memory address into a string as well
#     location_key = hex(location.flag_byte)[2:]
#     byte = memory.get(location_key)
#     if byte is not None:
#         return byte & location.flag_mask
#
#
# def check_location_scouted(location, memory):
#     if len(memory) == 0:
#         return False
#     location_key = hex(location.hint_flag)[2:]
#     byte = memory.get(location_key)
#     if byte is not None:
#         return byte & location.hint_flag_mask
#
#
# async def gba_sync_task(ctx: GS2Context):
#     logger.info("Starting GBA connector. Use /gba for status information.")
#     if ctx.patching_error:
#         logger.error('Unable to Patch ROM. No ROM provided or ROM does not match Golden Sun The Lost Age Version.')
#     while not ctx.exit_event.is_set():
#         error_status = None
#         if ctx.gba_streams:
#             (reader, writer) = ctx.gba_streams
#             msg = get_payload(ctx).encode()
#             writer.write(msg)
#             writer.write(b'\n')
#             try:
#                 await asyncio.wait_for(writer.drain(), timeout=1.5)
#                 try:
#                     # Data will return a dict with up to four fields
#                     # 1. str: player name (always)
#                     # 2. int: script version (always)
#                     # 3. dict[str, byte]: value of location's memory byte
#                     # 4. bool: whether the game currently registers as complete
#                     data = await asyncio.wait_for(reader.readline(), timeout=10)
#                     data_decoded = json.loads(data.decode())
#                     reported_version = data_decoded.get("scriptVersion", 0)
#                     if reported_version >= script_version:
#                         if ctx.game is not None and "locations" in data_decoded:
#                             # Not just a keep alive ping, parse
#                             asyncio.create_task((parse_payload(data_decoded, ctx, False)))
#                         if not ctx.auth:
#                             ctx.auth_name = bytes(data_decoded["playerName"])
#
#                             if ctx.awaiting_rom:
#                                 logger.info("Awaiting data from ROM...")
#                                 await ctx.server_auth(False)
#                     else:
#                         if not ctx.version_warning:
#                             logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}."
#                                            "Please update to the latest version."
#                                            "Your connection to the Archipelago server will not be accepted.")
#                             ctx.version_warning = True
#                 except asyncio.TimeoutError:
#                     logger.debug("Read Timed Out, Reconnecting")
#                     error_status = CONNECTION_TIMING_OUT_STATUS
#                     writer.close()
#                     ctx.gba_streams = None
#                 except ConnectionResetError:
#                     logger.debug("Read failed due to Connection Lost, Reconnecting")
#                     error_status = CONNECTION_RESET_STATUS
#                     writer.close()
#                     ctx.gba_streams = None
#             except TimeoutError:
#                 logger.debug("Connection Timed Out, Reconnecting")
#                 error_status = CONNECTION_TIMING_OUT_STATUS
#                 writer.close()
#                 ctx.gba_streams = None
#             except ConnectionResetError:
#                 logger.debug("Connection Lost, Reconnecting")
#                 error_status = CONNECTION_RESET_STATUS
#                 writer.close()
#                 ctx.gba_streams = None
#             if ctx.gba_status == CONNECTION_TENTATIVE_STATUS:
#                 if not error_status:
#                     logger.info("Successfully Connected to GBA")
#                     ctx.gba_status = CONNECTION_CONNECTED_STATUS
#                 else:
#                     ctx.gba_status = f"Was tentatively connected but error occurred: {error_status}"
#             elif error_status:
#                 ctx.gba_status = error_status
#                 logger.info("Lost connection to GBA and attempting to reconnect. Use /gba for status updates")
#         else:
#             try:
#                 logger.debug("Attempting to connect to GBA")
#                 ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 28922), timeout=10)
#                 ctx.gba_status = CONNECTION_TENTATIVE_STATUS
#             except TimeoutError:
#                 logger.debug("Connection Timed Out, Trying Again")
#                 ctx.gba_status = CONNECTION_TIMING_OUT_STATUS
#                 continue
#             except ConnectionRefusedError:
#                 logger.debug("Connection Refused, Trying Again")
#                 ctx.gba_status = CONNECTION_REFUSED_STATUS
#                 continue
#
#
# async def run_game(romfile):
#     options = Utils.get_options().get("GS2_options", None)
#     if options is None:
#         auto_start = True
#     else:
#         auto_start = options.get("rom_start", True)
#     if auto_start:
#         import webbrowser
#         webbrowser.open(romfile)
#     elif os.path.isfile(auto_start):
#         subprocess.Popen([auto_start, romfile],
#                          stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#
#
# async def patch_and_run_game(apGS23_file):
#     base_name = os.path.splitext(apGS23_file)[0]
#
#     with zipfile.ZipFile(apGS23_file, 'r') as patch_archive:
#         try:
#             with patch_archive.open("delta.bsdiff4", 'r') as stream:
#                 patch_data = stream.read()
#         except KeyError:
#             raise FileNotFoundError("Patch file missing from archive.")
#     rom_file = get_base_rom_path()
#
#     with open(rom_file, 'rb') as rom:
#         rom_bytes = rom.read()
#
#     patched_bytes = bsdiff4.patch(rom_bytes, patch_data)
#     patched_rom_file = base_name+".gba"
#     with open(patched_rom_file, 'wb') as patched_rom:
#         patched_rom.write(patched_bytes)
#
#     asyncio.create_task(run_game(patched_rom_file))
#
#
# def confirm_checksum():
#     rom_file = get_base_rom_path()
#     if not os.path.exists(rom_file):
#         return False
#
#     with open(rom_file, 'rb') as rom:
#         rom_bytes = rom.read()
#
#     basemd5 = hashlib.md5()
#     basemd5.update(rom_bytes)
#     return CHECKSUM_BLUE == basemd5.hexdigest()
#
#
# async def main():
#     multiprocessing.freeze_support()
#     parser = get_base_parser()
#     parser.add_argument("patch_file", default="", type=str, nargs="?",
#         help="Path to an APGS23 file")
#     args = parser.parse_args()
#     checksum_matches = confirm_checksum()
#     if checksum_matches:
#         if args.patch_file:
#             asyncio.create_task(patch_and_run_game(args.patch_file))
#
#     ctx = GS2Context(args.connect, args.password)
#     if not checksum_matches:
#         ctx.patching_error = True
#     ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
#     if gui_enabled:
#         ctx.run_gui()
#     ctx.run_cli()
#
#     ctx.gba_sync_task = asyncio.create_task(gba_sync_task(ctx), name="GBA Sync")
#     await ctx.exit_event.wait()
#     ctx.server_address = None
#     await ctx.shutdown()
#
#     if ctx.gba_sync_task:
#         await ctx.gba_sync_task
#
#
# def launch():
#     import colorama
#
#     colorama.init()
#
#     asyncio.run(main())
#     colorama.deinit()