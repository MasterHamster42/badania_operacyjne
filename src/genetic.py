import model
import model_factory
from copy import deepcopy

from prettyprinter import cpprint
from random import randint, sample

import numpy as np
import matplotlib.pyplot as plt


class GeneticSearch:
    def __init__(self, initial_population: list[model.Floor], crossover_method=None, parents_size=None) -> None:
        self.initial_population: list[model.Floor] = initial_population
        self.NO_IMPROVEMENT_TIME = 300
        self.PARENTS_SIZE = len(self.initial_population)
        if crossover_method:
            self._crossover = crossover_method
        if parents_size:
            self.PARENTS_SIZE = parents_size
        self.best_hist = []

    def run(self, always_perform=True) -> model.Floor:
        current_population = deepcopy(self.initial_population)
        highest_income = self._count_population_fitness(current_population)
        # highest_income = 0
        the_best_genom = max(self.initial_population, key=lambda genotype: genotype.calculate_fitness())

        test_iter = 0
        no_improvement_iter = 0
        while no_improvement_iter < self.NO_IMPROVEMENT_TIME:
            self.best_hist.append(highest_income)
            test_iter += 1
            parents = self._select_parents(current_population)
            current_population = self._crossover_and_generate(current_population, parents)
            current_population = self._perform_mutaion(current_population)

            fitness = self._count_population_fitness(current_population)
            # if test_iter < 100:
            #      print(f'test iter: {test_iter} | highest_income: {highest_income}, fitness: {fitness}, result: {max(current_population, key=lambda genotype: genotype.calculate_fitness()).room_count}')
            # if test_iter % 50 == 0:
            #   print(f'test iter: {test_iter} | highest_fitness: {highest_income}, result: {the_best_genom.room_count}')
            if fitness > highest_income:
                highest_income = fitness
                the_best_genom = max(current_population, key=lambda genotype: genotype.calculate_fitness())
                # cpprint(f'New genotype found | iter: {test_iter}, fitness: {fitness}, result: {the_best_genom.room_count}')
                no_improvement_iter = 0
            else:
                no_improvement_iter += 1

        self.iters = test_iter
        return the_best_genom

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


def test(initial_population_size, rooms=None, N=100):
    if rooms is None:
        rooms = model_factory.RoomTypeFactory.build_batch(size=5)

    budget = 0
    capacity = 0
    min_room_num = [1 for _ in range(len(rooms))]

    for room in rooms:
        budget += room.cost_of_building
        capacity += room.size

    budget *= 100
    capacity *= 6
    corridor_capacity = round(0.1 * capacity)

    initial_population = model_factory.FloorFactory.build_batch(
        size=initial_population_size,
        capacity=capacity,
        corridor_capacity=corridor_capacity,
        budget=budget,
        min_room_num=min_room_num,
        room_types=rooms
    )

    alg = GeneticSearch(initial_population)

    initial_population_fitness = alg._count_population_fitness(initial_population)
    print("initial fitness: ", initial_population_fitness)

    iter_nos = []
    improvements = []

    max_iter = 0
    max_iter_hist = []
    for i in range(N):
        result = alg.run()

        result_fitness = result.calculate_fitness()
        cpprint(result_fitness)

        improve = result_fitness - initial_population_fitness
        improvements.append(improve / initial_population_fitness)

        iter_no = alg.iters
        iter_nos.append(iter_no)

        if iter_no > max_iter:
            max_iter = iter_no
            max_iter_hist = alg.best_hist
        alg.best_hist = []

        print(f'improve: {improve}, {(improve / initial_population_fitness * 100):.2f}%', 'AFTER ', alg.iters)

    plt.plot(max_iter_hist, linestyle='-', color='b')
    plt.xlabel('Iterations')
    plt.ylabel('Best Fitness')
    plt.title(f'Fitness Improvement over Iterations \n(Genetic, max number of iterations over {N} runs)')
    plt.grid(True)

    info_text = (
        f"mean relative improvement: {np.mean(improvements):.2f}\n"
        f"improvement st dev: {np.std(improvements):.2f}\n"
        f"max relative improvement : {np.max(improvements):.2f}\n"
        f"min relative improvement: {np.min(improvements):.2f}\n"

        f"mean iter no: {np.mean(iter_nos):.2f}\n"
        f"iter no st dev: {np.std(iter_nos):.2f}\n"
        f"max iter no: {np.max(iter_nos)}\n"
        f"min iter no: {np.min(iter_nos)}")
    plt.text(0.5, 0.40, info_text, fontsize=10, ha='left', va='top', transform=plt.gca().transAxes)

    print(
        f"mean relative improvement: {np.mean(improvements)}   |    improvement st dev: {np.std(improvements)}    |   max: {np.max(improvements)}   |   min: {np.min(improvements)}")
    print(
        f"mean iter no: {np.mean(iter_nos)}   |    iter no st dev: {np.std(iter_nos)}   |   max: {np.max(iter_nos)}   |   min: {np.min(iter_nos)}")
    plt.show()
    return improvements


if __name__ == '__main__':
    rooms = model_factory.RoomTypeFactory.build_batch(size=5)
    # cpprint(rooms)
    # print('----------------------------------')
    print(rooms)
    # test - trzeba będzie generować możliwe budżety i pojemności
    budget = 0
    capacity = 0
    min_room_num = [1 for _ in range(len(rooms))]
    for room in rooms:
        budget += room.cost_of_building
        capacity += room.size
    budget *= 100  # randint(100, 200)
    capacity *= 6  # randint(4, 10)
    corridor_capacity = round(0.1 * capacity)
    # ----------------

    # generate initail population
    initial_population = model_factory.FloorFactory.build_batch(size=6,
                                                                capacity=capacity,
                                                                corridor_capacity=corridor_capacity,
                                                                budget=budget,
                                                                min_room_num=min_room_num,
                                                                room_types=rooms)

    alg = GeneticSearch(initial_population)
    cpprint(alg._count_population_fitness(initial_population))
    cpprint(max(initial_population, key=lambda genotype: genotype.calculate_fitness()).room_count)
    result = alg.run()
    cpprint(result.calculate_fitness())
    improve = result.calculate_fitness() - alg._count_population_fitness(initial_population)
    print(f'improve: {improve}, {(improve / alg._count_population_fitness(initial_population) * 100):.2f}%')

    test(5)







