import copy
import random
import sys

from attrs import frozen, field, evolve

from src.model import Floor, RoomType

sys.path.insert(0, '../src')


@frozen
class Bee:
    position: Floor
    fitness: int = field()

    @fitness.default
    def calculate(self):
        return self.fitness_function()

    @classmethod
    def room_profit(cls, room):
        return room.frequency_of_use * room.cost_per_day - room.cost_of_maintenance - room.cost_of_building

    def fitness_function(self):
        return sum(
                self.position.room_count[i] * self.room_profit(self.position.room_types[i])
                for i in range(len(self.position.room_types))
            )


def send_close_to_bee(bee: Bee, rooms: list[RoomType]) -> Bee:
    position = bee.position
    print(position.room_count, position.capacity, position.remaining_capacity, position.cost, position.budget)
    can_remove = [i for i, count in enumerate(position.room_count) if count > position.min_room_num[i]]
    remove = random.choice(can_remove)
    new_position = evolve(position)
    new_room_count = new_position.room_count
    new_room_count[remove] -= 1

    while True:
        candidates = []
        for i, room in enumerate(rooms):
            if room.size > new_position.remaining_capacity:
                continue
            if room.cost_of_building + new_position.cost > new_position.budget:
                continue

            candidates.append(i)

        if not candidates:
            break

        new_room = random.choice(candidates)
        new_room_count[new_room] += 1

    return Bee(new_position)