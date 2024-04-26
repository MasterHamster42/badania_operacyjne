from model_factory import RoomTypeFactory, DataFactory, RoomType
from Bee import Bee, send_close_to_bee
from constants import *

def initialize_population(population_size: int, rooms: list[RoomType], floor_capacity: int):
    """init"""
    population = []
    for _ in range(population_size):
        position = DataFactory.build(room_types=rooms, floor_capacity = floor_capacity)
        population.append(Bee(position))
    return population

def update_best_solutions(global_best: list, new_bee: Bee):
    """list of NUM_BEST_BEES bees with best fitness sorted"""
    fitness = new_bee.fitness
    if global_best[-1] == None or global_best[-1].fitness < fitness:
        global_best[-1] = new_bee
        id = NUM_BEST_BEES - 1
        while (id > 0 and (global_best[id-1] == None or global_best[id-1].fitness < fitness)):
            global_best[id],global_best[id-1] = global_best[id-1], global_best[id]
            id-=1

def bee_algorithm(population_size: int, num_iterations: int, rooms: list[RoomType], floor_capacity: int):
    population = initialize_population(population_size, rooms, floor_capacity)
    global_best = [None for _ in range (NUM_BEST_BEES)]
    """jak narazie global_best zostaja najlepsze odpowiedzi a wszystkie pszczoly sa wysylane gdzie indziej 
    i jesli sa lepsze wyniki to sa aktualizowane jak nie to zostaje jak jest i ciagle sie szuka kolo tego samego miejsca"""
    for _ in range(num_iterations):
        for bee in population:
            update_best_solutions(global_best, bee)
        population = initialize_population(BEES_RANDOM,rooms,floor_capacity) #some bees going to random places, trying to not fell for local extremum
        """for bee in global_best[:NUM_STRICTLY_BEST_BEES]: #more bees going to strictly best places
            for _ in range (BEES_FOR_TOP_BEST):
                population.append(send_close_to_bee(bee, rooms)) 
        for bee in global_best[NUM_STRICTLY_BEST_BEES:]: #less bees for not the best but good places
            for _ in range (BEES_FOR_DOWN_BEST):
                population.append(send_close_to_bee(bee, rooms)) """ # send_close_to_bee <- TO IMPLEMENT
    for bee in global_best:
        print (bee.fitness)
    return global_best[0]

# Example:
if __name__ == "__main__":
    rooms = RoomTypeFactory.build_batch(size=NUM_ROOM_TYPES)
    best_solution = bee_algorithm(NUM_BEES, NUM_ITERATIONS, rooms, CAPACITY)
    print("Najlepsze rozwiązanie:", best_solution)
    print("Wartość najlepszego rozwiązania: ", best_solution.fitness)
