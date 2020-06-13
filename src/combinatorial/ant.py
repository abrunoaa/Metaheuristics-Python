#  ant.py
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

from abc import abstractmethod

from combinatorial.solution import Solution


class Ant(Solution):
  """
  Class to define the behavior of an ant class.
  """

  @abstractmethod
  def update_delta(self, delta) -> None:
    """
    Given an delta matrix, update it accordingly to current solution.

    :param delta: Matrix to update values of change in pheromone
    :return: None
    """
    pass

  @abstractmethod
  def travel(self, alpha, beta, pheromone, quality) -> None:
    """
    Create a new solution by traveling around the graph.
    The tour consider quality and pheromone while walking, and update delta accordingly.

    :param alpha: Significance of the pheromone
    :param beta: Significance of the quality
    :param pheromone: Matrix of pheromone of each edge
    :param quality: Matrix of quality of each edge
    :return: None
    """
    pass
