import model
import model_factory
from copy import deepcopy

from prettyprinter import cpprint
from random import randint, sample

class GeneticSearch:
     def __init__(self, initial_population: list[model.Floor], crossover_method=None, parents_size=None) -> None:
          self.initial_population: list[model.Floor] = initial_population
          self.NO_IMPROVEMENT_TIME = 50
          self.PARENTS_SIZE = len(self.initial_population) // 2
          if crossover_method:
               self._crossover = crossover_method
          if parents_size:
               self.PARENTS_SIZE = parents_size
          
          
     
     def run(self, always_perform=True) -> model.Floor:
          current_population = deepcopy(self.initial_population)
          highest_income = self._count_population_fitness(current_population)
          the_best_genom = max(self.initial_population, key=lambda genotype: genotype.calculate_fitness())
          
          test_iter = 0
          no_improvement_iter = 0
          while no_improvement_iter < self.NO_IMPROVEMENT_TIME:
               test_iter += 1
               parents = self._select_parents(current_population)
               childs = self._crossover_and_generate(parents)
               
               print(self._count_population_fitness(childs), max(childs, key=lambda genotype: genotype.calculate_fitness()).room_count)
               fitness = self._count_population_fitness(childs) if childs else highest_income
               if fitness > highest_income:
                    highest_income = fitness
                    the_best_genom = max(childs, key=lambda genotype: genotype.calculate_fitness())
                    no_improvement_iter = 0
                    if not always_perform:
                         self._perform_mutaion(current_population, childs)
               else:
                    no_improvement_iter += 1
                    
               if always_perform:
                    current_population = self._perform_mutaion(current_population, childs)
                    
          return the_best_genom
             
     def _count_population_fitness(self, population) -> float:
          if not population:
               return -float('inf')
          return max(population, key=lambda genotype: genotype.calculate_fitness()).calculate_fitness()
     
     def _select_parents(self, population) -> list[model.Floor]:
          # population.sort(reverse=True, key=lambda genotype: genotype.calculate_fitness())
          # return deepcopy(population[:self.PARENTS_SIZE]) # to nie działa chyba
          return sample(population, self.PARENTS_SIZE)
     
     def _crossover_and_generate(self, parents) -> list[model.Floor]:
          crossover_result = []
          for i in range(0, len(parents)-1, 2):
               child = self._crossover(parents[i], parents[i+1])
               if child.check_limitations():
                    crossover_result.append(child)
          return crossover_result
               
     def _crossover(self, parent1, parent2) -> model.Floor:
          # child = deepcopy(parent1)
          # for i in range(len(child.room_count)):
          #      child.room_count[i] = (parent1.room_count[i] + parent2.room_count[i]) // 2
          # return child
          child = deepcopy(parent1)
          for i in range(len(child.room_types)):
               bit_mask = randint(0, 1)
               if bit_mask:
                    child.room_count[i] = parent2.room_count[i]
          if child.check_limitations():
               return child
          return parent1
               
          
     
     def _perform_mutaion(self, population, childs) -> list[model.Floor]:
          population.sort(key=lambda genotype: genotype.calculate_fitness())
          # i = 0
          # for child in childs:
          #      while i < len(population) and child.calculate_fitness() < population[i].calculate_fitness():
          #           i += 1
          #      if i < len(population) and child.calculate_fitness() > population[i].calculate_fitness():
          #           population[i] = child
          #           i += 1
          # return population
          for i, child in enumerate(childs):
               population[i] = child
          return population
                    
                    
if __name__ == '__main__':
     rooms = model_factory.RoomTypeFactory.build_batch(size=5)
     # cpprint(rooms)
     # print('----------------------------------')
     
     # test - trzeba będzie generować możliwe budżety i pojemności
     budget = 0
     capacity = 0
     min_room_num = [1 for _ in range(len(rooms))]
     for room in rooms:
          budget += room.cost_of_building
          capacity += room.size
     budget *= randint(100, 200)
     capacity *= randint(4, 10)
     corridor_capacity = round(0.1 * capacity)
     # ----------------
     
     # generate initail population
     initial_population = model_factory.FloorFactory.build_batch(size=50, 
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
          
               
     
     
     
     
     
     