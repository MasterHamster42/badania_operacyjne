import random

import factory.random

from src.PSO.constants import PopulationConfig
from src.model_factory import FloorFactory


class PopulationCreator:

    def __init__(self, config: PopulationConfig, seed: int | None = None):
        self.config = config
        self.rooms = config.rooms
        if seed:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()

    def create(self, size: int, seed: int | None = None) -> list:
        if seed is None:
            seed = self.rng.randint(1, 10**10)
        factory.random.reseed_random(seed)

        min_room_num = [1 for _ in self.rooms]
        return FloorFactory.build_batch(
            size=size,
            capacity=self.config.capacity,
            corridor_capacity=self.config.corridor_capacity,
            budget=self.config.budget,
            min_room_num=min_room_num,
            room_types=self.rooms,
            room_types__seed=seed
        )


if __name__ == "__main__":
    config = PopulationConfig(seed=42)

    p = PopulationCreator(config, seed=1)
    for _ in range(3):
        print(p.create(1))
