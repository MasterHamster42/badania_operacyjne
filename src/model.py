from attr import frozen, define


@frozen
class RoomType:
    type: int
    size: int
    frequency_of_use: int
    cost_of_maintenance: float
    cost_of_building: float
    cost_per_day: float
    
@define
class Floor:
    capacity: int
    corridor_capacity: int
    budget: int
    room_types: list[RoomType] = []
    min_room_num: list[int] = []
    room_count: list[int] = []
    
    def calculate_fitness(self) -> float:
        income = 0
        for room, count in zip(self.room_types, self.room_count):
            income += room.cost_per_day * room.frequency_of_use - room.cost_of_maintenance
            income *= count
        return income
    
    def check_limitations(self) -> bool:
        return (self._check_capacity() and 
                self._check_room_count() and 
                self._check_budget())
        
    def _check_capacity(self) -> bool:
        room_capacity = 0
        for room, count in zip(self.room_types, self.room_count):
            room_capacity += room.size * count
        return room_capacity <= self.capacity - self.corridor_capacity
        
    def _check_room_count(self) -> bool:
        for count, min_count in zip(self.room_count, self.min_room_num):
            if count < min_count:
                return False
        return True
    
    def _check_budget(self) -> bool:
        cost = 0
        for room, count in zip(self.room_types, self.room_count):
            cost += count * room.cost_of_building
        return cost < self.budget