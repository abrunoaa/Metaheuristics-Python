#  simulated_annealing.py
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

from math import exp
from random import uniform

from combinatorial.metaheuristic import MetaheuristicSingleSolution
from combinatorial.solution import Solution


class SimulatedAnnealing(MetaheuristicSingleSolution):
  """
  Simulated Annealing implementation.
  This algorithm works based on class Solution.
  """

  @staticmethod
  def build(start_temperature, min_temperature, alpha):
    """
    Util function to build this class.

    :param start_temperature: The initial temperature of algorithm.
    :param min_temperature: The stopping temperature of algorithm.
    :param alpha: Cooling rate.
    :return: A tuple with the values to build this class.
    """
    return SimulatedAnnealing((start_temperature, min_temperature, alpha))

  def __init__(self, args):
    """
    Create an instance of simulated annealing, which can be used with many solutions.

    :param args: A tuple with three values (see {@link build}): start_temperature, min_temperature and alpha.
    """
    # TODO: change args to **kwargs
    assert len(args) == 3, "Expected three args"
    assert all(args[i] is not None for i in range(3)), "Found variable with None"

    self.__start_temperature = args[0]
    self.__min_temperature = args[1]
    self.__alpha = args[2]

  def execute(self, initial_solution: Solution):
    """
    Simulated Annealing implementation.

    :param initial_solution: A starting solution, which is expected to be based on class Solution.
    :return: The best solution found.
    """
    best = initial_solution
    x = best
    temperature = self.__start_temperature
    while temperature > self.__min_temperature:
      y = x.neighbor()
      y.local_search()
      if y.get_fitness() < x.get_fitness() or uniform(0, 1) < exp((x.get_fitness() - y.get_fitness()) / temperature):
        x = y
        if x.get_fitness() < best.get_fitness():
          best = x
      temperature *= self.__alpha
    return best
