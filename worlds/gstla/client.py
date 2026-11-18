from __future__ import annotations

import base64
import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self, cast

from BaseClasses import ItemClassification
from NetUtils import ClientStatus, NetworkItem
from Utils import async_start
from worlds._bizhawk import display_message, guarded_write, read, write
from worlds._bizhawk.client import BizHawkClient
from worlds.gstla.game_data.djinns import DJINN_MAPPING_TABLE_RANGE, djinn_to_flag_index
from worlds.gstla.memory import (
    AP_ITEM_SLOT,
    AP_ITEMS_RECEIVED,
    GAME_STATE_READS,
    ROM_GAME_NAME,
    ROM_SLOT_NAME,
    GameState,
)
from .deathlink import PARTY_STATE_READS, DeathDeliverer, PartyState
from .game_data.loader import load_game_data
from .gstla_types import ItemType, LocationType
from .locations import get_remote_blacklist
from .names import LocationName

if TYPE_CHECKING:
    from collections.abc import Iterable

    from worlds._bizhawk.context import BizHawkClientCommandProcessor, BizHawkClientContext
    from worlds.gstla.memory import FlagArray

logger = logging.getLogger('Client')


OPTION_NAME_TO_GOAL_NAME: dict[str, str] = {
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


def get_deprecated_options_from_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
    # Should be removed after the next release/a few months after the poptracker pack release
    options = dict(slot_data['options'])
    if 'start_with_wings' in options:
        options['start_with_wings_of_anemos'] = options.pop('start_with_wings')

    legacy_goal = slot_data.get('goal') or {}
    goals = set(legacy_goal.get('flags', ()))
    counts = legacy_goal.get('counts', {})
    if 'djinn' in counts:
        goals.add('Djinn Hunt')
        options['djinn_hunt_count'] = counts['djinn']
    if 'summons' in counts:
        goals.add('Summon Hunt')
        options['summon_hunt_count'] = counts['summons']
    options['goal'] = sorted(goals)
    return options


def get_options_from_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
    if 'v2' in slot_data['options']:
        return dict(slot_data['options']['v2'])

    return get_deprecated_options_from_slot_data(slot_data)


@dataclass(frozen=True)
class GoalRequirements:
    events: frozenset[str]
    djinn_count: int
    summon_count: int

    @classmethod
    def from_options(cls, goal: Iterable[str], djinn_hunt_count: int, summon_hunt_count: int) -> Self:
        goals = frozenset(goal)
        return cls(
            events=goals - {'Djinn Hunt', 'Summon Hunt'},
            djinn_count=djinn_hunt_count if 'Djinn Hunt' in goals else 0,
            summon_count=summon_hunt_count if 'Summon Hunt' in goals else 0,
        )


class GoalManager:
    def __init__(self):
        self.game_data = load_game_data()
        self.supported_flags: dict[str, int] = {
            name: self.game_data.event_by_name[name].flag for name in OPTION_NAME_TO_GOAL_NAME.values()
        }
        self.flag_to_name: dict[int, str] = {v: k for k, v in self.supported_flags.items()}
        self.requirements = GoalRequirements(events=frozenset(), djinn_count=0, summon_count=0)
        self.desired_flags: dict[int, int] = {}
        self.current: defaultdict[str, defaultdict[str, bool]] = defaultdict(lambda: defaultdict(lambda: False))
        self.initialized = False

    def init_reqs_from_slotdata(self, slot_data: dict[str, Any]) -> None:
        options = get_options_from_slot_data(slot_data)
        self.requirements = GoalRequirements.from_options(
            options['goal'],
            options.get('djinn_hunt_count', 0),
            options.get('summon_hunt_count', 0),
        )

        for key in self.requirements.events:
            location_name = OPTION_NAME_TO_GOAL_NAME[key]
            enemy_flag = self.supported_flags[location_name]
            self.desired_flags[enemy_flag] = self.game_data.event_by_name[location_name].id
        # logger.info(f"Desired flags: {self.desired_flags}")
        # logger.info(f"Desired counts: {self.count_requirements}")

    async def check_goals(self, client: GSTLAClient, ctx: BizHawkClientContext) -> None:
        server_flags: list[int] | None = ctx.stored_data.get(client.get_goal_flags_key(ctx), None)
        if server_flags is None:
            server_flags = []
        updated_flags: set[int] = set()
        for flag, is_set in client.goal_map.items():
            ap_id = self.desired_flags.get(flag, None)
            if ap_id is not None and is_set and ap_id not in server_flags:
                await display_message(ctx.bizhawk_ctx, self.flag_to_name.get(flag, 'Unknown') + ' Completed')
                updated_flags.add(ap_id)

        server_djinn = ctx.stored_data.get(client.get_djinn_location_key(ctx), [])
        if server_djinn is None:
            server_djinn: list[int] = []

        # Always compute difference for pop tracker
        difference = client.checked_djinn.difference(server_djinn)

        if difference:
            await display_message(
                ctx.bizhawk_ctx,
                f'Number of Djinn Obtained: {len(client.checked_djinn)}'
                + (f'/{self.requirements.djinn_count}' if self.requirements.djinn_count else ''),
            )

        if updated_flags or difference:
            # logger.info(f"Flags updated: {updated_flags}")
            # logger.info(f"Difference: {difference}")
            await client.update_goal_flags(updated_flags, ctx, include_djinn=len(difference) > 0)

    def is_done(self, client: GSTLAClient, ctx: BizHawkClientContext):
        if not self.initialized:
            return None
        goal_flags: list[int] = ctx.stored_data.get(client.get_goal_flags_key(ctx), [])
        if goal_flags is None:
            goal_flags = []
        # logger.info(f"Goal flags: {goal_flags}")
        for ap_id in self.desired_flags.values():
            if ap_id not in goal_flags:
                return False

        server_djinn = ctx.stored_data.get(client.get_djinn_location_key(ctx)) or []
        return (
            len(server_djinn) >= self.requirements.djinn_count and len(client.summons) >= self.requirements.summon_count
        )


def _handle_common_cmd(self: BizHawkClientCommandProcessor) -> GSTLAClient | None:
    from worlds._bizhawk.context import BizHawkClientContext

    if self.ctx.game != 'Golden Sun The Lost Age':
        logger.warning('This command can only be used when playing GSTLA')
        return None

    if not self.ctx.server or not self.ctx.slot:
        logger.warning('You must be connected to a server to use this command')
        return None
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, GSTLAClient)
    return client


def cmd_unchecked_djinn(self: BizHawkClientCommandProcessor) -> None:
    """Prints djinn locations that have not yet been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn in client.game_data.locations_by_type[LocationType.Djinn]:
        if djinn.flag not in client.checked_djinn:
            logger.info(djinn.name)


def cmd_checked_djinn(self: BizHawkClientCommandProcessor) -> None:
    """Prints djinn locations that have been checked"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    for djinn_id in client.checked_djinn:
        djinn = client.game_data.location_by_id[client.djinn_flag_to_loc_id[djinn_id]]
        logger.info(djinn.name)


def cmd_print_goals(self: BizHawkClientCommandProcessor) -> None:
    """Prints the goals for this seed"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    requirements = client.goals.requirements
    if requirements.events:
        logger.info('Must clear the following: ')
        for event in sorted(requirements.events):
            logger.info(event)
    if requirements.djinn_count or requirements.summon_count:
        logger.info('Obtain the following: ')
        if requirements.djinn_count:
            logger.info(f'Djinn count: {requirements.djinn_count}')
        if requirements.summon_count:
            logger.info(f'Summons count: {requirements.summon_count}')


def cmd_print_progress(self: BizHawkClientCommandProcessor) -> None:
    """Prints the current progress towards the goal"""
    client = _handle_common_cmd(self)
    if client is None:
        return
    flags: list[int] | None = self.ctx.stored_data.get(client.get_goal_flags_key(self.ctx))
    if flags is not None and len(flags) != 0:
        logger.info('Objectives Completed: ')
        for ap_id in flags:
            logger.info(client.game_data.event_locations[ap_id].name)

    djinn_count: list[int] | None = self.ctx.stored_data.get(client.get_djinn_location_key(self.ctx))
    if client.goals.requirements.djinn_count and djinn_count is not None:
        logger.info(f'Djinn count: {len(djinn_count)}')
        # logger.info("Objectives Not Completed: ")
        # for flag, cleared in flags.items():
        #     if not cleared:
        #         logger.info(flag)
    if client.goals.requirements.summon_count:
        logger.info(f'Summon count: {len(client.summons)}')


def cmd_toggle_death_link(self: BizHawkClientCommandProcessor) -> None:
    """Toggle deathlink on/off. Defaults to the deathlink setting in your YAML"""
    client = _handle_common_cmd(self)
    if client is None:
        return

    ctx = cast('BizHawkClientContext', self.ctx)  # should preferably changed somewhere up the tree
    client.death_link_initialized_for = (ctx.server_seed_name, ctx.slot)
    state_after_toggle = not client.death_link_enabled
    async_start(client.set_death_link(ctx, state_after_toggle), name='GSTLA death link toggle')


def cmd_test_death_link(self: BizHawkClientCommandProcessor) -> None:
    """Simulates somone else dying, just locally. Exactly like an incoming death link would"""
    client = _handle_common_cmd(self)
    if client is None:
        return

    if not client.death_link_enabled:
        logger.warning('DeathLink is disabled. Turn it on with /deathlink first')
        return

    if not client.was_in_game:
        logger.warning('Not in game. Load a savefile first')
        return

    if client.death_deliverer.is_delivering:
        logger.warning('A death is already in progress')
        return

    client.death_deliverer.queue_death()
    logger.info('Local death has been queued')


commands = [
    ('unchecked_djinn', cmd_unchecked_djinn),
    ('djinn', cmd_checked_djinn),
    ('goals', cmd_print_goals),
    ('goals_completed', cmd_print_progress),
    ('deathlink', cmd_toggle_death_link),
    ('deathlink_test', cmd_test_death_link),
]


class GSTLAClient(BizHawkClient):
    game = 'Golden Sun The Lost Age'
    system = 'GBA'
    patch_suffix = '.apgstla'

    def __init__(self):
        super().__init__()
        self.game_data = load_game_data()

        self.slot_name = ''
        self.flag_map: defaultdict[int, set[int]] = defaultdict(lambda: set())
        self.event_flag_map: defaultdict[int, set[int]] = defaultdict(lambda: set())
        self.goal_map: dict[int, bool] = {}
        self.djinn_ram_to_rom: dict[int, int] = {}
        self.djinn_flag_to_loc_id: dict[int, int] = {
            d.flag: d.id for d in self.game_data.locations_by_type[LocationType.Djinn]
        }
        self.checked_djinn: set[int] = set()
        self.possessed_djinn: set[int] = set()
        self.djinn_last_count: int = 0
        self.summons: set[int] = set()
        self.summon_item_index: int = 0
        for event in self.game_data.event_by_name.values():
            self.event_flag_map[event.flag].add(event.id)
        for loc in self.game_data.location_by_id.values():
            if loc.type != LocationType.Djinn:
                self.flag_map[loc.flag].add(loc.id)
        self.temp_locs: set[int] = set()
        self.temp_events: set[int] = set()
        self.local_events: set[int] = set()
        self.local_locations: set[int] = set()
        # self.starting_items: StartingItemHandler = StartingItemHandler(dict())
        self.was_in_game: bool = False
        self.coop: int = 0
        self.remote_blacklist: set[int] = get_remote_blacklist()
        self.goals = GoalManager()
        self.last_map: int = 0
        self.last_entrance: int = 0
        self.death_deliverer = DeathDeliverer()
        self.death_link_enabled: bool = False
        self.death_link_initialized_for: tuple[str | None, int | None] | None = None  # (seed, slot)
        self.previous_death_link: float = 0.0

    async def validate_rom(self, ctx: BizHawkClientContext):
        from worlds._bizhawk.context import TextCategory

        game_name = await read(ctx.bizhawk_ctx, [ROM_GAME_NAME])
        game_name = game_name[0].decode('ascii')
        logger.debug('Game loaded: %s', game_name)
        if game_name != 'GOLDEN_SUN_BAGFE01':
            for cmd, _ in commands:
                if cmd in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(cmd)
            return False
        ctx.game = self.game
        # TODO: would like to verify that the ROM is the correct one somehow
        # Possibly verify the seed; would also be nice to have the slot name encoded
        # in the rom somewhere, though not necessary
        slot_name = await read(ctx.bizhawk_ctx, [ROM_SLOT_NAME])
        if not slot_name:
            logger.warning('Could not find slot name in GSTLA ROM; please double check the ROM is correct')
        else:
            self.slot_name = base64.b64decode(slot_name[0].rstrip(b'\x00'), validate=True).decode('utf-8').strip()
        for cmd, func in commands:
            if cmd not in ctx.command_processor.commands:
                ctx.command_processor.commands[cmd] = func
        ctx.items_handling = 0b111
        ctx.watcher_timeout = 1  # not sure what a reasonable setting here is; passed to asyncio.wait_for
        ctx.text_passthrough_categories.add(TextCategory.OUTGOING)
        ctx.text_passthrough_categories.add(TextCategory.HINT)
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        ignore_slot_name = os.environ.get('GSTLA_IGNORE_SLOT_NAME') in ['1', 'true', 'yes']
        if self.slot_name and not ignore_slot_name:
            ctx.auth = self.slot_name

    async def set_death_link(self, ctx: BizHawkClientContext, enabled: bool) -> None:
        if not enabled:
            self.death_deliverer.reset()
        self.death_link_enabled = enabled
        self.previous_death_link = ctx.last_death_link
        await ctx.update_death_link(enabled)

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == 'Connected' and self.death_link_initialized_for != (ctx.server_seed_name, args.get('slot')):
            # reset deathlink when either the server or slot changes.
            self.death_link_initialized_for = None

    async def _load_djinn(self, ctx: BizHawkClientContext) -> None:
        if self.djinn_ram_to_rom:
            return
        (table,) = await read(ctx.bizhawk_ctx, [DJINN_MAPPING_TABLE_RANGE])
        for vanilla_djinn in self.game_data.djinn.values():
            entry_offset = 2 * vanilla_djinn.rom_index
            djinn_index, djinn_element = table[entry_offset : entry_offset + 2]
            placed_flag = djinn_to_flag_index(djinn_element, djinn_index)
            self.djinn_ram_to_rom[placed_flag] = vanilla_djinn.flag_index

    @staticmethod
    def get_goal_flags_key(ctx: BizHawkClientContext) -> str:
        return f'gstla_goal_flags_status_{ctx.slot}_{ctx.team}'

    @staticmethod
    def get_event_key(ctx: BizHawkClientContext) -> str:
        return f'gstla_events_status_{ctx.slot}_{ctx.team}'

    @staticmethod
    def get_djinn_location_key(ctx: BizHawkClientContext) -> str:
        return f'gstla_goal_djinn_status_{ctx.slot}_{ctx.team}'

    @staticmethod
    def get_djinn_possessed_key(ctx: BizHawkClientContext) -> str:
        return f'gstla_djinn_held_{ctx.slot}_{ctx.team}'

    @staticmethod
    def get_map_info_key(ctx: BizHawkClientContext) -> str:
        return f'gstla_map_info_{ctx.slot}_{ctx.team}'

    def check_summon_count(self, ctx: BizHawkClientContext) -> None:
        if self.summon_item_index >= len(ctx.items_received):
            return
        end = len(ctx.items_received)
        for i in range(self.summon_item_index, end):
            item = ctx.items_received[i]
            itemdata = self.game_data.item_by_id[item.item]
            if itemdata.type == ItemType.Summon:
                self.summons.add(itemdata.id)
        self.summon_item_index = end

    def _check_djinn_flags(self, flags: FlagArray) -> None:
        for owned_djinn_flag, location_flag in self.djinn_ram_to_rom.items():
            if flags.is_set(owned_djinn_flag):
                self.checked_djinn.add(location_flag)
                self.possessed_djinn.add(owned_djinn_flag)

    def _scan_flags(self, flags: FlagArray) -> tuple[set[int], set[int]]:
        location_ids: set[int] = set()
        for flag, locations in self.flag_map.items():
            if flags.is_set(flag):
                location_ids |= locations
        event_ids: set[int] = set()
        for flag, events in self.event_flag_map.items():
            if flags.is_set(flag):
                event_ids |= events
        for flag in self.goal_map:
            if flags.is_set(flag):
                self.goal_map[flag] = True
        return location_ids, event_ids

    async def _receive_items(self, ctx: BizHawkClientContext, game_state: GameState) -> None:
        if game_state.pending_item_id != 0:
            logger.debug('AP Item slot has data in it: %d', game_state.pending_item_id)
            return
        item_index = game_state.next_item_index
        cur_amount = len(ctx.items_received)
        if cur_amount <= item_index:
            return
        logger.debug('Items to give: %d, Current Item Index: %d', len(ctx.items_received), item_index)

        index_to_give = -1
        for i in range(item_index, cur_amount):
            item = ctx.items_received[i]
            if self._should_give_to_player(ctx, item):
                index_to_give = i
                break
            logger.debug(f'Should not give item {item.item} to player')

        if index_to_give == -1:
            logger.debug('None of the current items should be given')
            await write(ctx.bizhawk_ctx, [AP_ITEMS_RECEIVED.to_write(cur_amount)])
            return
        if item_index != index_to_give:
            # Update the item index so as to skip ones we don't care about
            await write(ctx.bizhawk_ctx, [AP_ITEMS_RECEIVED.to_write(index_to_give)])

        item = ctx.items_received[index_to_give]

        logger.debug('Writing Item %d to Slot', item.item)
        await write(ctx.bizhawk_ctx, [AP_ITEM_SLOT.to_write(item.item)])

    def _should_give_to_player(self, ctx: BizHawkClientContext, item: NetworkItem) -> bool:
        logger.debug('item: %s flags: %s location: %s coop: %s', item.item, item.flags, item.location, self.coop)
        if item.item in self.game_data.event_locations:
            return False
        if ctx.slot != item.player:
            return True
        if item.location < 0:
            # -1 can be the "!getitem" and "/send" command
            # -2 is the starting inventory, also allowed by "ctx.slot != item.player"
            return True
        if self.coop == 0 or item.location in self.remote_blacklist:
            return False
        return (
            self.coop == 3
            or item.flags & (ItemClassification.progression | ItemClassification.trap) > 0
            or (self.coop == 2 and item.flags & ItemClassification.useful > 0)
        )

    async def update_goal_flags(
        self, updated: set[int], ctx: BizHawkClientContext, include_djinn: bool = False
    ) -> None:
        messages = []
        if len(updated) > 0:
            messages.append(
                {
                    'cmd': 'Set',
                    'operation': 'update',
                    'want_reply': True,
                    'key': self.get_goal_flags_key(ctx),
                    'default': [],
                    'operations': [
                        {
                            'operation': 'update',
                            'value': list(updated),
                        }
                    ],
                }
            )
        if include_djinn:
            messages.append(
                {
                    'cmd': 'Set',
                    'operation': 'update',
                    'want_reply': True,
                    'key': self.get_djinn_location_key(ctx),
                    'default': [],
                    'operations': [
                        {
                            'operation': 'update',
                            'value': list(self.checked_djinn),
                        }
                    ],
                }
            )
        if messages:
            await ctx.send_msgs(messages)

    async def _handle_death_link(self, ctx: BizHawkClientContext) -> None:
        if not self.death_link_enabled or ctx.slot is None:
            return

        if ctx.last_death_link != self.previous_death_link:
            self.previous_death_link = ctx.last_death_link
            self.death_deliverer.queue_death()

        read_result = await read(ctx.bizhawk_ctx, PARTY_STATE_READS)
        game_state = PartyState.from_read_result(read_result)
        instruction = self.death_deliverer.tick(game_state)
        if instruction.writes:
            delivered = await guarded_write(ctx.bizhawk_ctx, instruction.writes, game_state.write_guards)
            if not delivered:
                self.death_deliverer.retry_delivery()
                logger.debug('DeathLink writes rejected by a guard. Retrying on next tick.')
        elif instruction.send_death:
            await ctx.send_death(f"{ctx.player_names[ctx.slot]}'s party has been defeated.")
            self.previous_death_link = ctx.last_death_link

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            logger.debug('Not connected to server...')
            return

        if self.death_link_initialized_for is None and ctx.slot_data is not None and ctx.slot is not None:
            # initializing here already before in-game check because we *could* do a "/deathlink"
            # on the title screen, which would then be overwritten once the stuff below initializes
            # with the YAML options
            await self.set_death_link(ctx, bool(get_options_from_slot_data(ctx.slot_data).get('death_link', False)))
            self.death_link_initialized_for = (ctx.server_seed_name, ctx.slot)
            logger.debug(f'DeathLink enabled: {self.death_link_enabled} with {ctx.server_seed_name=}, {ctx.slot=}')

        game_state_read = await read(ctx.bizhawk_ctx, GAME_STATE_READS)
        game_state = GameState.from_read_result(game_state_read)
        # logger.info(f'Game state read: {game_state._asdict()=}')
        if not game_state.is_in_game:
            self.death_deliverer.reset()  # makes sure title menu/game reset does not send outgoing deaths
            self.previous_death_link = ctx.last_death_link

            # TODO: if the player goes back into the save file should we reset some things?
            self.local_locations = set()
            self.was_in_game = False
            logger.debug('Not in game...')
            return

        if not self.was_in_game and ctx.slot_data is not None:
            # logger.info(f"Slot data: {ctx.slot_data}")
            # self.starting_items = StartingItemHandler(ctx.slot_data.get('start_inventory', dict()))
            self.goals.init_reqs_from_slotdata(ctx.slot_data)
            for desired_flag in self.goals.desired_flags:
                self.goal_map[desired_flag] = False
            self.check_summon_count(ctx)
            self.coop = get_options_from_slot_data(ctx.slot_data).get('coop', 0)
            ctx.set_notify(self.get_goal_flags_key(ctx), self.get_djinn_location_key(ctx))
            # logger.info(self.goals.flag_requirements)
            # logger.info(self.goals.count_requirements)
            self.was_in_game = True
            self.goals.initialized = True

        # logger.debug(
        #     f"Local locations checked: {len(self.local_locations)}; "
        #     f"server locations checked: {len(ctx.checked_locations)}"
        # )

        await self._load_djinn(ctx)
        self.temp_locs, self.temp_events = self._scan_flags(game_state.flags)
        self._check_djinn_flags(game_state.flags)

        await self._receive_items(ctx, game_state)

        await self._handle_death_link(ctx)

        self.check_summon_count(ctx)

        if self.temp_locs and self.temp_locs != self.local_locations:
            logger.debug('Sending locations to AP: %s', self.temp_locs)
            await ctx.send_msgs([{'cmd': 'LocationChecks', 'locations': list(self.temp_locs)}])
            self.local_locations = self.temp_locs

        if self.possessed_djinn and self.djinn_last_count != len(self.possessed_djinn):
            logger.debug(f'Possesed djinn: {self.possessed_djinn}')
            await ctx.send_msgs(
                [
                    {
                        'cmd': 'Set',
                        'operation': 'update',
                        'want_reply': True,
                        'key': self.get_djinn_possessed_key(ctx),
                        'default': [],
                        'operations': [
                            {
                                'operation': 'update',
                                'value': list(self.possessed_djinn),
                            }
                        ],
                    }
                ]
            )
            self.djinn_last_count = len(self.possessed_djinn)

        if self.temp_events and self.temp_events != self.local_events:
            await ctx.send_msgs(
                [
                    {
                        'cmd': 'Set',
                        'operation': 'update',
                        'want_reply': True,
                        'key': self.get_event_key(ctx),
                        'default': [],
                        'operations': [
                            {
                                'operation': 'update',
                                'value': list(self.temp_events),
                            }
                        ],
                    }
                ]
            )
            self.local_events = self.temp_events

        await self.goals.check_goals(self, ctx)

        current_map = game_state.map_id
        current_entrance = game_state.entrance_id
        if current_map != self.last_map or current_entrance != self.last_entrance:
            self.last_map = current_map
            self.last_entrance = current_entrance
            await ctx.send_msgs(
                [
                    {
                        'cmd': 'Set',
                        'key': self.get_map_info_key(ctx),
                        'default': {},
                        'want_reply': False,
                        'operations': [
                            {'operation': 'replace', 'value': {'map': current_map, 'entrance': current_entrance}}
                        ],
                    }
                ]
            )

        if not ctx.finished_game and self.goals.is_done(self, ctx):
            await ctx.send_msgs([{'cmd': 'StatusUpdate', 'status': ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
