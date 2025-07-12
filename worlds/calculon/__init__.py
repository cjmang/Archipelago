import csv
import logging
import os
from typing import List, Set, Optional

from BaseClasses import Item, CollectionState, Location
from Options import OptionError
from worlds.AutoWorld import World
from worlds.calculon import ItemStats
from worlds.calculon.ItemStats import ItemStats
from worlds.calculon.Options import CalculonOptions


class SimulationData:

    def __init__(self, world: World, prog_items: dict[str, ItemStats], item_groups: dict[str, Set[str]],
                 inverse_groups: dict[str, str]):
        self.world = world
        self.prog_items = prog_items
        self.item_groups = item_groups
        self.inverse_groups = inverse_groups
        self.shuffle_me = []
        for stats in self.prog_items.values():
            for _ in range(stats.count):
                self.shuffle_me.append(stats.item.name)
            if len(stats.equivalent_items) > 0:
                for item, count in stats.equivalent_items.items():
                    for _ in range(count):
                        self.shuffle_me.append(item.name)


class CalculonWorld(World):
    """
    Dramatic ...
    """
    options_dataclass = CalculonOptions
    options: CalculonOptions
    game = "Calculon"
    topology_present = False
    item_names = {}
    location_names = {}
    item_name_to_id = {}
    location_name_to_id = {}
    logger = logging.getLogger("Calculon")

    def generate_output(self, output_directory: str) -> None:
        worlds_to_analyze = []
        whitelist = self.options.games.value
        blacklist = self.options.skip_games.value
        for world in self.multiworld.worlds.values():
            if world.game == self.game:
                continue
            if len(whitelist) == 0 or world.game in whitelist:
                if world.game not in blacklist:
                    worlds_to_analyze.append(world)
        if len(worlds_to_analyze) == 0:
            # Nothing to do
            self.logger.warning("No worlds to analyze; why do you have me in here?")
            return
        with open(os.path.join(output_directory, f"multiworld_analysis_{self.multiworld.seed_name}.csv"), 'w', newline="") as output:
            writer = csv.DictWriter(output, ItemStats.fieldnames)
            writer.writeheader()
            for world in worlds_to_analyze:
                try:
                    self.analyze_world(world, writer)
                except:
                    self.logger.exception("I have failed to analyze the following world: Game='%s' Player='%s'; sorry :(", world.game, world.player_name)
                    continue

    def analyze_world(self, world: World, writer: csv.DictWriter):
        prog_items: dict[str, ItemStats] = dict()
        player = world.player
        item_groups: dict[str, Set[str]] = dict()
        inverse_groups: dict[str, str] = dict()
        if world.game in self.options.item_groups:
            game_groups = self.options.item_groups[world.game]
            for key, val in game_groups.items():
                if key == "item_groups":
                    for item_group_name in val:
                        if item_group_name in world.item_name_groups:
                            item_groups[item_group_name] = world.item_name_groups[item_group_name]
                else:
                    for inner_key, inner_val in val.items():
                        item_groups[inner_key] = inner_val

        count = 0
        for key, val in item_groups.items():
            count += len(val)
            for v in val:
                inverse_groups[v] = key

        if count != len(inverse_groups):
            raise OptionError("Invalid configuration in yaml for player %s; likely duplicate items in item groups" % world.player_name)

        for item in self.multiworld.itempool:
            if item.player == player and item.advancement and item.code is not None:
                name = item.name
                if name in inverse_groups:
                    name = inverse_groups[name]
                if name not in prog_items:
                    prog_items[name] = ItemStats(item, name=name, player=world.player_name, mid_game_stats=ItemStats(item, player=world.player_name))
                else:
                    prog_items[name].add_copy(item)
        num_sims = self.options.num_sims.value
        sim_data = SimulationData(world, prog_items, item_groups, inverse_groups)
        # shuffle_me = [stats.item.name for stats in prog_items.values() for _ in range(stats.count)]
        self._leave_one_out_sim(sim_data)
        for sim_num in range(num_sims):
            self._run_simulation(sim_data)

        self._compute_early_scores(prog_items)

        early_game_items = {k: v for k,v in prog_items.items() if v.early_score_ >= 0.5}
        mid_prog_items = {k: v for k,v in prog_items.items() if v.early_score_ < 0.5}
        if len(mid_prog_items) > 0:
            mid_item_groups = {k:v for k,v in item_groups.items() if k in mid_prog_items}
            mid_inverse_groups = dict()
            for key, val in item_groups.items():
                for v in val:
                    mid_inverse_groups[v] = key
            mid_sim_data = SimulationData(world, mid_prog_items, mid_item_groups, mid_inverse_groups)
            for sim_num in range(num_sims):
                self._run_simulation(mid_sim_data, early_game_items, True)
            self._compute_mid_scores(mid_prog_items)
        writeme = [stats.to_output(num_sims) for stats in prog_items.values()]
        writeme.sort(key=ItemStats.output_key)
        for val in writeme:
            writer.writerow(val)


    def _compute_early_scores(self, prog_items: dict[str, ItemStats]):
        max_score = -1
        max_required = -1
        for stats in prog_items.values():
            max_score = max(max_score, stats.score)
            max_required = max(max_required, stats.blocked_checks)
        if max_score <= 0:
            raise Exception("Max score was non-positive somehow")
        for stats in prog_items.values():
            stats.compute_early_late_scores(max_score, max_required)

    def _compute_mid_scores(self, prog_items: dict[str, ItemStats]):
        max_score = -1
        max_required = -1
        for stats in prog_items.values():
            max_score = max(max_score, stats.mid_game_stats.score)
            max_required = max(max_required, stats.mid_game_stats.blocked_checks)
        if max_score <= 0:
            raise Exception("Max score was non-positive somehow")
        for stats in prog_items.values():
            stats.compute_mid_score(max_score, max_required)

    def _leave_one_out_sim(self, sim_data: SimulationData):
        world = sim_data.world
        prog_items = sim_data.prog_items
        locations = [x for x in world.get_locations() if not x.is_event]
        for name, stats in prog_items.items():
            state = CollectionState(self.multiworld)
            for other_name, other_stats in prog_items.items():
                if other_name == name:
                    continue
                for _ in range(other_stats.count):
                    state.collect(other_stats.item, prevent_sweep=True)
                for item, count in other_stats.equivalent_items.items():
                    for _ in range(count):
                        state.collect(item, prevent_sweep=True)
            advancement_locations = {x for x in self.multiworld.get_filled_locations(world.player) if
                                     x.advancement and x.item.name not in prog_items}
            # self._sweep_for_advancements(state, exclude=prog_items.keys())
            self._sweep_for_advancements(state, locations=advancement_locations)
            remaining_locations = [loc for loc in locations if not loc.can_reach(state)]
            stats.checks_hard_required(len(remaining_locations))
            if not self.multiworld.completion_condition[world.player](state):
                stats.required_for_goal = True
            stats.total_locations = len(locations)
            had_remaining_locations = len(remaining_locations) != 0
            for i in range(stats.count):
                state.collect(stats.item, prevent_sweep=True)
                self._sweep_for_advancements(state, locations=advancement_locations)
                remaining_locations = [loc for loc in locations if not loc.can_reach(state)]
                if had_remaining_locations and len(remaining_locations) == 0 and stats.min_required_for_checks == 0:
                    stats.min_required_for_checks = i + 1
                if stats.required_for_goal and stats.min_required_for_goal == 0 and self.multiworld.completion_condition[world.player](state):
                    stats.min_required_for_goal = i + 1
            extras = 0
            for item, count in stats.equivalent_items.items():
                for j in range(count):
                    extras += 1
                    state.collect(item, prevent_sweep=True)
                    self._sweep_for_advancements(state, locations=advancement_locations)
                    remaining_locations = [loc for loc in locations if not loc.can_reach(state)]
                    if had_remaining_locations and len(remaining_locations) == 0 and stats.min_required_for_checks == 0:
                        stats.min_required_for_checks = stats.count + extras
                    if stats.required_for_goal and stats.min_required_for_goal == 0 and self.multiworld.completion_condition[world.player](state):
                        stats.min_required_for_goal = stats.count + extras

    def _run_simulation(self, sim_data: SimulationData, pre_collect: Optional[dict[str, ItemStats]] = None, mid_game: Optional[bool]=False):
        world = sim_data.world
        prog_items = sim_data.prog_items
        shuffle_me = sim_data.shuffle_me
        self.random.shuffle(shuffle_me)
        state = CollectionState(self.multiworld)
        locations = [x for x in world.get_locations() if not x.is_event]
        total_locs = len(locations)
        advancement_locations = {x for x in self.multiworld.get_filled_locations(world.player) if x.advancement and x.item.name not in prog_items and x.item.name not in sim_data.inverse_groups}
        # self._sweep_for_advancements(state, exclude=prog_items.keys(), locations=advancement_locations)
        self._sweep_for_advancements(state, locations=advancement_locations)
        locations = [x for x in locations if not x.can_reach(state)]
        currently_available = total_locs - len(locations)
        # TODO: this doesn't really account for compounding very well
        # I.e. what happens if an item on its own doesn't unlock stuff, but in conjunction
        # with others it unlocks a ton?

        if pre_collect is not None:
            for stats in pre_collect.values():
                for _ in range(stats.count):
                    state.collect(stats.item, prevent_sweep=True)
                    # self._sweep_for_advancements(state, exclude=prog_items.keys(), locations=advancement_locations)
                    self._sweep_for_advancements(state, locations=advancement_locations)
                for item, count in stats.equivalent_items:
                    for _ in range(count):
                        state.collect(item, prevent_sweep=True)
                        # self._sweep_for_advancements(state, exclude=prog_items.keys(), locations=advancement_locations)
                        self._sweep_for_advancements(state, locations=advancement_locations)

        for stats in prog_items.values():
            stats.reset()

        collected_names: dict[str, ItemStats] = dict()
        # index = 0
        for name in shuffle_me:
            lookup_name = name
            if name not in prog_items:
                lookup_name = sim_data.inverse_groups[name]
            stats = prog_items[lookup_name]
            item = stats.name_to_item[name]
            state.collect(item, prevent_sweep=True)
            # if name == "Gold Skulltula Token":
            #     state_dupe = state.copy()
            # state.collect(stats.item)
            # self._sweep_for_events(state)
            # self._sweep_for_advancements(state, exclude=prog_items.keys(), locations=advancement_locations)
            self._sweep_for_advancements(state, locations=advancement_locations)
            locations = [x for x in locations if not x.can_reach(state)]
            now_available = total_locs - len(locations)
            new_checks = now_available - currently_available
            if mid_game:
                stats.add_mid_game_checks(new_checks, 1.0)
            else:
                stats.add_checks(new_checks, 1.0)
            if new_checks > 0:
                previous_collected = len(collected_names)
                for i, old_stats in enumerate(collected_names.values()):
                    old_stats.add_checks(new_checks, 0.6**(previous_collected - i))
            currently_available = now_available
            if lookup_name not in collected_names:
                collected_names[lookup_name] = stats
            # print(world.get_location("Ganon").can_reach(state))
            if self.multiworld.completion_condition[world.player](state):
                break

        # print(index)
        # print(world.get_location("Ganon").can_reach(state))
        # print(f"prog_items: {len(prog_items)}, collected_names: {len(collected_names)}, prog_item_count: {len(shuffle_me)}")
        if not mid_game:
            for name in collected_names:
                prog_items[name].goaled()


    # def _sweep_for_advancements(self, state: CollectionState, locations: Set[Location], exclude: Set[str]) -> None:
    def _sweep_for_advancements(self, state: CollectionState, locations: Set[Location]) -> None:
        reachable_events = True
        # since the loop has a good chance to run more than once, only filter the advancements once
        # internal_locs = {location for location in locations if location.advancement and location not in state.advancements and location.item.name not in exclude}
        internal_locs = {location for location in locations if location.advancement and location not in state.advancements}

        while reachable_events:
            reachable_events = {location for location in internal_locs if location.can_reach(state)}
            internal_locs -= reachable_events
            locations -= reachable_events
            for event in reachable_events:
                state.advancements.add(event)
                assert isinstance(event.item, Item), "tried to collect Event with no Item"
                state.collect(event.item, True, event)

