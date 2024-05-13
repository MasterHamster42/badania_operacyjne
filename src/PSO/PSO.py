import seaborn as sns
from matplotlib import pyplot as plt

from src.model_factory import RoomTypeFactory, FloorFactory, RoomType
from Bee import Bee, send_close_to_bee
from constants import *


def initialize_population(
        population_size: int,
        rooms: list[RoomType],
        capacity: int,
        corridor_capacity: int,
        budget: int
):
    """init"""
    min_room_num = [1 for _ in rooms]
    positions = FloorFactory.build_batch(
        size=population_size,
        capacity=capacity,
        corridor_capacity=corridor_capacity,
        budget=budget,
        min_room_num=min_room_num,
        room_types=rooms
    )
    population = [Bee(position) for position in positions]
    return population


def update_best_solutions(global_best: list, new_bee: Bee):
    """list of NUM_BEST_BEES bees with the best fitness sorted"""
    fitness = new_bee.fitness
    if global_best[-1] is None or global_best[-1].fitness < fitness:
        global_best[-1] = new_bee
        id = NUM_BEST_BEES - 1
        while id > 0 and (global_best[id - 1] is None or global_best[id - 1].fitness < fitness):
            global_best[id], global_best[id - 1] = global_best[id - 1], global_best[id]
            id -= 1


def bee_algorithm(
    population_size: int,
    num_iterations: int,
    rooms: list[RoomType],
    capacity: int,
    corridor_capacity: int,
    budget: int
) -> tuple[Bee, list[float]]:
    population = initialize_population(population_size, rooms, capacity, corridor_capacity, budget)
    global_best = [None for _ in range(NUM_BEST_BEES)]
    """jak narazie global_best zostaja najlepsze odpowiedzi a wszystkie pszczoly sa wysylane gdzie indziej 
    i jesli sa lepsze wyniki to sa aktualizowane jak nie to zostaje jak jest i ciagle sie szuka kolo tego samego miejsca"""
    history = []

    for _ in range(num_iterations):
        for bee in population:
            update_best_solutions(global_best, bee)

        history.append(global_best[0].fitness)

        population = initialize_population(
            BEES_RANDOM, rooms, capacity, corridor_capacity, budget
        )  #some bees going to random places, trying to not fell for local extremum

        for bee in global_best[:NUM_STRICTLY_BEST_BEES]:  #more bees going to strictly best places
            for _ in range(BEES_FOR_TOP_BEST):
                population.append(send_close_to_bee(bee, rooms))
        for bee in global_best[NUM_STRICTLY_BEST_BEES:]:  #less bees for not the best but good places
            for _ in range(BEES_FOR_DOWN_BEST):
                population.append(send_close_to_bee(bee, rooms))  # send_close_to_bee <- TO IMPLEMENT

    # for bee in global_best:
    #     print(bee.fitness)
    return global_best[0], history


def plot_history(history: list[float]) -> None:
    sns.set_theme()
    x = range(len(history))

    sns.lineplot(x=x, y=history)
    plt.ylabel("Fitness")
    plt.xlabel("Iteration")

    plt.show()


# Example:
if __name__ == "__main__":
    rooms = RoomTypeFactory.build_batch(size=NUM_ROOM_TYPES)
    random_bee = Bee(FloorFactory.build(
        capacity=CAPACITY,
        corridor_capacity=CORRIDOR_CAPACITY,
        budget=BUDGET,
        min_room_num=[1 for _ in range(len(rooms))],
        room_types=rooms
    ))
    best_solution, fitness_history = bee_algorithm(NUM_BEES, NUM_ITERATIONS, rooms, CAPACITY, CORRIDOR_CAPACITY, BUDGET)
    print(f"Losowe rozwiązanie: {random_bee.fitness:.2e}")
    print("Najlepsze rozwiązanie:", best_solution)
    print(f"Wartość najlepszego rozwiązania: {best_solution.fitness:.2e}")

    plot_history(fitness_history)
