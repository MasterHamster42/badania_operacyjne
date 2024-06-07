import random

import factory.random
import prettyprinter.extras.attrs
from prettyprinter import cpprint

from src.model import RoomType, Floor

prettyprinter.extras.attrs.install()


class RoomTypeFactory(factory.Factory):
    class Meta:
        model = RoomType

    type = factory.Sequence(lambda n: n)
    size = factory.Faker('random_int', min=1, max=100)
    frequency_of_use = factory.Faker('random_int', min=1, max=365)
    cost_of_maintenance = factory.Faker(
        'pyfloat', min_value=1, max_value=200000, right_digits=2)
    cost_of_building = factory.Faker(
        'pyfloat', min_value=1, max_value=200000, right_digits=2)
    cost_per_day = factory.Faker(
        'pyfloat', min_value=1, max_value=50000, right_digits=2)


class FloorFactory(factory.Factory):
    class Meta:
        model = Floor

    capacity: int = factory.Faker('random_int', min=1)
    corridor_capacity: int = factory.Faker('random_int', min=1)
    budget: int = factory.Faker('random_int', min=1)
    room_types: list[RoomType] = []
    min_room_num: list[int] = []
    room_count: list[int] = []
    
    @factory.post_generation
    def room_types(self, _, extracted, **kwargs):
        if "seed" in kwargs and kwargs['seed'] is not None:
            random.seed(kwargs['seed'])

        self.room_types = extracted
        self.room_count = [x for x in self.min_room_num]
        
        min_size = min(self.room_types, key=lambda room: room.size).size
        min_cost = min(self.room_types, key=lambda room: room.cost_of_building).cost_of_building
        capacity = self.capacity
        budget = self.budget
        
        capacity -= self.corridor_capacity

        for room, count in zip(self.room_types, self.room_count):
            capacity -= room.size * count
            budget -= room.cost_of_building * count

        while min_size < capacity and min_cost < budget:
            room_types = [x for x in self.room_types if x.size < capacity and x.cost_of_building < budget]
            choice = 0 if len(room_types) <= 1 else random.randint(0, len(room_types)-1)
            room_type = room_types[choice]

            capacity -= room_type.size
            budget -= room_type.cost_of_building
            self.room_count[choice] += 1


if __name__ == "__main__":
    rooms = RoomTypeFactory.build_batch(size=5)
    cpprint(rooms)

    min_room_num = [1 for _ in rooms]
    data = FloorFactory.build_batch(size=10, capacity=1000, corridor_capacity=100, budget=1000000, min_room_num=min_room_num, room_types=rooms)
    cpprint(data)
