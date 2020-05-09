#  cvrp_chromosome.py
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

from abc import abstractmethod

from combinatorial.solution import Solution


class Chromosome(Solution):
  """
  Defines the behavior of a chromosome for Genetic Algorithm.
  """

  @abstractmethod
  def mate(self, other: 'Chromosome') -> 'Chromosome':
    """
    Mate current solution with other.

    :param other: Solution to mate with.
    :return: A new solution based on this and other.
    """
    pass

  @abstractmethod
  def mutate(self) -> None:
    """
    Change this solution.

    :return: None
    """
    pass
