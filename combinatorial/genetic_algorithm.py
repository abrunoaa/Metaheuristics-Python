#  genetic_algorithm.py
#
#  Copyright (c) 2020 Bruno Almeda de Oliveira <abrunoaa@gmail.com>
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

from bisect import bisect_left
from itertools import accumulate
from random import uniform, random

from combinatorial.metaheuristic import MetaheuristicPopulationBased


class GeneticAlgorithm(MetaheuristicPopulationBased):
  """
  Genetic Algorithm implementation.
  This algorithm works based on class Solution.
  """

  @staticmethod
  def build(iterations, crossover, elitism, mutation):
    """
    Util function to build this class.

    :param iterations: Number of iterations.
    :param crossover: Probability of crossover in range [0, 1].
    :param elitism: Percentage in range [0, 1) of elite solutions (the best that don't change in an iteration).
    :param mutation: Probability of mutation in range [0, 1].
    :return: A tuple with the values to build this class.
    """
    return GeneticAlgorithm((iterations, crossover, elitism, mutation))

  def __init__(self, args):
    """
    Create an instance of simulated annealing, which can be used with many populations.

    :param args: A tuple with four values (see {@link build}): iterations, crossover, elitism and mutation.
    """
    # TODO: change args to **kwargs
    assert len(args) == 4, "Need exactly four args"
    assert 0 <= args[1] <= 1, "Crossover must be in range [0, 1]"
    assert 0 <= args[2] < 1, "Elitism must be in range [0, 1)"
    assert 0 <= args[3] <= 1, "Mutation must be in range [0, 1]"

    self.__iterations = args[0]
    self.__crossover = args[1]
    self.__elitism = args[2]
    self.__mutation = args[3]

  def execute(self, population):
    """
    Execute the Genetic Algorithm.

    :param population: List of solutions. This list may change since all operations are made in-place.
    :return: The population.
    """
    assert len(population) >= 2, "Need at least two solutions in population"
    assert int(len(population) * self.__elitism) < len(population), "All solutions are elite and won't change"

    elitism = int(self.__elitism * len(population))
    for iteration in range(self.__iterations):
      population.sort(key=lambda x: x.get_fitness())
      high = population[-1].get_fitness()
      probability = list(accumulate(high - population[i].get_fitness() + 1 for i in range(len(population))))
      for i in range(elitism, len(population)):
        if random() < self.__crossover:
          k = bisect_left(probability, uniform(0, probability[-1]))
          assert k != len(probability), "Impossible selection occurred!"
          if k == i:
            k -= 1
          population[i] = population[i].mate(population[k])
        if random() < self.__mutation:
          population[i].mutate()
        population[i].local_search()

    population.sort(key=lambda x: x.get_fitness())
    return population[0]
