#  metaheuristic.py
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

from abc import ABC, abstractmethod


class MetaheuristicSingleSolution(ABC):
  """
  Class to define behavior of metaheuristics of single solution.
  """

  @abstractmethod
  def execute(self, initial_solution):
    """
    Execute current metaheuristic with the given initial solution.

    :param initial_solution: An initial solution, which must be a single solution.
    :return: The best found solution.
    """
    pass


class MetaheuristicPopulationBased(ABC):
  """
  Class to define behavior of metaheuristics of population based.
  """

  @abstractmethod
  def execute(self, initial_population):
    """
    Execute current metaheuristic with the given initial population.

    :param initial_population: An initial solution, which must be a list of solutions.
    :return: The final population sorted by fitness.
    """
    pass
