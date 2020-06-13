#  simulated_annealing.py
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
  def build(start_temperature, min_temperature, alpha, stop_condition):
    """
    Util function to build this class.

    :param start_temperature: The initial temperature of algorithm.
    :param min_temperature: The stopping temperature of algorithm.
    :param alpha: Cooling rate.
    :param stop_condition: Condition to stop. Also, it'll stop when the temperature is bellow the minimum.
    :return: A tuple with the values to build this class.
    """
    return SimulatedAnnealing((start_temperature, min_temperature, alpha, stop_condition))

  def __init__(self, args):
    """
    Create an instance of simulated annealing, which can be used with many solutions.

    :param args: A tuple with three values (see {@link build}): start_temperature, min_temperature and alpha.
    """
    # TODO: change args to **kwargs
    assert len(args) == 4, "Expected three args"
    assert all(x is not None for x in args), "Found variable with None"

    self.__start_temperature = args[0]
    self.__min_temperature = args[1]
    self.__alpha = args[2]
    self.__stop_condition = args[3]

  def execute(self, initial_solution: Solution):
    """
    Simulated Annealing implementation.

    :param initial_solution: A starting solution, which is expected to be based on class Solution.
    :return: The best solution found.
    """
    best = initial_solution
    x = best
    temperature = self.__start_temperature
    try:
      self.__stop_condition.start()
      while temperature > self.__min_temperature and not self.__stop_condition:
        y = x.neighbor()
        y.local_search()
        improved = False
        if y.get_fitness() < x.get_fitness() or uniform(0, 1) < exp((x.get_fitness() - y.get_fitness()) / temperature):
          x = y
          if x.get_fitness() < best.get_fitness():
            best = x
            improved = True
        temperature *= self.__alpha
        self.__stop_condition.update(improved)
    except RuntimeError as error:
      print(error)

    return best
