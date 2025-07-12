from collections import defaultdict
from statistics import median, mode
from typing import Optional, List, Any

from BaseClasses import Item


class ItemStats:

    fieldnames = [
        "game",
        "player",
        "name",
        "group_name",
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
        # "weighted_score",
        "required_for_goal",
        "hard_required_for_checks",
        "min_required_for_goal",
        "min_required_for_checks",
        "early_score",
        "mid_score",
        "late_score",
        "best_score",
        "importance",
    ]

    def __init__(self,
                 item: Item,
                 player: str,
                 name: Optional[str] = None,
                 mid_game_stats: Optional['ItemStats'] = None):
        if name is None:
            self.name: str = item.name
        else:
            self.name = name
        self.item: Item = item
        self.equivalent_items: dict[Item, int] = dict()
        self.name_to_item: dict[str, Item] = dict()
        self.name_to_item[item.name] = item
        self.game = item.game
        self.player = player
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
        self.min_required_for_goal = 0
        self.min_required_for_checks = 0
        self.mid_game_stats = mid_game_stats
        # self.weighted_score = 0.0
        self.early_score_ = 0
        self.mid_score_ = 0
        self.late_score_ = 0

    def add_copy(self, item: Optional[Item] = None):
        if item != self.item:
            self.equivalent_items[item] = self.equivalent_items.get(item,0) + 1
            self.name_to_item[item.name] = item
        else:
            self.count += 1

    def goaled(self):
        self.goal_count += 1

    def checks_hard_required(self, count: int):
        self.blocked_checks = count

    @staticmethod
    def output_key(val: dict[str, Any]):
        importance = val["importance"]
        if importance == "Critical Items":
            return 0
        elif importance == "Mid Game Powerhouses":
            return 1
        elif importance == "End Game Essentials":
            return 2
        elif importance == "Decent":
            return 3
        elif importance == "Ok I Guess":
            return 4
        else:
            return 5

    def add_checks(self, new_checks: int, scale: float):
        if scale >= (1.0 - 1e-3):
            self.total_obtained += 1
            self.current_run_obtained += 1
            self.total_checks += new_checks
            self.location_counts.append(new_checks)
        self.score += (new_checks * scale) * (0.98**(self.current_run_obtained - 1))

    def add_mid_game_checks(self, new_checks: int, scale: float):
        self.mid_game_stats.add_checks(new_checks, scale)

    def reset(self):
        self.current_run_obtained = 0

    def compute_early_late_scores(self, max_score: float, max_required: int):
        early_score_weight = 0.3
        early_required_weight = 0.7
        late_score_weight = 0.1
        late_required_weight = 0.3
        late_goal_weight = 0.6
        relative_score = self.score/max_score
        if max_required > 0:
            relative_required = self.blocked_checks/max_required
        else:
            early_required_weight = 0.0
            early_score_weight = 1.0
            relative_required = 0.0
            late_score_weight = 0.5
            late_required_weight = 0.0
        self.early_score_ = (early_score_weight*relative_score) + (early_required_weight*relative_required)
        self.late_score_ = (late_score_weight*relative_score) + (late_required_weight*relative_required) + (late_goal_weight if self.required_for_goal else 0.0)

    def compute_mid_score(self, max_score: float, max_required: int):
        score_weight = 0.6
        required_weight = 0.4
        relative_score = self.mid_game_stats.score/max_score
        if max_required > 0:
            relative_required = self.mid_game_stats.blocked_checks/max_required
        else:
            required_weight = 0.0
            score_weight = 1.0
            relative_required = 0.0
        self.mid_score_ = (score_weight*relative_score) + (required_weight*relative_required)

    def to_output(self, num_sims) -> dict[str, Any]:
        ret = dict()
        ret["game"] = self.game
        ret["player"] = self.player
        name = self.item.name
        count = self.count
        if len(self.equivalent_items) > 0:
            name = name + ";" + ";".join([x.name for x in self.equivalent_items.keys()])
            for x in self.equivalent_items.values():
                count += x

        ret["name"] = name
        ret["group_name"] = self.name
        ret["count"] = count
        ret["total_obtained"] = self.total_obtained
        ret["goal_count"] = self.goal_count
        ret['avg_obtained'] = self.total_obtained / num_sims
        ret["mean_checks"] = 0 if self.total_obtained == 0 else self.total_checks / self.total_obtained
        sorted_locations = list(self.location_counts)
        sorted_locations.sort()
        # TODO: What to do with weighted score?
        ret["total_checks"] = self.total_checks
        ret["median_checks"] = median(sorted_locations)
        ret["mode_checks"] = mode(self.location_counts)
        ret["num_sims"] = num_sims
        ret["score"] = 0 if self.total_obtained == 0 else self.score/self.total_locations
        ret["required_for_goal"] = self.required_for_goal
        ret["hard_required_for_checks"] = self.blocked_checks
        ret["min_required_for_goal"] = self.min_required_for_goal
        ret["min_required_for_checks"] = self.min_required_for_checks
        ret["early_score"] = self.early_score_
        ret["late_score"] = self.late_score_
        ret["mid_score"] = self.mid_score_
        ret["best_score"] = max(self.early_score_, self.mid_score_, self.late_score_)
        importance = "Uh..."
        if self.early_score_ > 0.5:
            importance = "Critical Items"
        elif self.mid_score_ > 0.5:
            importance = "Mid Game Powerhouses"
        elif self.late_score_ > 0.5:
            importance = "End Game Essentials"
        elif ret["best_score"] >= 0.2:
            importance = "Decent"
        elif ret["best_score"] >= 0.1:
            importance = "Ok I Guess"
        ret["importance"] = importance
        return ret
