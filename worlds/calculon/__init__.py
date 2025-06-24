import csv
import os
from typing import List, Any, Iterable, Set, Optional
from statistics import mode, median

from BaseClasses import ItemClassification, Item, CollectionState, Location
from worlds.AutoWorld import World
from worlds.calculon.Options import CalculonOptions

class ItemStats:

    fieldnames = [
        "name",
        "count",
        "total_checks",
        "total_obtained",
        "goal_count",
        "avg_obtained",
        "mean_checks",
        "median_checks",
        "mode_checks",
        "num_sims",
        "score",
        "weighted_score",
        "required_for_goal",
        "hard_required_for_checks",
    ]

    def __init__(self, item: Item):
        self.name: str = item.name
        self.item: Item = item
        self.count: int = 1
        self.total_checks: int = 0
        self.goal_count: int = 0
        self.location_counts: List[int] = []
        self.total_obtained: int = 0
        self.required_for_goal: bool = False
        self.blocked_checks = 0
        self.score = 0.0
        self.total_locations = 0
        self.current_run_obtained = 0

    def add_copy(self):
        self.count += 1

    def goaled(self):
        self.goal_count += 1

    def checks_hard_required(self, count: int):
        self.blocked_checks = count

    def add_checks(self, new_checks: int, scale: float):
        if scale >= (1.0 - 1e-3):
            self.total_obtained += 1
            self.current_run_obtained += 1
            self.total_checks += new_checks
            self.location_counts.append(new_checks)
        self.score += (new_checks * scale) * (0.98**(self.current_run_obtained - 1))

    def reset(self):
        self.current_run_obtained = 0

    def to_output(self, num_sims) -> dict[str, Any]:
        ret = dict()
        ret["name"] = self.name
        ret["count"] = self.count
        ret["total_obtained"] = self.total_obtained
        ret["goal_count"] = self.goal_count
        ret['avg_obtained'] = self.total_obtained / num_sims
        ret["mean_checks"] = 0 if self.total_obtained == 0 else self.total_checks / self.total_obtained
        sorted_locations = list(self.location_counts)
        sorted_locations.sort()
        ret["total_checks"] = self.total_checks
        ret["median_checks"] = median(sorted_locations)
        ret["mode_checks"] = mode(self.location_counts)
        ret["num_sims"] = num_sims
        ret["score"] = 0 if self.total_obtained == 0 else self.score/self.total_locations
        ret["required_for_goal"] = self.required_for_goal
        ret["hard_required_for_checks"] = self.blocked_checks
        return ret

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

        for player, world in self.multiworld.worlds.items():
            if world.game == "Ocarina of Time":
                victim = world
                vampire = player
                break
        else:
            raise Exception("Didn't find v6")

        prog_items: dict[str, ItemStats] = dict()

        for item in self.multiworld.itempool:
            if item.player == vampire and item.advancement and item.code is not None:
                if item.name not in prog_items:
                    prog_items[item.name] = ItemStats(item)
                else:
                    prog_items[item.name].add_copy()
        num_sims = 100
        shuffle_me = [stats.item.name for stats in prog_items.values() for _ in range(stats.count)]
        self._leave_one_out_sim(victim, prog_items, shuffle_me)
        for sim_num in range(num_sims):
            self._run_simulation(victim, prog_items, shuffle_me)

        with open(os.path.join(output_directory, f"multiworld_analysis_{self.multiworld.seed_name}.csv"), 'w', newline="") as output:
            writer = csv.DictWriter(output, ItemStats.fieldnames)
            writer.writeheader()
            for stats in prog_items.values():
                writer.writerow(stats.to_output(num_sims))

    def _leave_one_out_sim(self, world: World, prog_items: dict[str, ItemStats], shuffle_me: List[str]):
        locations = [x for x in world.get_locations() if not x.is_event]
        for name, stats in prog_items.items():
            state = CollectionState(self.multiworld)
            for other_name, other_stats in prog_items.items():
                if other_name == name:
                    continue
                for _ in range(other_stats.count):
                    state.collect(other_stats.item, prevent_sweep=True)
            self._sweep_for_advancements(state, exclude=prog_items.keys())
            count = 0
            for loc in locations:
                if not loc.can_reach(state):
                    count += 1
            stats.checks_hard_required(count)
            if not self.multiworld.completion_condition[world.player](state):
                stats.required_for_goal = True
            stats.total_locations = len(locations)


    def _run_simulation(self, world: World, prog_items: dict[str, ItemStats], shuffle_me: List[str]):
        self.random.shuffle(shuffle_me)
        state = CollectionState(self.multiworld)
        locations = [x for x in world.get_locations() if not x.is_event]
        total_locs = len(locations)
        self._sweep_for_advancements(state, exclude=prog_items.keys())
        locations = [x for x in locations if not x.can_reach(state)]
        currently_available = total_locs - len(locations)
        # TODO: this doesn't really account for compounding very well
        # I.e. what happens if an item on its own doesn't unlock stuff, but in conjunction
        # with others it unlocks a ton?

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
            self._sweep_for_advancements(state, exclude=prog_items.keys())
            locations = [x for x in locations if not x.can_reach(state)]
            now_available = total_locs - len(locations)
            new_checks = now_available - currently_available
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
        print(world.get_location("Ganon").can_reach(state))
        # print(f"prog_items: {len(prog_items)}, collected_names: {len(collected_names)}, prog_item_count: {len(shuffle_me)}")
        for name in collected_names:
            prog_items[name].goaled()


    def _sweep_for_advancements(self, state: CollectionState, exclude: Set[str], locations: Optional[Iterable[Location]] = None) -> None:
        if locations is None:
            locations = self.multiworld.get_filled_locations()
        reachable_events = True
        # since the loop has a good chance to run more than once, only filter the advancements once
        locations = {location for location in locations if location.advancement and location not in state.advancements and location.item.name not in exclude}

        while reachable_events:
            reachable_events = {location for location in locations if location.can_reach(state)}
            locations -= reachable_events
            for event in reachable_events:
                state.advancements.add(event)
                assert isinstance(event.item, Item), "tried to collect Event with no Item"
                state.collect(event.item, True, event)
