import random
from model_factory import RoomTypeFactory, DataFactory

class Bee:
    def __init__(self, position, fitness):
        self.position = position
        self.fitness = fitness

def initialize_population(population_size, rooms, floor_capacity):
    population = []
    for _ in range(population_size):
        position = DataFactory.build(room_types=rooms, floor_capacity = floor_capacity)
        population.append(Bee(position, fitness_function(position)))
    return population

def room_profit(room):
    return room.frequency_of_use * room.cost_per_day - room.cost_of_maintenance - room.cost_of_building

def fitness_function(position):
    return sum (position.room_count[i] * room_profit(position.room_types[i]) for i in range (len(position.room_types)))

def update_bee_position(bee, rooms): 
    #find solution close to current one
    new_position = None
    bee.position = new_position
    bee.fitness = fitness_function(new_position)

def update_best_solution(global_best, local_best):
    if global_best is None or local_best.fitness < global_best.fitness:
        return local_best
    return global_best

def bee_algorithm(population_size, num_iterations, search_space):
    population = initialize_population(population_size, search_space)
    global_best = None

    for _ in range(num_iterations):
        for bee in population:
            update_bee_position(bee, search_space)
            global_best = update_best_solution(global_best, bee)

    return global_best

# Przykładowe użycie:
if __name__ == "__main__":
    capacity = 10000
    rooms = RoomTypeFactory.build_batch(size=5)
    population = initialize_population(5,rooms,capacity)
    
""" best_solution = bee_algorithm(population_size, num_iterations, search_space)
    print("Najlepsze rozwiązanie:", best_solution.position)
    print("Wartość funkcji celu dla najlepszego rozwiązania:", best_solution.fitness) 
"""