import random

import attrs
import pandas as pd
import factory.random
from attrs import define, field

from src.model import Floor, RoomType
from src.model_factory import RoomTypeFactory



@define
class PopulationConfig:
    """Base configuration class for population creation."""
    _seed: int | None = field(default=None)
    _rng: random.Random = field()
    number_of_room_types: int = field(default=5)
    rooms: list[RoomType] = field()
    capacity: int = field()
    corridor_capacity: int = field()
    budget: int = field()

    @_rng.default
    def _get_rng(self) -> random.Random:
        if self._seed is None:
            return random.Random()
        return random.Random(self._seed)

    @rooms.default
    def _create_rooms(self) -> list[Floor]:
        if self._seed:
            factory.random.reseed_random(self._seed)
        return RoomTypeFactory.build_batch(size=self.number_of_room_types)

    @capacity.default
    def _calculate_capacity(self) -> int:
        capacity = 0
        for room in self.rooms:
            capacity += room.size
        capacity *= self._rng.randint(4, 10)
        return capacity

    @budget.default
    def _calculate_budget(self) -> int:
        budget = 0
        for room in self.rooms:
            budget += room.cost_of_building
        budget *= self._rng.randint(100, 200)
        return budget

    @corridor_capacity.default
    def _corridor_capacity(self) -> int:
        return round(0.1 * self.capacity)

    def to_dataframe(self):
        data = {
            "Attribute": [
                "seed",
                "number_of_room_types",
                "capacity",
                "corridor_capacity",
                "budget"
            ],
            "Value": [
                self._seed,
                self.number_of_room_types,
                self.capacity,
                self.corridor_capacity,
                self.budget
            ]
        }
        return pd.DataFrame(data)

    def rooms_to_dataframe(self):
        rooms_data = [{
            "type": room.type,
            "size": room.size,
            "frequency_of_use": room.frequency_of_use,
            "cost_of_maintenance": room.cost_of_maintenance,
            "cost_of_building": room.cost_of_building,
            "cost_per_day": room.cost_per_day
        } for room in self.rooms]
        df = pd.DataFrame(rooms_data)
        return df.set_index("type")

    def copy(self):
        return attrs.evolve(self)


@define
class BeeOptimizationConfig:
    """Base configuration class for the Bee Optimization Algorithm."""

    # Algorithm parameters
    num_iterations: int = field(default=30)
    num_bees: int = field(default=20)
    num_strictly_best_bees: int = field()
    num_best_bees: int = field()
    random_percent: float = field(default=0.3)
    bees_for_top_best: int = field()
    bees_for_down_best: int = field()
    bees_random: int = field()

    @num_strictly_best_bees.default
    def _get_num_strictly_best_bees(self) -> int:
        return self.num_bees//6

    @num_best_bees.default
    def _get_num_best_bees(self) -> int:
        return self.num_bees//5

    @bees_for_top_best.default
    def _get_bees_for_top_best(self) -> int:
        """Calculates the number of bees for exploring top best solutions."""
        parent_bees = self.num_strictly_best_bees
        return int((1 - self.random_percent) * self.num_bees * 2 / 3 / parent_bees)

    @bees_for_down_best.default
    def _get_bees_for_down_best(self) -> int:
        """Calculates the number of bees for exploring down-best solutions."""
        parent_bees = self.num_best_bees - self.num_strictly_best_bees
        return int((1 - self.random_percent) * self.num_bees * 1 / 3 / parent_bees)

    @bees_random.default
    def _get_bees_random(self) -> int:
        """Calculates the number of bees for random exploration."""
        return self.num_bees - (
                self.num_strictly_best_bees * self.bees_for_top_best +
                (self.num_best_bees - self.num_strictly_best_bees) * self.bees_for_down_best
        )

    def copy(self):
        return attrs.evolve(self)