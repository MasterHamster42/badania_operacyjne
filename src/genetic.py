import model
from copy import deepcopy

from prettyprinter import cpprint
from random import randint, sample

from src.PSO.constants import PopulationConfig
from src.populationcreator import PopulationCreator


class GeneticSearch:
    def __init__(self, initial_population: list[model.Floor], crossover_method=None, parents_size=None) -> None:
        self.initial_population: list[model.Floor] = initial_population
        self.NO_IMPROVEMENT_TIME = 10
        self.PARENTS_SIZE = len(self.initial_population)
        if crossover_method:
            self._crossover = crossover_method
        if parents_size:
            self.PARENTS_SIZE = parents_size

    def run(self, always_perform=True) -> tuple[model.Floor, list[float]]:
        current_population = deepcopy(self.initial_population)
        # highest_income = self._count_population_fitness(current_population)
        highest_income = 0
        history = []
        the_best_genom = max(self.initial_population, key=lambda genotype: genotype.calculate_fitness())

        test_iter = 0
        no_improvement_iter = 0
        while no_improvement_iter < self.NO_IMPROVEMENT_TIME:
            test_iter += 1
            parents = self._select_parents(current_population)
            current_population = self._crossover_and_generate(current_population, parents)
            current_population = self._perform_mutaion(current_population)

            fitness = self._count_population_fitness(current_population)
            # if test_iter < 100:
            #      print(f'test iter: {test_iter} | highest_income: {highest_income}, fitness: {fitness}, result: {max(current_population, key=lambda genotype: genotype.calculate_fitness()).room_count}')
            if test_iter % 50 == 0:
                print(
                    f'test iter: {test_iter} | highest_fitness: {highest_income}, result: {the_best_genom.room_count}')
            if fitness > highest_income:
                highest_income = fitness
                the_best_genom = max(current_population, key=lambda genotype: genotype.calculate_fitness())
                cpprint(
                    f'New genotype found | iter: {test_iter}, fitness: {fitness}, result: {the_best_genom.room_count}')
                no_improvement_iter = 0
            else:
                no_improvement_iter += 1

            history.append(highest_income)

        return the_best_genom, history

    def _count_population_fitness(self, population: list[model.Floor]) -> float:
        if not population:
            return -float('inf')
        return max(population, key=lambda genotype: genotype.calculate_fitness()).calculate_fitness()

    def _select_parents(self, population: list[model.Floor]) -> list[model.Floor]:
        # population.sort(reverse=True, key=lambda genotype: genotype.calculate_fitness())
        # return deepcopy(population[:self.PARENTS_SIZE]) # to nie działa chyba
        return sample(population, self.PARENTS_SIZE)

    def _crossover_and_generate(self, population: list[model.Floor], parents: list[model.Floor]) -> list[model.Floor]:
        crossover_result = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = self._crossover(parents[i], parents[i + 1])
            crossover_result.append(child1)
            crossover_result.append(child2)

        new_population = deepcopy(population)
        new_population.sort(key=lambda genotype: genotype.calculate_fitness())
        for i, genotype in enumerate(crossover_result):
            new_population[i] = genotype
        return new_population

    def _crossover(self, parent1: model.Floor, parent2: model.Floor) -> tuple[model.Floor, model.Floor]:
        child1 = deepcopy(parent1)
        child2 = deepcopy(parent2)
        for i in range(len(child1.room_types)):
            bit_mask = randint(0, 1)
            if bit_mask:
                child1.room_count[i] = parent2.room_count[i]
                child2.room_count[i] = parent1.room_count[i]

        if not child1.check_limitations():
            child1 = parent1
        if not child2.check_limitations():
            child2 = parent2
        return (child1, child2)

    def _perform_mutaion(self, population: list[model.Floor]) -> list[model.Floor]:
        for genotype in population:
            room1 = randint(0, len(genotype.room_types) - 1)
            room2 = randint(0, len(genotype.room_types) - 1)
            # num_of_changes = randint(1, 2)
            num_of_changes = 1
            num_of_changes = min(num_of_changes, genotype.room_count[room1])
            genotype.room_count[room1] -= num_of_changes
            genotype.room_count[room2] += num_of_changes
            if not genotype.check_limitations():
                genotype.room_count[room1] += num_of_changes
                genotype.room_count[room2] -= num_of_changes

        return population


if __name__ == '__main__':
    population_config = PopulationConfig(seed=42)
    population_creator = PopulationCreator(population_config, seed=42)
    initial_population = population_creator.create(size=50)
    alg = GeneticSearch(initial_population)
    cpprint(alg._count_population_fitness(initial_population))
    cpprint(max(initial_population, key=lambda genotype: genotype.calculate_fitness()).room_count)
    result, history = alg.run()
    cpprint(f"{result.calculate_fitness():.2e}")
    improve = result.calculate_fitness() - alg._count_population_fitness(initial_population)
    print(f'improve: {improve}, {(improve / alg._count_population_fitness(initial_population) * 100):.2f}%')
