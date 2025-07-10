import csv
import os
from typing import List, Set, Optional

from BaseClasses import Item, CollectionState, Location
from worlds.AutoWorld import World
from worlds.calculon import ItemStats
from worlds.calculon.ItemStats import ItemStats
from worlds.calculon.Options import CalculonOptions


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
            # if world.game == "Slay the Spire":
            # if world.game == "VVVVVV":
            # if world.game == "Minecraft":
            # if world.game == "Hollow Knight":
        #     if world.game == "Golden Sun The Lost Age":
        #     # if world.game == "Kingdom Hearts 2":
        #     # if world.game == "Pokemon Mystery Dungeon Explorers of Sky":
        #     # if world.game == "Sonic Adventure 2 Battle":
        #
        #         victim = world
        #         vampire = player
        #         break
        # else:
        #     raise Exception("Didn't find v6")
        if len(worlds_to_analyze) == 0:
            # Nothing to do
            return

        with open(os.path.join(output_directory, f"multiworld_analysis_{self.multiworld.seed_name}.csv"), 'w', newline="") as output:
            writer = csv.DictWriter(output, ItemStats.fieldnames)
            writer.writeheader()
            for world in worlds_to_analyze:
                self.analyze_world(world, writer)

    def analyze_world(self, world: World, writer: csv.DictWriter):
        prog_items: dict[str, ItemStats] = dict()
        player = world.player
        for item in self.multiworld.itempool:
            if item.player == player and item.advancement and item.code is not None:
                if item.name not in prog_items:
                    prog_items[item.name] = ItemStats(item, mid_game_stats=ItemStats(item))
                else:
                    prog_items[item.name].add_copy()
        num_sims = self.options.num_sims.value
        shuffle_me = [stats.item.name for stats in prog_items.values() for _ in range(stats.count)]
        self._leave_one_out_sim(world, prog_items, shuffle_me)
        for sim_num in range(num_sims):
            self._run_simulation(world, prog_items, shuffle_me)

        self._compute_early_scores(prog_items)

        early_game_items = {k: v for k,v in prog_items.items() if v.early_score_ >= 0.5}
        mid_prog_items = {k: v for k,v in prog_items.items() if v.early_score_ < 0.5}
        if len(mid_prog_items) > 0:
            shuffle_me = [stats.item.name for stats in mid_prog_items.values() for _ in range(stats.count)]
            for sim_num in range(num_sims):
                self._run_simulation(world, mid_prog_items, shuffle_me, early_game_items, True)
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

    def _leave_one_out_sim(self, world: World, prog_items: dict[str, ItemStats], shuffle_me: List[str]):
        locations = [x for x in world.get_locations() if not x.is_event]
        for name, stats in prog_items.items():
            state = CollectionState(self.multiworld)
            for other_name, other_stats in prog_items.items():
                if other_name == name:
                    continue
                for _ in range(other_stats.count):
                    state.collect(other_stats.item, prevent_sweep=True)
            advancement_locations = {x for x in self.multiworld.get_filled_locations(world.player) if
                                     x.advancement and x.item.name not in prog_items}
            # self._sweep_for_advancements(state, exclude=prog_items.keys())
            self._sweep_for_advancements(state, locations=advancement_locations)
            count = 0
            for loc in locations:
                if not loc.can_reach(state):
                    count += 1
            stats.checks_hard_required(count)
            if not self.multiworld.completion_condition[world.player](state):
                stats.required_for_goal = True
            stats.total_locations = len(locations)


    def _run_simulation(self, world: World, prog_items: dict[str, ItemStats], shuffle_me: List[str], pre_collect: Optional[dict[str, ItemStats]] = None, mid_game: Optional[bool]=False):
        self.random.shuffle(shuffle_me)
        state = CollectionState(self.multiworld)
        locations = [x for x in world.get_locations() if not x.is_event]
        total_locs = len(locations)
        advancement_locations = {x for x in self.multiworld.get_filled_locations(world.player) if x.advancement and x.item.name not in prog_items}
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

        for stats in prog_items.values():
            stats.reset()

        collected_names: dict[str, ItemStats] = dict()
        # index = 0
        for name in shuffle_me:
            # index += 1
            stats = prog_items[name]
            state.collect(stats.item, prevent_sweep=True)
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
            if name not in collected_names:
                collected_names[name] = stats
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
