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
class Data:
    floor_capacity: int
    room_types: list[RoomType] = []
    room_count: list[int] = []
