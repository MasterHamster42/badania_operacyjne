import sys
sys.path.insert(0, '../src')

class Bee:
    def __init__(self, position):
        self.position = position
        self.fitness = self.fitness_function(position)

    def room_profit(self, room):
        return room.frequency_of_use * room.cost_per_day - room.cost_of_maintenance - room.cost_of_building

    def fitness_function(self, position):
        return sum (position.room_count[i] * self.room_profit(position.room_types[i]) for i in range (len(position.room_types)))

def send_close_to_bee(bee, rooms): 
    #find solution close to current one
    new_position = None
    bee = Bee(new_position)