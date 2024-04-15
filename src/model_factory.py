import random

import factory
import prettyprinter.extras.attrs
from prettyprinter import cpprint

from src.model import Data, RoomType

prettyprinter.extras.attrs.install()


class RoomTypeFactory(factory.Factory):
    class Meta:
        model = RoomType

    type = factory.Sequence(lambda n: n)
    size = factory.Faker('random_int', min=1, max=100)
    frequency_of_use = factory.Faker('random_int', min=1, max=365)
    cost_of_maintenance = factory.Faker('pyfloat', min_value=1, right_digits=2)
    cost_of_building = factory.Faker('pyfloat', min_value=1, right_digits=2)
    cost_per_day = factory.Faker('pyfloat', min_value=1, right_digits=2)


class DataFactory(factory.Factory):
    class Meta:
        model = Data

    floor_capacity: int = factory.Faker('random_int', min=1)
    room_types = []
    room_count = []

    @factory.post_generation
    def room_types(self, create, extracted: list[RoomType], **kwargs):
        if extracted is None:
            return

        self.room_types = random.sample(extracted, k=random.randint(1, len(extracted)))
        self.room_count = [0] * len(self.room_types)

        min_size = min(self.room_types, key=lambda room: room.size).size
        capacity = self.floor_capacity

        while min_size < capacity:
            choice = random.randint(0, len(self.room_types)-1)
            room_type = self.room_types[choice]

            if capacity - room_type.size < 0:
                continue

            capacity -= room_type.size
            self.room_count[choice] += 1


if __name__ == "__main__":
    rooms = RoomTypeFactory.build_batch(size=5)
    cpprint(rooms)

    data = DataFactory.build(room_types=rooms)
    cpprint(data)
