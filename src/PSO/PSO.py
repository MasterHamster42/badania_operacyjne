import seaborn as sns
from matplotlib import pyplot as plt

from src.PSO.Bee import Bee, send_close_to_bee
from src.PSO.constants import BeeOptimizationConfig, PopulationConfig
from src.model import Floor
from src.populationcreator import PopulationCreator


def update_best_solutions(global_best: list, new_bee: Bee):
    """list of NUM_BEST_BEES bees with the best fitness sorted"""
    fitness = new_bee.fitness
    if global_best[-1] is None or global_best[-1].fitness < fitness:
        global_best[-1] = new_bee
        id = len(global_best) - 1
        while id > 0 and (global_best[id - 1] is None or global_best[id - 1].fitness < fitness):
            global_best[id], global_best[id - 1] = global_best[id - 1], global_best[id]
            id -= 1


def bee_algorithm(
    config: BeeOptimizationConfig,
    population_creator: PopulationCreator,
    initial_population: list[Floor]
) -> tuple[Bee, list[float]]:
    assert len(initial_population) == config.num_bees, "Population size must be equal to the bees random value"

    population = [Bee(point) for point in initial_population]
    global_best: list[None | Bee] = [None for _ in range(config.num_best_bees)]
    history = []

    for _ in range(config.num_iterations):
        for bee in population:
            update_best_solutions(global_best, bee)

        history.append(global_best[0].fitness)

        population = [Bee(point) for point in population_creator.create(size=config.bees_random)]

        for bee in global_best[:config.num_strictly_best_bees]:  #more bees going to strictly best places
            for _ in range(config.bees_for_top_best):
                population.append(send_close_to_bee(bee, population_creator.rooms))
        for bee in global_best[config.num_strictly_best_bees:]:  #less bees for not the best but good places
            for _ in range(config.bees_for_down_best):
                population.append(send_close_to_bee(bee, population_creator.rooms))  # send_close_to_bee <- TO IMPLEMENT

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
    population_config = PopulationConfig(seed=42)
    population_creator = PopulationCreator(population_config, seed=42)
    bee_config = BeeOptimizationConfig()
    starting_population = population_creator.create(size=bee_config.num_bees)

    best_solution, fitness_history = bee_algorithm(
        bee_config,
        population_creator,
        starting_population
    )
    print(f"Losowe rozwiązanie: {starting_population[0].calculate_fitness():.2e}")
    print("Najlepsze rozwiązanie:", best_solution)
    print(f"Wartość najlepszego rozwiązania: {best_solution.fitness:.2e}")

    plot_history(fitness_history)
