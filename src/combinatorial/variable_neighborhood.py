#  variable_neighborhood.py
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
from typing import Tuple

from combinatorial.metaheuristic import MetaheuristicSingleSolution
from combinatorial.neighborhood import Neighborhood
from stopping.stopping_condition import StoppingCondition


class VariableNeighborhoodSearch(MetaheuristicSingleSolution):
  # TODO: document this class

  @staticmethod
  def build(stopping_condition: StoppingCondition):
    return VariableNeighborhoodSearch(tuple([stopping_condition]))

  def __init__(self, args: Tuple[StoppingCondition]):
    assert len(args) == 1
    self.__stopping_condition = args[0]

  def execute(self, initial_solution: Neighborhood):
    self.__stopping_condition.start()
    best = deepcopy(initial_solution)
    current = initial_solution
    while not self.__stopping_condition:
      current.shake()
      current.local_search()
      if current.get_fitness() < best.get_fitness():
        best = deepcopy(current)
        self.__stopping_condition.update(True)
      else:
        self.__stopping_condition.update(False)

    return best
