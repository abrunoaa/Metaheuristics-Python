#  ant_colony.py
#
#  Copyright (c) 2020 Bruno Almêda de Oliveira <abrunoaa@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
from copy import deepcopy
from random import random
from typing import List

from combinatorial.ant import Ant
from combinatorial.metaheuristic import MetaheuristicPopulationBased


# TODO: document this file
class AntColonyOptimization(MetaheuristicPopulationBased):
  """
  Ant Colony Optimization implementation.
  """

  @staticmethod
  def build(pheromone, alpha, beta, rho, stopping_condition):
    return AntColonyOptimization((alpha, beta, rho, stopping_condition, pheromone))

  @staticmethod
  def default_pheromone(dimension):
    return [[0.5 for _ in range(dimension)] for _ in range(dimension)]

  def __init__(self, args):
    # TODO: change args to **kwargs
    # TODO: add validation
    self.__alpha = args[0]
    self.__beta = args[1]
    self.__rho = args[2]
    self.__q = 1000
    self.__stopping_condition = args[3]
    self.__pheromone = args[4]

  def _update_pheromone(self, population: List[Ant]):
    n = len(self.__pheromone)
    delta = [[0 for _ in range(n)] for _ in range(n)]
    for x in population:
      x.update_delta(delta)

    mx = max(max(delta))
    for i in range(n):
      for j in range(n):
        self.__pheromone[i][j] = (1 - self.__rho) * self.__pheromone[i][j] + self.__rho * delta[i][j] / mx + 0.5

  def execute(self, population: List[Ant]):
    instance = population[0].get_instance()
    n = len(self.__pheromone)

    # TODO: raise this value to the power of beta instead of calculating inside ant, which may improve speed
    cost = instance.cost
    quality = [[self.__q / cost(u, v) if cost(u, v) != 0 else 2 * self.__q for v in range(n)] for u in range(n)]

    population.sort(key=lambda x: x.get_fitness())
    best = deepcopy(population[0])
    self.__stopping_condition.start()
    reboot = 0
    while not self.__stopping_condition:
      if reboot == 50:
        reboot = 0
        for u in range(n):
          for v in range(n):
            self.__pheromone[u][v] = 0.5

      reboot += 1
      t = self.__stopping_condition.timing()
      # print(t)
      # print([x for x in self.__pheromone])
      alpha = 10 * t
      beta = 20 * t if t < .5 else 20
      for ant in population:
        ant.travel(alpha, beta, self.__pheromone, quality)
        ant.local_search()

      population.sort(key=lambda x: x.get_fitness())
      self._update_pheromone(population)
      # if t > .5:
      #   for p in population:
      #     print(p)

      if population[0].get_fitness() < best.get_fitness():
        # print('Improved!')
        best = deepcopy(population[0])
        self.__stopping_condition.update(improved = True)
        reboot = 0
      else:
        self.__stopping_condition.update(improved = False)

    return best
